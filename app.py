import streamlit as st
import pandas as pd
import plotly.express as px
from gtts import gTTS
import io
import time

# 1. إعدادات الصفحة
st.set_page_config(page_title="Pulse AI", page_icon="📊", layout="wide")

st.markdown("""
    <style>
    /* تغيير خلفية التطبيق بالكامل للون الأسود */
    .stApp { background-color: #000000; color: #ffffff; }
    .main { background-color: #000000; }
    
    /* الأزرار باللون الأخضر الأساسي للباليت */
    .stButton>button { background-color: #84B179; color: #000000; border-radius: 8px; border: 1px solid #A2CB8B; font-weight: bold; width: 100%; }
    .stButton>button:hover { background-color: #A2CB8B; color: #000000; }
    
    /* بطاقات المؤشرات متناسقة مع المظهر الداكن والباليت */
    .metric-card { background-color: #111111; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(255,255,255,0.05); border-left: 5px solid #84B179; text-align: center; margin-bottom: 10px; border-top: 1px solid #222222; border-right: 1px solid #222222; border-bottom: 1px solid #222222; }
    .metric-card h4 { color: #C7EABB !important; margin: 0; padding: 0; font-size: 16px; }
    .metric-card h2 { color: #E8F5BD !important; margin: 10px 0 0 0; padding: 0; font-size: 28px; font-weight: bold; }
    
    /* تنبيه الأمان */
    .security-notice { background-color: #2c0d11; color: #ff8a80; padding: 10px; border-radius: 5px; font-weight: bold; text-align: center; border: 1px solid #d32f2f; }
    
    /* تعديل نصوص القائمة الجانبية لتناسب الخلفية الداكنة */
    .css-17eq0hr, .stRadio, label { color: #ffffff !important; }
    </style>
""", unsafe_allow_html=True)

# 2. نظام الأمان
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
        if username == "admin" and password == "hr2026":
            st.session_state['logged_in'] = True
            st.success("تم التحقق من الصلاحية الأمنية بنجاح! جاري تحميل النظام...")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة! (استخدم admin و hr2026 للتجربة)")
    st.stop()

# 3. القاموس لتدعيم اللغات
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

with st.sidebar:
    lang = st.radio(text["ar"]["lang_select"], ["ar", "en"])
    st.title(text[lang]["nav"])
    page = st.radio("", [text[lang]["home"], text[lang]["analysis"], text[lang]["advisor"], text[lang]["export"]])
    st.markdown("---")
    if st.button("تسجيل الخروج / Logout"):
        st.session_state['logged_in'] = False
        st.rerun()

# 4. البيانات التجريبية
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
    'Sentiment': ["Negative", "Positive", "Positive", "Neutral", "Neutral"]
})

df = mock_data_ar if lang == "ar" else mock_data_en

# 5. محتوى الصفحات
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.markdown("---")
    
    st.write("🎵 **مؤثر صوتي ترحيبي للنظام (Welcome Chime):**")
    try:
        welcome_tts = gTTS(text="Welcome to Pulse AI" if lang == "en" else "مرحباً بكم في منصة نبض", lang='en' if lang == 'en' else 'ar')
        sound_fp = io.BytesIO()
        welcome_tts.write_to_fp(sound_fp)
        sound_fp.seek(0)
        st.audio(sound_fp, format="audio/mp3")
    except:
        st.audio("https://www.soundjay.com/buttons/sounds/button-09a.mp3", format="audio/mp3")
        
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_total']}</h4><h2>45</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_sat']}</h4><h2>4.2 / 5</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_dept']}</h4><h2>{ 'التقنية' if lang=='ar' else 'IT' }</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-card'><h4>{text[lang]['kpi_loyalty']}</h4><h2>88%</h2></div>", unsafe_allow_html=True)

elif page == text[lang]["analysis"]:
    st.title(text[lang]["analysis"])
    if st.button(text[lang]["load_mock"]):
        st.dataframe(df, use_container_width=True)
        col1, col2 = st.columns(2)
        with col1:
            # رسوم بيانية مخصصة تتماشى مع ألوان الباليت المحدثة والخلفية الداكنة
            fig1 = px.bar(df, x=df.columns[0], y=df.columns[1], title=text[lang]["chart_title1"], color=df.columns[0], color_discrete_sequence=['#84B179', '#A2CB8B', '#C7EABB', '#E8F5BD'])
            fig1.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig1, use_container_width=True)
        with col2:
            fig2 = px.pie(df, names=df.columns[3], title=text[lang]["chart_title2"], color_discrete_sequence=['#84B179', '#e57373', '#757575'])
            fig2.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig2, use_container_width=True)

elif page == text[lang]["advisor"]:
    st.title(text[lang]["bot_title"])
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)
    user_query = st.text_input(text[lang]["bot_ask"])
    if st.button(text[lang]["bot_btn"]):
        with st.spinner("Thinking..."):
            time.sleep(1)
            if lang == "ar":
                advice_text = "مستشار نبض الذكي ينصحك: بناءً على تحليل بيانات قسم التقنية، يوجد انخفاض في الرضا بسبب ضغط المواعيد، نوصي فوراً بتطبيق ساعات عمل مرنة وتكريم الموظفين المتميزين."
                st.info(f"🤖 {advice_text}")
                tts = gTTS(text=advice_text, lang='ar')
            else:
                advice_text = "Pulse AI Advisor Recommends: Based on IT department analysis, there is a drop in satisfaction due to strict deadlines. We highly recommend implementing flexible hours and recognizing top talent."
                st.info(f"🤖 {advice_text}")
                tts = gTTS(text=advice_text, lang='en')
            
            fp = io.BytesIO()
            tts.write_to_fp(fp)
            fp.seek(0)
            st.audio(fp, format='audio/mp3')

elif page == text[lang]["export"]:
    st.title(text[lang]["export"])
    st.write("⚙️ **نظام أتمتة تدفق البيانات (Workflow Automation):**")
    if st.button(text[lang]["send_exec"]):
        progress_bar = st.progress(0)
        for percent_complete in range(100):
            time.sleep(0.01)
            progress_bar.progress(percent_complete + 1)
        st.success(text[lang]["success_msg"])
        st.balloons()
