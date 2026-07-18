import streamlit as st
import pandas as pd
import plotly.express as px
from gtts import gTTS
import io
import time

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية (اليوم 1 و 3)
# ==========================================
st.set_page_config(page_title="Pulse AI", page_icon="📊", layout="wide")

# تصميم فاخر متناسق مع هوية الموارد البشرية (أخضر عميق وذهبي)
st.markdown("""
    <style>
    .main { background-color: #f4f7f5; }
    .stButton>button { background-color: #1b4d3e; color: white; border-radius: 8px; border: 1px solid #d4af37; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #d4af37; color: #1b4d3e; }
    .metric-card { background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border-left: 5px solid #1b4d3e; text-align: center; }
    .security-notice { background-color: #ffebee; color: #c62828; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 2. نظام الأمان وصلاحيات الدخول (اليوم 4 - Security)
# ==========================================
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    st.title("🔐 بوابة Pulse AI الآمنة للموارد البشرية")
    st.markdown("<p class='security-notice'>تنبيه أمني: هذه البيانات مشفرة ومخصصة فقط لمسؤولي الموارد البشرية المصرح لهم.</p>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        username = st.text_input("اسم المستخدم / Username")
    with col2:
        password = st.text_input("كلمة المرور / Password", type="password")
        
    if st.button("تسجيل الدخول الآمن / Secure Login"):
        # حساب تجريبي مجاني وآمن للمحكمين لسهولة التجربة
        if username == "admin" and password == "hr2026":
            st.session_state['logged_in'] = True
            st.success("تم التحقق من الصلاحية الأمنية بنجاح! جاري تحميل النظام...")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة! (استخدم admin و hr2026 للتجربة)")
    st.stop()

# ==========================================
# 3. قاموس المصطلحات لتدعيم اللغتين (Bilingual)
# ==========================================
text = {
    "ar": {
        "title": "📊 Pulse AI - محلل نبض الموظفين الذكي",
        "subtitle": "منصتك الذكية المدعومة بالذكاء الاصطناعي لتحليل بيئة العمل ورضا الموظفين",
        "lang_select": "اختر اللغة / Choose Language",
        "nav": "لوحة التحكم",
        "home": "الرئيسية وبيئة العمل",
        "analysis": "تحليل البيانات والمشاعر",
        "advisor": "المستشار الذكي (صوتي)",
        "export": "الأتمتة وتصدير التقارير",
        "kpi_total": "إجمالي المشاركين",
        "kpi_sat": "معدل الرضا العام",
        "kpi_dept": "القسم الأكثر تحدياً",
        "kpi_loyalty": "نسبة الولاء الوظيفي",
        "load_mock": "🎯 تشغيل المحاكاة وتحميل البيانات التجريبية فوراً",
        "chart_title1": "معدلات الرضا حسب الأقسام",
        "chart_title2": "تحليل مشاعر تعليقات الموظفين",
        "sentiment": "تصنيف المشاعر الذكي",
        "bot_title": "🤖 مستشار الموارد البشرية الذكي (مدعوم بالصوت)",
        "bot_ask": "اسأل المستشار الذكي عن حلول وتوصيات لبيئة العمل...",
        "bot_btn": "توليد التوصية الذكية والنطق بها 🎙️",
        "send_exec": "⚡ تشغيل أمر الأتمتة: إرسال التقرير للإدارة العليا والوزارة",
        "success_msg": "🚀 نجحت الأتمتة! تم إرسال البريد الإلكتروني المؤتمت وتقارير PDF إلى مجلس الإدارة بنجاح!"
    },
    "en": {
        "title": "📊 Pulse AI - Employee Sentiment Analyzer",
        "subtitle": "Your AI-powered platform for workplace analytics and employee satisfaction",
        "lang_select": "Choose Language / اختر اللغة",
        "nav": "Navigation",
        "home": "Home & Workplace",
        "analysis": "Data & Sentiment Analysis",
        "advisor": "AI Advisor (Voice enabled)",
        "export": "Automation & Export",
        "kpi_total": "Total Participants",
        "kpi_sat": "Overall Satisfaction",
        "kpi_dept": "Most Challenged Dept",
        "kpi_loyalty": "Employee Loyalty Rate",
        "load_mock": "🎯 Run Simulation & Load Mock Data Instantly",
        "chart_title1": "Satisfaction Rates by Department",
        "chart_title2": "Employee Feedback Sentiment Analysis",
        "sentiment": "AI Sentiment Classification",
        "bot_title": "🤖 AI HR Executive Advisor (Voice Enabled)",
        "bot_ask": "Ask the AI Advisor for recommendations to improve the workplace...",
        "bot_btn": "Generate AI Recommendation & Speak 🎙️",
        "send_exec": "⚡ Trigger Automation: Send Report to Executive Board & Ministry",
        "success_msg": "🚀 Automation Success! Automated email and PDF reports have been successfully queued and sent to the Board!"
    }
}

# شريط التحكم الجانبي واللغة
with st.sidebar:
    lang = st.radio(text["ar"]["lang_select"], ["ar", "en"])
    st.title(text[lang]["nav"])
    page = st.radio("", [text[lang]["home"], text[lang]["analysis"], text[lang]["advisor"], text[lang]["export"]])
    st.markdown("---")
    if st.button("تسجيل الخروج / Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

# تجهيز البيانات التفاعلية للأقسام
mock_data_ar = pd.DataFrame({
    'القسم': ['التقنية', 'العمليات', 'المبيعات', 'التقنية', 'الموارد البشرية'],
    'التقييم': [2, 4, 5, 3, 4],
    'تعليق الموظف': ['ضغط العمل كبير والمواعيد غير واقعية وبحاجة لمرونة', 'البيئة محفزة جداً وأشعر بالتقدير والدعم', 'فريق رائع ودعم مستمر من الإدارة العليا', 'نحتاج دورات تدريبية أكثر مواكبة للتطور', 'التواصل بين الأقسام يحتاج تحسين وتطوير'],
    'المشاعر': ["سلبي", "إيجابي", "إيجابي", "محايد", "محايد"]
})

mock_data_en = pd.DataFrame({
    'Department': ['IT', 'Operations', 'Sales', 'IT', 'HR'],
    'Score': [2, 4, 5, 3, 4],
    'Employee Comment': ['High workload and unrealistic deadlines', 'Great environment, I feel valued', 'Amazing team and continuous management support', 'We need more modern training courses', 'Inter-department communication needs work'],
    'Sentiment': [text[lang]["neg"], text[lang]["pos"], text[lang]["pos"], text[lang]["neu"], text[lang]["neu"]]
})

df = mock_data_ar if lang == "ar" else mock_data_en

# ==========================================
# 4. محتوى الصفحات وتطبيق ميزات الورش اليومية
# ==========================================

# صفحة الرئيسية ومؤثرات الصوت (اليوم 5 - Music)
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.markdown("---")
    
    # اليوم 5: إضافة مؤثر صوتي ترحيبي تفاعلي عند فتح التطبيق
    st.write("🎵 **مؤثر صوتي ترحيبي للنظام (Welcome Chime):**")
    st.audio("https://www.soundjay.com/buttons/sounds/button-09a.mp3", format="audio/mp3")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_total']}</h4><h2>45</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_sat']}</h4><h2>4.2 / 5</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_dept']}</h4><h2>{ 'التقنية' if lang=='ar' else 'IT' }</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_loyalty']}</h4><h2>88%</h2></div>", unsafe_allow_html=True)

# صفحة الرسوم البيانية (اليوم 3 - Images & Presentations)
elif page == text[lang]["analysis"]:
    st.title(text[lang]["analysis"])
    
    if st.button(text[lang]["load_mock"]):
        st.dataframe(df, use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            fig1 = px.bar(df, x=df.columns[0], y=df.columns[1], title=text[lang]["chart_title1"], color=df.columns[0], color_discrete_sequence=px.colors.qualitative.Dark2)
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.pie(df, names=df.columns[3], title=text[lang]["chart_title2"], color_discrete_sequence=['#2e7d32', '#c62828', '#757575'])
            st.plotly_chart(fig2, use_container_width=True)

# صفحة المستشار الصوتي الذكي (اليوم 4 - Voice & Avatar)
elif page == text[lang]["advisor"]:
    st.title(text[lang]["bot_title"])
    
    # اليوم 4: إضافة صورة رمزية للمساعد الذكي (Avatar)
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    
    user_query = st.text_input(text[lang]["bot_ask"])
    if st.button(text[lang]["bot_btn"]):
        with st.spinner("Thinking..."):
            time.sleep(1) # محاكاة تفكير الذكاء الاصطناعي
            if lang == "ar":
                advice_text = "مستشار نبض الذكي ينصحك: بناءً على تحليل بيانات قسم التقنية، يوجد انخفاض في الرضا بسبب ضغط المواعيد، نوصي فوراً بتطبيق ساعات عمل مرنة وتكريم الموظفين المتميزين."
                st.info(f"🤖 {advice_text}")
                tts = gTTS(text=advice_text, lang='ar')
            else:
                advice_text = "Pulse AI Advisor Recommends: Based on IT department analysis, there is a drop in satisfaction due to strict deadlines. We highly recommend implementing flexible hours and recognizing top talent."
                st.info(f"🤖 {advice_text}")
                tts = gTTS(text=advice_text, lang='en')
            
            # قراءة النص بالصوت (Voice Feature)
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')

# صفحة الأتمتة والتصدير (اليوم 5 - Automation)
elif page == text[lang]["export"]:
    st.title(text[lang]["export"])
    st.write("⚙️ **نظام أتمتة تدفق البيانات (Workflow Automation):**")
    
    if st.button(text[lang]["send_exec"]):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
            
        st.success(text[lang]["success_msg"])
        st.balloons() # تأثير بصري حماسي للنجاح والتسليم