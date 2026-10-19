import os
import time
import schedule
from supabase import create_client, Client

# Supabase Credentials
SUPABASE_URL = "https://yixhxiwyjkjbgyooicuo.supabase.co"
SUPABASE_KEY = "sb_publishable_YfYQD0s7RKsrVu5wqf8KVw_MpGmp7J4"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def process_queue():
    print("🚀 جاري فحص الطابور وجلب المهام من Supabase...")
    try:
        # جلب أول إيميل حالته pending
        response = supabase.table("leads").select("*").eq("status", "pending").limit(1).execute()
        leads = response.data

        if leads:
            lead = leads[0]
            lead_id = lead["id"]
            lead_email = lead["lead_email"]

            print(f"📧 جاري معالجة الإيميل: {lead_email}")

            # تحديث الحالة إلى sent
            supabase.table("leads").update({"status": "sent"}).eq("id", lead_id).execute()
            print(f"✅ تم تحديث حالة {lead_email} إلى sent بنجاح!")
        else:
            print("😴 لا توجد إيميلات معلقة (pending) حالياً.")

    except Exception as e:
        print(f"❌ حدث خطأ أثناء المعالجة: {e}")

# تشغيل الفحص كل دقيقة للاختبار
schedule.every(1).minutes.do(process_queue)

print("🔥 تم تشغيل محرك الطوابير والتوزيع على السيرفر بنجاح...")

# تشغيل الكود في حلقة مستمرة
process_queue()  # تشغيل أول مرة فوراً عند بدء السيرفر
while True:
    schedule.run_pending()
    time.sleep(1)
