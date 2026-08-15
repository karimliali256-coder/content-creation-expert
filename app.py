import tempfile
import time
import google.generativeai as genai
import streamlit as st

# 1. Streamlit Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="Viral Creator AI | Gemini UI",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# 2. Custom CSS: Həm Mobildə, Həm Kompüterdə Gemini Chat UI Dizaynı, Rənglər və API Xəbərdarlığı
st.markdown(
    """
    <style>
    /* Bütün səhifə üçün təmiz ağ fon */
    .stApp {
        background-color: #FFFFFF !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Başlıq sahəsi */
    .main-header {
        text-align: center;
        padding: 30px 0 20px 0;
    }
    .main-header h1 {
        color: #0A192F !important; /* Navy Blue */
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #64748B;
        font-size: 0.95rem;
    }

    /* --- API Xəbərdarlığı Dizaynı (Sarı-Ağ yox, Tünd Mavi-Ağ) --- */
    [data-testid="stWarning"] {
        background-color: #0A192F !important; /* Navy Blue fon */
        color: #FFFFFF !important; /* Ağ mətn */
        border: 1px solid #DADCE0;
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 1rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    [data-testid="stWarning"] .stAlertContent {
        color: #FFFFFF !important; /* Mətnin daxili rəngini də ağ et */
    }

    /* --- Çat Mesajları Dizaynı (Mobildə və Kompüterdə Eyni Gemini Style) --- */
    [data-testid="stChatMessage"] {
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
        border-radius: 20px !important;
        max-width: 80% !important; /* Mobildə daha dar etmək üçün */
    }

    /* İstifadəçi Mesajı (Zəngin Mavi) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) {
        background-color: #1A73E8 !important; /* Rich Blue */
        color: #FFFFFF !important;
        margin-left: auto !important; /* Sağ tərəfə söykə */
        border-bottom-right-radius: 5px !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) .stAlertContent {
        color: #FFFFFF !important;
    }

    /* Çatbot (Gemini) Mesajı (Boz) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")) {
        background-color: #F0F2F5 !important; /* Gray fon */
        color: #1F1F1F !important; /* Qara mətn */
        margin-right: auto !important; /* Sol tərəfə söykə */
        border-bottom-left-radius: 5px !important;
    }
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")) .stAlertContent {
        color: #1F1F1F !important;
    }

    /* Avatar simgələrini gizlət (Həm mobildə, həm kompüterdə təmiz görünüş üçün) */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* --- Aşağı Giriş Sahəsi Dizaynı (Düzgün Hizalanma və Rənglər) --- */
    /* Çat giriş sütunu layout */
    [data-testid="stChatInput"] {
        background-color: transparent !important; /* Fonu təmizlə */
        border: none !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
    }

    /* Giriş mətn qutusu (Oval və Ağ) */
    [data-testid="stChatInput"] input {
        background-color: #FFFFFF !important; /* Ağ fon */
        border: 1px solid #DADCE0 !important;
        border-radius: 28px !important;
        padding: 10px 15px !important;
        color: #1F1F1F !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Göndər düyməsi (Tünd Navy Blue) */
    [data-testid="stChatInputSubmitBtn"] {
        background-color: #0A192F !important; /* Navy Blue fon */
        color: #FFFFFF !important; /* Ağ ok */
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        top: auto !important;
        bottom: 5px !important;
        right: 5px !important;
    }

    /* '+' Düyməsi (Fayl yükləmək üçün, sol sütunda, boz oval) */
    .file-upload-plus {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 45px;
        height: 45px;
        background-color: #F0F2F5; /* Boz fon */
        color: #0A192F; /* Navy Blue '+' */
        border: 1px solid #DADCE0;
        border-radius: 50%;
        cursor: pointer;
        font-size: 24px;
        text-decoration: none;
        box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        margin-right: 10px;
    }

    /* Media elementlərinin künclərini oval et */
    img, video { border-radius: 12px !important; }
    footer { visibility: hidden; }
    </style>
""",
    unsafe_allow_html=True,
)

# 3. İnterfeys Başlığı
st.markdown(
    """
    <div class="main-header">
        <h1>🚀 Viral Creator AI</h1>
        <p>Shorts, Reels & TikTok üçün Gemini v3.6 Analitika Asistenti</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sol panel: API Key Girişi (Məxfi saxlamaq üçün sidebar-da qalsın)
with st.sidebar:
  st.title("⚙️ Tənzimləmələr")
  st.markdown("Tətbiqi işlətmək üçün Google AI Studio API Keyinizi daxil edin.")
  api_key = st.text_input("API Key:", type="password")

# 4. AI Sistem Təlimatı
SYSTEM_INSTRUCTION = """
Sən TikTok, Instagram Reels və YouTube Shorts alqoritmləri üzrə baş ekspert, canlı trend analitiki və multimodal sosial media köməkçisisən.

Rejim qaydaları:
1. Brainstorm: İstifadəçi ideya istədikdə 3 ədəd trendə uyğun, yüksək retention ehtimallı video konsepti təqdim et.
2. Deep Research: Mövzunu və ya medianı alqoritmik, psixoloji və vizual baxımdan addım-addım dərin analiz et.
3. A/B Test Generator: Eyni video üçün 2 fərqli Hook (ilk 3 saniyə), 2 fərqli Başlıq (Caption) və CTA versiyası yaradaraq A və B variantları kimi müqayisəli təqdim et.
"""

if api_key:
  genai.configure(api_key=api_key)

  # 5. Gemini v3.6 Flash Modeli və Canlı Web Research
  model = genai.GenerativeModel(
      model_name="gemini-3.6-flash",
      system_instruction=SYSTEM_INSTRUCTION,
      tools=["google_search_retrieval"],
  )

  # Sesiyaların yadda saxlanması
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Keçmiş mesajların ekranda göstərilməsi
  for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # 6. Giriş Sahəsi Layout: '+' Düyməsi və Mətn Girişi (Düzgün Hizalama)
  input_col1, input_col2 = st.columns([1, 8])

  with input_col1:
    # Fayl yükləmək üçün '+' düyməsini oval və boz etmək
    uploaded_file = st.file_uploader("", type=["jpg", "jpeg", "png", "mp4", "mov"], label_visibility="collapsed")
    st.markdown('<label for="file_uploader" class="file-upload-plus">+</label>', unsafe_allow_html=True)

  with input_col2:
    # AĞ rəngdə çat input, GÖNDƏR düyməsi NAVY rəngdə
    user_input = st.chat_input("Fikir yazın və ya 'Dərin analiz et' deyin...")

  # Göndərmə prosesi
  if user_input or uploaded_file:
    content_parts = []

    if uploaded_file:
      with tempfile.NamedTemporaryFile(
          delete=False, suffix=uploaded_file.name
      ) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

      with st.spinner("Media emal olunur..."):
        media_file = genai.upload_file(tmp_path)
        while media_file.state.name == "PROCESSING":
          time.sleep(1)
          media_file = genai.get_file(media_file.name)

      content_parts.append(media_file)

    if user_input:
        prompt_text = user_input
    else:
        prompt_text = "Bu faylı analiz et."
    content_parts.append(prompt_text)

    # İstifadəçi mesajını yaddaşa yazmaq və göstərmək (ZƏNGİN MAVİ, sağda, oval)
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
      st.markdown(prompt_text)

    # AI Cavabının hazırlanması və göstərilməsi (BOZ, solda, oval)
    with st.chat_message("assistant"):
      with st.spinner("Viral Agent cavab hazırlayır..."):
        try:
          response = model.generate_content(content_parts)
          st.markdown(response.text)
          st.session_state.messages.append(
              {"role": "assistant", "content": response.text}
          )
        except Exception as e:
          st.error(f"Xəta baş verdi: {e}")
else:
    # --- DÜZƏLİŞ: API Xəbərdarlığı İndi Tam Oxunaqlıdır (Mobildə və Kompüterdə) ---
    st.warning("🚀 Tətbiqi işlətmək üçün zəhmət olmasa sol paneldən (Settings) API Key daxil edin.")
