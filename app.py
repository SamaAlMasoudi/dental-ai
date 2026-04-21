import os
import numpy as np
import sqlite3
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from werkzeug.utils import secure_filename
from datetime import datetime

app = Flask(__name__)
@app.route('/')
def index():
    return send_from_directory('frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    return send_from_directory('frontend', path)
CORS(app)

# --- إعدادات المجلدات ---
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- 1. إعداد قاعدة البيانات (SQLite) ---
def init_db():
    conn = sqlite3.connect('dental_ai.db')
    c = conn.cursor()
    # جدول المستخدمين (مرضى، أطباء، ومسؤولين)
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  name TEXT NOT NULL, 
                  email TEXT UNIQUE NOT NULL, 
                  password TEXT NOT NULL, 
                  role TEXT NOT NULL,
                  phone TEXT,
                  age INTEGER,
                  gender TEXT,
                  history TEXT,
                  specialty TEXT,
                  clinic_location TEXT,
                  experience INTEGER,
                  bio TEXT)''')
    # جدول التحليلات
    c.execute('''CREATE TABLE IF NOT EXISTS analyses 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  user_id INTEGER, image_path TEXT, prediction TEXT, 
                  confidence REAL, date TEXT)''')
    
    # إنشاء حساب المسؤول (Admin) لأول مرة فقط إذا لم يكن موجوداً
    admin_email = "admin@dentalai.com"
    admin_pass = "Admin@2026#Secure"
    c.execute("SELECT id FROM users WHERE email=?", (admin_email,))
    if not c.fetchone():
        c.execute("INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                  ("System Administrator", admin_email, admin_pass, "admin"))
    
    conn.commit()
    conn.close()

init_db()

# --- 2. تحميل نموذج الذكاء الاصطناعي ---
MODEL_PATH = 'model.h5'
model = None
CLASS_NAMES = ['BDC-BDR', 'Caries', 'Fractured', 'Healthy', 'Infection']

if os.path.exists(MODEL_PATH):
    model = load_model(MODEL_PATH)
    print("Model loaded successfully!")

# --- 3. مسارات الـ API (Authentication & Profile) ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    try:
        conn = sqlite3.connect('dental_ai.db')
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE email=?", (data['email'],))
        if c.fetchone():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        if data['role'] == 'patient':
            c.execute("INSERT INTO users (name, email, password, role, phone, age, gender, history) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                      (data['name'], data['email'], data['password'], 'patient', data['phone'], data['age'], data['gender'], data['history']))
        else:
            c.execute("INSERT INTO users (name, email, password, role, phone, specialty, clinic_location, experience, bio) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (data['name'], data['email'], data['password'], 'doctor', data['phone'], data['specialty'], data['clinic_location'], data['experience'], data['bio']))
        
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Registration successful'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    conn = sqlite3.connect('dental_ai.db')
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE email=? AND password=?", (data['email'], data['password']))
    user = c.fetchone()
    conn.close()
    if user:
        user_data = {
            'id': user[0], 'name': user[1], 'email': user[2], 'role': user[4],
            'phone': user[5], 'age': user[6], 'gender': user[7], 'history': user[8],
            'specialty': user[9], 'clinic_location': user[10], 'experience': user[11], 'bio': user[12]
        }
        return jsonify({'success': True, 'user': user_data})
    return jsonify({'success': False, 'message': 'Invalid email or password'}), 401

# --- 4. مسارات المسؤول (Admin Routes) ---
@app.route('/admin/dashboard', methods=['GET'])
def admin_dashboard():
    try:
        conn = sqlite3.connect('dental_ai.db')
        c = conn.cursor()
        # جلب كافة المستخدمين
        c.execute("SELECT id, name, email, role, phone FROM users")
        users = [{'id': r[0], 'name': r[1], 'email': r[2], 'role': r[3], 'phone': r[4]} for r in c.fetchall()]
        # جلب كافة التحليلات
        c.execute("SELECT a.id, u.name, a.prediction, a.confidence, a.date FROM analyses a JOIN users u ON a.user_id = u.id")
        analyses = [{'id': r[0], 'user_name': r[1], 'prediction': r[2], 'confidence': r[3], 'date': r[4]} for r in c.fetchall()]
        conn.close()
        return jsonify({'success': True, 'users': users, 'analyses': analyses})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin/delete-user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        conn = sqlite3.connect('dental_ai.db')
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE id=?", (user_id,))
        c.execute("DELETE FROM analyses WHERE user_id=?", (user_id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'User deleted successfully'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# --- 5. مسار تحليل الصور ---
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'success': False, 'error': 'Model not loaded'}), 500
    try:
        file = request.files['image']
        user_id = request.form.get('user_id')
        filename = secure_filename(f"{datetime.now().timestamp()}_{file.filename}")
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        img = image.load_img(filepath, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0
        
        predictions = model.predict(img_array)
        class_idx = np.argmax(predictions[0])
        confidence = float(np.max(predictions[0]) * 100)
        result = CLASS_NAMES[class_idx]
        
        if user_id:
            conn = sqlite3.connect('dental_ai.db')
            c = conn.cursor()
            c.execute("INSERT INTO analyses (user_id, image_path, prediction, confidence, date) VALUES (?, ?, ?, ?, ?)",
                      (user_id, filename, result, confidence, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            conn.commit()
            conn.close()

        return jsonify({
            'success': True,
            'prediction': result,
            'confidence': round(confidence, 2),
            'image_url': f'http://127.0.0.1:5000/uploads/{filename}'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
   
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7860)
