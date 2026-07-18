import streamlit as st
import pandas as pd
import plotly.express as px
from gtts import gTTS
import io
import time

# ==========================================
# 1. إعدادات الصفحة والهوية البصرية
# ==========================================
st.set_page_config(page_title="Pulse AI", page_icon="📊", layout="wide")

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
# 2. نظام الأمان وصلاحيات الدخول
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
        if username == "admin" and password == "hr2026":
            st.session_state['logged_in'] = True
            st.success("تم التحقق من الصلاحية الأمنية بنجاح! جاري تحميل النظام...")
            st.rerun()
        else:
            st.error("بيانات الدخول غير صحيحة! (استخدم admin و hr2026 للتجربة)")
    st.stop()

# ==========================================
# 3. قاموس المصطلحات لتدعيم اللغتين
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
    'Sentiment': ["Negative", "Positive", "Positive", "Neutral", "Neutral"]
})

df = mock_data_ar if lang == "ar" else mock_data_en

# ==========================================
# 4. محتوى الصفحات
# ==========================================
if page == text[lang]["home"]:
    st.title(text[lang]["title"])
    st.subheader(text[lang]["subtitle"])
    st.markdown("---")
    
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
