import time
import schedule
from datetime import datetime

# ==========================================
# 1. قائمة أسطول الحسابات (Account Fleet)
# ==========================================
# هنا بنسجل الحسابات اللي هتشتغل بالدور
ACCOUNTS = [
    {"email": "account1@yourdomain.com", "smtp_server": "mail.yourdomain.com", "port": 587},
    {"email": "account2@yourdomain.com", "smtp_server": "mail.yourdomain.com", "port": 587},
    {"email": "account3@yourdomain.com", "smtp_server": "mail.yourdomain.com", "port": 587},
]

# مؤشر لتحديد الحساب الحالي في الدور
current_account_index = 0

def send_next_email():
    global current_account_index
    
    # اختيار الحساب الحالي من الأسطول
    current_account = ACCOUNTS[current_account_index]
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 🚀 جاري معالجة الدور للحساب: {current_account['email']}")
    
    # -------------------------------------------------------------
    # هنا بيتم دمج منطق الربط مع الداتابيز وإرسال الإيميل (SMTP)
    # -------------------------------------------------------------
    
    # الانتقال للحساب التالي في الدور (Loop Back)
    current_account_index = (current_account_index + 1) % len(ACCOUNTS)

# ==========================================
# 2. إعداد مجدول المواعيد (Queue Interval)
# ==========================================
# ضبط الفاصل الزمني (مثلاً إرسال مهمة كل 10 دقائق)
INTERVAL_MINUTES = 10
schedule.every(INTERVAL_MINUTES).minutes.do(send_next_email)

print("🔥 تم تشغيل محرك الطوابير والتوزيع على السيرفر بنجاح...")

# تشغيل الحلقة التكرارية لضمان عمل السيرفر 24/7
while True:
    schedule.run_pending()
    time.sleep(1)
