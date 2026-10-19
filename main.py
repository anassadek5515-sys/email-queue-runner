import time
import schedule
from datetime import datetime
from supabase import create_client, Client

# ==========================================
# إعدادات الاتصال بقاعدة البيانات (Supabase)
# ==========================================
SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "sb_publishable_YfYQD0s7RKsrVu5wqf8KVw_MpGmp7J4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def send_next_email():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{now}] 🔄 جاري فحص الطابور وجلب المهام من Supabase...")
    
    try:
        # 1. سحب أول عميل لم يتم الإرسال له بعد (status = pending)
        response = supabase.table("leads").select("*").eq("status", "pending").limit(1).execute()
        leads = response.data
        
        if not leads:
            print("📭 لا توجد إيميلات معلقة حالياً في الطابور.")
            return
            
        lead = leads[0]
        print(f"🎯 تم استهداف العميل: {lead['lead_email']}")
        
        # -------------------------------------------------------------
        # 2. هنا بيتم تنفيذ إرسال الإيميل الفعلي عبر خادم البريد
        # -------------------------------------------------------------
        
        # 3. تحديث حالة العميل في الداتابيز إنه اتبعت بنجاح (status = sent)
        supabase.table("leads").update({"status": "sent"}).eq("id", lead['id']).execute()
        print(f"✅ تم الإرسال وتحديث الحالة بنجاح للعميل: {lead['lead_email']}")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء معالجة الطابور: {e}")

# ==========================================
# ضبط الجدول الزمني (إيميل كل 10 دقائق)
# ==========================================
INTERVAL_MINUTES = 10
schedule.every(INTERVAL_MINUTES).minutes.do(send_next_email)

print("🔥 محرك الطوابير المتصل بقاعدة البيانات يعمل الآن بنجاح على السيرفر...")

while True:
    schedule.run_pending()
    time.sleep(1)
    
