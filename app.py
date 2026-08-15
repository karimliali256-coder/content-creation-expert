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

# ULTRA-PREMIUM MODERN UI CSS
st.markdown(
    """
    <style>
    /* Bütün Səhifə Arxa Fonu */
    .stApp {
        background-color: #FAFAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", "Segoe UI", Roboto, sans-serif !important;
    }

    /* Streamlit standart elementləri təmizləmək */
    header, footer, [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 7rem !important;
        max-width: 760px !important;
    }

    /* Başlıq Dizaynı */
    .app-header {
        text-align: center;
        margin-bottom: 25px;
    }
    .app-header h1 {
        font-size: 2rem;
        font-weight: 700;
        color: #0B192C;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .app-header p {
        font-size: 0.9rem;
        color: #64748B;
    }

    /* Avatar İkonlarını Tam Gizlət */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* Ümumi Chat Mesaj Container-i */
    [data-testid="stChatMessage"] {
        background: transparent !important;
        border: none !important;
        padding: 4px 0px !important;
        margin-bottom: 12px !important;
        display: flex !important;
        box-shadow: none !important;
    }

    /* İstifadəçi Mesajı: Sağa Yönlü, Tünd Navy Blue */
    [data-testid="stChatMessage"]:nth-child(odd) {
        justify-content: flex-end !important;
    }
    [data-testid="stChatMessage"]:nth-child(odd) [data-testid="stChatMessageContent"] {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border-radius: 20px 20px 4px 20px !important;
        padding: 12px 18px !important;
        max-width: 80% !important;
        box-shadow: 0 4px 14px rgba(11, 25, 44, 0.12) !important;
    }

    /* AI Chatbot Mesajı: Sola Yönlü, Zəngin Boz */
    [data-testid="stChatMessage"]:nth-child(even) {
        justify-content: flex-start !important;
    }
    [data-testid="stChatMessage"]:nth-child(even) [data-testid="stChatMessageContent"] {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
        border-radius: 20px 20px 20px 4px !important;
        padding: 14px 20px !important;
        max-width: 85% !important;
        border: 1px solid #E2E8F0 !important;
    }

    /* Input Sahəsini Ekranın Altında Sabitləmək vən Pill Şəklinə Salmaq */
    .stChatInputContainer {
        border-radius: 35px !important;
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.05) !important;
        padding: 3px 8px !important;
    }
    .stChatInputContainer:focus-within {
        border-color: #0B192C !important;
        box-shadow: 0 10px 25px rgba(11, 25, 44, 0.1) !important;
    }

    /* Popover (+) Düyməsi */
    [data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 38px !important;
        height: 38px !important;
        background-color: #F1F5F9 !important;
        color: #0B192C !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: 600 !important;
    }
    [data-testid="stPopover"] > button:hover {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
    }

    /* Send Button */
    button[aria-label="Send message"] {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
    }

    /* TXT Export Düyməsi */
    .stDownloadButton > button {
        border-radius: 20px !important;
        background-color: #FFFFFF !important;
        color: #0B192C !important;
        border: 1px solid #E2E8F0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        padding: 6px 16px !important;
    }
    .stDownloadButton > button:hover {
        border-color: #0B192C !important;
        background-color: #F8FAFC !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="app-header">
        <h1>Viral Creator AI</h1>
        <p>Shorts, Reels & TikTok Analitika Asistenti</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sidebar
with st.sidebar:
  st.title("⚙️ Tənzimləmələr")
  api_key = st.text_input("Google AI Studio API Key:", type="password")
  st.markdown("---")
  platform = st.selectbox(
      "Platforma seçin:", ["General", "TikTok", "Instagram Reels", "YouTube Shorts"]
  )

SYSTEM_INSTRUCTION = """
Sən TikTok, Instagram Reels və YouTube Shorts üzrə ekspert və multimodal sosial media köməkçisisən.

İŞ REJİMLƏRİ:
1. PLATFORMA ADAPTASİYASI: Verilən cavabları seçilmiş platformaya uyğunlaşdır.
2. DƏRİN RESEARCH REJİMİ: Mövzunu alqoritmik və psixoloji baxımdan dərindən analiz et.
3. BRAINSTORM REJİMİ: 5 fərqli viral konsept və bucaq təklif et.
4. A/B TEST GENERATORU: 3 fərqli vizual hook və başlanğıc cümləsi hazırla.
5. VIRAL FAİZİ: Soruşulsa İLK SƏTİRDƏ "📊 VIRAL EHTİMAL: [X]%" göstər.
6. SEO & HASHTAGS: 📌 Description, 🏷️ Hashtags, 💬 Call to Action yaz.
"""

if api_key:
  genai.configure(api_key=api_key)
  model = genai.GenerativeModel(
      model_name="gemini-3.6-flash", system_instruction=SYSTEM_INSTRUCTION
  )

  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Mesajların Göstərilməsi
  for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # Bottom Controls
  col_plus, col_input = st.columns([1, 8])

  uploaded_file = None
  action_type = "Standard"

  with col_plus:
    with st.popover("＋", help="Alətlər vən Media"):
      st.markdown("**🛠️ Rejimlər:**")
      action_type = st.radio(
          "İş rejimini seçin:",
          [
              "Standard",
              "🔍 Dərin Research",
              "💡 Brainstorm",
              "🧪 A/B Test Generator",
          ],
          label_visibility="collapsed",
      )
      st.markdown("---")
      st.markdown("**📎 Media Yüklə:**")
      uploaded_file = st.file_uploader(
          "Fayl seçin:",
          type=["jpg", "jpeg", "png", "mp4", "mov"],
          label_visibility="collapsed",
      )

  with col_input:
    user_input = st.chat_input("Mesaj yazın...")

  if uploaded_file:
    st.toast(f"📎 Fayl seçildi: {uploaded_file.name}", icon="✅")

  if user_input or uploaded_file:
    content_parts = []
    prefix_prompt = f"[PLATFORMA: {platform}] "

    if action_type == "🔍 Dərin Research":
      prefix_prompt += "[REJİM: DƏRİN RESEARCH] "
    elif action_type == "💡 Brainstorm":
      prefix_prompt += "[REJİM: BRAINSTORM] "
    elif action_type == "🧪 A/B Test Generator":
      prefix_prompt += "[REJİM: A/B TEST GENERATORU] "

    if uploaded_file:
      with tempfile.NamedTemporaryFile(
          delete=False, suffix=uploaded_file.name
      ) as tmp:
        tmp.write(uploaded_file.getvalue())
        tmp_path = tmp.name

      with st.spinner("Media emal olunur..."):
        media_file = genai.upload_file(tmp_path)
        while media_file.state.name == "PROCESSING":
          time.sleep(1.5)
          media_file = genai.get_file(media_file.name)

      content_parts.append(media_file)

    if user_input:
      content_parts.append(prefix_prompt + user_input)

    display_text = user_input or f"[{action_type} - Media faylı]"
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
      st.markdown(display_text)

    with st.chat_message("assistant"):
      with st.spinner("Cavab hazırlanır..."):
        try:
          response = model.generate_content(content_parts)
          st.markdown(response.text)
          st.session_state.messages.append(
              {"role": "assistant", "content": response.text}
          )
        except Exception as e:
          if "429" in str(e):
            st.error("⚠️ API limiti aşıldı! 1 dəqiqə gözləyin.")
          else:
            st.error(f"Xəta: {e}")

  if st.session_state.messages:
    chat_export_text = "\n\n".join(
        [f"{m['role'].upper()}: {m['content']}" for m in st.session_state.messages]
    )
    st.download_button(
        label="📥 Söhbəti TXT Kimi Yüklə",
        data=chat_export_text,
        file_name="viral_agent_export.txt",
        mime="text/plain",
    )
else:
  st.warning("Sol paneldən API Key daxil edin.")
