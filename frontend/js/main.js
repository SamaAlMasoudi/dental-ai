
// --- نظام الترجمة الشامل (100% i18n) ---
const translations = {
    en: {
        'lang-text': 'عربي',
        'nav_home': 'Home',
        'nav_analyze': 'Analyze',
        'nav_doctor': 'Doctor Portal',
        'nav_profile': 'Profile',
        'nav_logout': 'Logout',
        'login_title': 'Welcome Back',
        'login_subtitle': 'Please sign in to your account',
        'register_title': 'Create Account',
        'register_subtitle': 'Join our AI-powered dental network',
        'forgot_password_link': 'Forgot Password?',
        'forgot_password_title': 'Reset Password',
        'forgot_password_subtitle': 'Enter your details to reset password',
        'reset_btn': 'Reset Password',
        'sign_in_btn': 'Sign in',
        'sign_up_btn': 'Sign up',
        'no_account': "Don't have an account?",
        'sign_up_link': 'Sign up now',
        'upload_title': 'Drag & Drop Your X-ray',
        'upload_subtitle': 'or click to browse',
        'analyze_btn': 'Analyze Now',
        'diagnosis_title': '🧠 AI Diagnosis Result',
        'confidence_label': 'Confidence',
        'next_steps': 'Next Steps',
        'find_dentist': 'Find a Dentist',
        'chat_title': 'AI Dental Assistant',
        'chat_subtitle': 'Online & Ready',
        'chat_placeholder': 'Ask about your symptoms...',
        'footer_text': '© 2026 DentalAI. All rights reserved.',
        'welcome_msg': 'Welcome back, ',
        'profile_title': 'User Profile',
        'profile_subtitle': 'Manage your personal information',
        'save_changes': 'Save Changes',
        'role_patient': 'Patient',
        'role_doctor': 'Doctor',
        'name_label': 'Full Name',
        'email_label': 'Email Address',
        'password_label': 'Password',
        'phone_label': 'Phone Number',
        'age_label': 'Age',
        'gender_label': 'Gender',
        'history_label': 'Medical History',
        'specialty_label': 'Specialty',
        'clinic_label': 'Clinic Location',
        'experience_label': 'Years of Experience',
        'bio_label': 'Professional Bio',
        'male': 'Male',
        'female': 'Female',
        'success': 'Success',
        'error': 'Error',
        'confirm_logout': 'Are you sure you want to logout?'
    },
    ar: {
        'lang-text': 'English',
        'nav_home': 'الرئيسية',
        'nav_analyze': 'تحليل الأشعة',
        'nav_doctor': 'بوابة الطبيب',
        'nav_profile': 'الملف الشخصي',
        'nav_logout': 'تسجيل الخروج',
        'login_title': 'مرحباً بك مجدداً',
        'login_subtitle': 'الرجاء تسجيل الدخول إلى حسابك',
        'register_title': 'إنشاء حساب جديد',
        'register_subtitle': 'انضم إلى شبكة طب الأسنان الذكية',
        'forgot_password_link': 'نسيت كلمة المرور؟',
        'forgot_password_title': 'إعادة تعيين كلمة المرور',
        'forgot_password_subtitle': 'أدخل بياناتك لإعادة تعيين كلمة المرور',
        'reset_btn': 'إعادة تعيين كلمة المرور',
        'sign_in_btn': 'تسجيل الدخول',
        'sign_up_btn': 'إنشاء حساب',
        'no_account': 'ليس لديك حساب؟',
        'sign_up_link': 'أنشئ حساباً الآن',
        'upload_title': 'اسحب وأفلت صورة الأشعة',
        'upload_subtitle': 'أو انقر للتصفح',
        'analyze_btn': 'حلل الآن',
        'diagnosis_title': '🧠 نتيجة تشخيص الذكاء الاصطناعي',
        'confidence_label': 'نسبة الثقة',
        'next_steps': 'الخطوات التالية',
        'find_dentist': 'ابحث عن طبيب',
        'chat_title': 'مساعد الأسنان الذكي',
        'chat_subtitle': 'متصل وجاهز للمساعدة',
        'chat_placeholder': 'اسأل عن أعراضك أو اطلب نصيحة...',
        'footer_text': '© ٢٠٢٦ DentalAI. جميع الحقوق محفوظة.',
        'welcome_msg': 'مرحباً بك مجدداً، ',
        'profile_title': 'الملف الشخصي',
        'profile_subtitle': 'إدارة معلوماتك الشخصية',
        'save_changes': 'حفظ التغييرات',
        'role_patient': 'مريض',
        'role_doctor': 'طبيب',
        'name_label': 'الاسم الكامل',
        'email_label': 'البريد الإلكتروني',
        'password_label': 'كلمة المرور',
        'phone_label': 'رقم الهاتف',
        'age_label': 'العمر',
        'gender_label': 'الجنس',
        'history_label': 'التاريخ الطبي',
        'specialty_label': 'التخصص',
        'clinic_label': 'موقع العيادة',
        'experience_label': 'سنوات الخبرة',
        'bio_label': 'السيرة الذاتية المهنية',
        'male': 'ذكر',
        'female': 'أنثى',
        'success': 'تم بنجاح',
        'error': 'خطأ',
        'confirm_logout': 'هل أنت متأكد من تسجيل الخروج؟'
    }
};

let currentLang = localStorage.getItem('lang') || 'en';

// --- إدارة الجلسة (Session) ---
function checkAuth() {
    const publicPages = ['login.html', 'register.html', 'forgot-password.html'];
    const currentPage = window.location.pathname.split('/').pop();
    const user = localStorage.getItem('user');

    if (!user && !publicPages.includes(currentPage) && currentPage !== '') {
        window.location.href = 'login.html';
    }
}

function logout() {
    if (confirm(translations[currentLang]['confirm_logout'])) {
        localStorage.removeItem('user');
        window.location.href = 'login.html';
    }
}

// --- تحديث اللغة والواجهة ---
function updateLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    document.documentElement.dir = lang === 'ar' ? 'rtl' : 'ltr';
    document.documentElement.lang = lang;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translations[lang][key];
            } else {
                el.textContent = translations[lang][key];
            }
        }
    });

    const langText = document.getElementById('lang-text');
    if (langText) langText.textContent = translations[lang]['lang-text'];
    
    updateUserGreeting();
}

function updateUserGreeting() {
    const user = JSON.parse(localStorage.getItem('user'));
    const greetingEl = document.getElementById('user-greeting');
    if (user && greetingEl) {
        greetingEl.textContent = translations[currentLang]['welcome_msg'] + user.name;
    }
}

// --- تحليل الصور ---
async function analyzeImage() {
    const fileInput = document.getElementById('imageInput');
    const file = fileInput?.files[0];
    const user = JSON.parse(localStorage.getItem('user'));
    if (!file) {
    Swal.fire({
        text: currentLang === 'ar' ? 'الرجاء اختيار صورة أولاً' : 'Please select an image first',
        icon: 'warning',
        confirmButtonText: currentLang === 'ar' ? 'حسناً' : 'OK'
    });
    return;
}

const analyzeBtn = document.querySelector('#analyzeBtn');
if (analyzeBtn) {
    analyzeBtn.textContent = currentLang === 'ar' ? 'جاري التحليل...' : 'Analyzing...';
    analyzeBtn.disabled = true;
}

const formData = new FormData();
formData.append('image', file);
if (user) formData.append('user_id', user.id);

try {
    const response = await fetch('http://127.0.0.1:5000/predict', { method: 'POST', body: formData });
    const data = await response.json();
    if (data.success) {
        localStorage.setItem('diagnosisResult', JSON.stringify(data));
        window.location.href = 'results.html';
    } else {
        throw new Error(data.error);
    }
} catch (error) {
    Swal.fire({
        text: currentLang === 'ar' ? 'خطأ في الاتصال بالخادم' : 'Server connection error',
        icon: 'error',
        confirmButtonText: currentLang === 'ar' ? 'حسناً' : 'OK'
    });
    if (analyzeBtn) {
        analyzeBtn.textContent = translations[currentLang]['analyze_btn'];
        analyzeBtn.disabled = false;
    }
}
}

// --- تهيئة الصفحة ---
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    updateLanguage(currentLang);
    if (typeof lucide !== 'undefined') lucide.createIcons();

    const langToggle = document.getElementById('lang-toggle');
    if (langToggle) {
        langToggle.addEventListener('click', () => {
            updateLanguage(currentLang === 'en' ? 'ar' : 'en');
        });
    }
});
