import tempfile
import time
import google.generativeai as genai
import streamlit as st

# Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="Viral Creator AI",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# SƏDƏ VƏ MOBİL UYĞUN CSS
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FAFAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }
    header, footer, [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 6rem !important;
        max-width: 100% !important;
    }
    .app-header {
        text-align: center;
        margin-bottom: 15px;
    }
    .app-header h1 {
        font-size: 1.8rem;
        font-weight: 800;
        color: #0B192C;
        margin-bottom: 2px;
    }
    .app-header p {
        font-size: 0.85rem;
        color: #64748B;
    }
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 10px;
    }
    .user-bubble {
        background-color: #0B192C;
        color: #FFFFFF;
        border-radius: 16px 16px 2px 16px;
        padding: 10px 14px;
        max-width: 85%;
        font-size: 0.95rem;
    }
    .ai-bubble-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 12px;
    }
    .ai-bubble {
        background-color: #F1F5F9;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 16px 16px 16px 2px;
        padding: 12px 15px;
        max-width: 90%;
        font-size: 0.95rem;
    }
    [data-testid="stChatMessage"] {
        display: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Başlıq
st.markdown(
    """
    <div class="app-header">
        <h1>🚀 Viral Creator AI</h1>
        <p>Shorts, Reels & TikTok Analitika Asistenti</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Ana Ekran Ayarları (Telefonda İtməməsi Üçün Birbaşa Yuxarıda)
with st.expander("🔑 API Key və Tənzimləmələr", expanded=True):
  api_key = st.text_input(
      "Google AI Studio API Key:", type="password", placeholder="AIzaSy..."
  )
  col_a, col_b = st.columns(2)
  with col_a:
    platform = st.selectbox(
        "Platforma:", ["General", "TikTok", "Instagram Reels", "YouTube Shorts"]
    )
  with col_b:
    action_type = st.selectbox(
        "Rejim:",
        [
            "Standard",
            "🔍 Dərin Research",
            "💡 Brainstorm",
            "🧪 A/B Test Generator",
        ],
    )
  uploaded_file = st.file_uploader(
      "Media Yüklə (Şəkil/Video):", type=["jpg", "jpeg", "png", "mp4", "mov"]
  )

SYSTEM_INSTRUCTION = """
Sən TikTok, Instagram Reels və YouTube Shorts üzrə ekspert və multimodal sosial media köməkçisisən.
1. PLATFORMA ADAPTASİYASI: Cavabları seçilmiş platformaya uyğunlaşdır.
2. DƏRİN RESEARCH REJİMİ: Mövzunu alqoritmik və psixoloji dərindən analiz et.
3. BRAINSTORM REJİMİ: 5 fərqli viral konsept və bucaq təklif et.
4. A/B TEST GENERATORU: 3 fərqli vizual hook və başlanğıc cümləsi hazırla.
"""

if "messages" not in st.session_state:
  st.session_state.messages = []

# Keçmiş Mesajları Göstər
for msg in st.session_state.messages:
  if msg["role"] == "user":
    st.markdown(
        f'<div class="user-bubble-container"><div'
        f' class="user-bubble">{msg["content"]}</div></div>',
        unsafe_allow_html=True,
    )
  else:
    st.markdown(
        f'<div class="ai-bubble-container"><div'
        f' class="ai-bubble">{msg["content"]}</div></div>',
        unsafe_allow_html=True,
    )

# Mesaj Daxil Etmə Paneli (HƏMİŞƏ EKRANDA GÖRÜNÜR)
user_input = st.chat_input("Mesajınızı bura yazın...")

if user_input or uploaded_file:
  if not api_key:
    st.error(
        "⚠️ Xahiş olunur yuxarıdakı '🔑 API Key və Tənzimləmələr' bölməsindən"
        " API Key daxil edin!"
    )
  else:
    try:
      genai.configure(api_key=api_key)
      model = genai.GenerativeModel(
          model_name="gemini-3.6-flash", system_instruction=SYSTEM_INSTRUCTION
      )

      content_parts = []
      prefix_prompt = f"[PLATFORMA: {platform}] [REJİM: {action_type}] "

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
        content_parts.append(prefix_prompt + user_input)

      display_text = user_input or f"[{action_type} - Media faylı]"

      # İstifadəçi mesajını elə həmin an ekrana vur
      st.session_state.messages.append(
          {"role": "user", "content": display_text}
      )

      with st.spinner("Cavab hazırlanır..."):
        response = model.generate_content(content_parts)
        ai_response_text = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response_text}
        )
        st.rerun()

    except Exception as e:
      if "429" in str(e):
        st.error("⚠️ API limiti aşıldı! 1 dəqiqə gözləyin.")
      else:
        st.error(f"Xəta baş verdi: {e}")
else:
  st.warning("Sol paneldən (Sidebar) API Key daxil edin.")
