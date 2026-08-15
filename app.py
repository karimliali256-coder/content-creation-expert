import tempfile
import time
import google.generativeai as genai
import streamlit as st

# Səhifə Tənzimləmələri
st.set_page_config(
    page_title="Viral Creator AI",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# ULTRA-CLEAN CUSTOM UI CSS
st.markdown(
    """
    <style>
    /* Bütün Səhifə Arxa Fonu */
    .stApp {
        background-color: #FAFAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Streamlit Standart Header/Footer Təmizliyi */
    header, footer, [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }

    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 6rem !important;
        max-width: 780px !important;
    }

    /* Başlıq */
    .app-header {
        text-align: center;
        margin-bottom: 30px;
    }
    .app-header h1 {
        font-size: 2.1rem;
        font-weight: 800;
        color: #0B192C;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .app-header p {
        font-size: 0.95rem;
        color: #64748B;
    }

    /* XÜSUSİ MESAJ KUTULARI (CUSTOM BUBBLES) */
    
    /* User Bubble - Sağa Yönlü, Navy Blue */
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 14px;
        width: 100%;
    }
    .user-bubble {
        background-color: #0B192C;
        color: #FFFFFF;
        border-radius: 20px 20px 4px 20px;
        padding: 12px 20px;
        max-width: 80%;
        font-size: 0.98rem;
        line-height: 1.5;
        box-shadow: 0 4px 12px rgba(11, 25, 44, 0.12);
    }

    /* AI Bubble - Sola Yönlü, Zəngin Boz */
    .ai-bubble-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 18px;
        width: 100%;
    }
    .ai-bubble {
        background-color: #F1F5F9;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 20px 20px 20px 4px;
        padding: 16px 22px;
        max-width: 88%;
        font-size: 0.98rem;
        line-height: 1.6;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    /* Input Bar və Popover Kontrolu */
    div[data-testid="stChatInput"] {
        border-radius: 35px !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06) !important;
        padding: 2px 6px !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #0B192C !important;
    }

    /* Popover (+) Düyməsi */
    [data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
        background-color: #F1F5F9 !important;
        color: #0B192C !important;
        border: none !important;
        font-size: 18px !important;
        font-weight: bold !important;
    }
    [data-testid="stPopover"] > button:hover {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
    }

    /* Standart ChatMessage Elementlərini Tam Gizlət */
    [data-testid="stChatMessage"] {
        display: none !important;
    }

    button[aria-label="Send message"] {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# Header
st.markdown(
    """
    <div class="app-header">
        <h1>🚀 Viral Creator AI</h1>
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
      model_name="gemini-2.0-flash", system_instruction=SYSTEM_INSTRUCTION
  )

  if "messages" not in st.session_state:
    st.session_state.messages = []

  # MESAJLARIN XÜSUSİ HTML İLƏ RENDER EDİLMƏSİ
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

  # Əsas İnput Paneli
  col_plus, col_input = st.columns([1, 8])

  uploaded_file = None
  action_type = "Standard"

  with col_plus:
    with st.popover("＋", help="Alətlər və Media"):
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

    # User mesajını ekrana çıxar və yaddaşa yaz
    st.session_state.messages.append({"role": "user", "content": display_text})
    st.markdown(
        f'<div class="user-bubble-container"><div'
        f' class="user-bubble">{display_text}</div></div>',
        unsafe_allow_html=True,
    )

    # AI Cavabı
    with st.spinner("Cavab hazırlanır..."):
      try:
        response = model.generate_content(content_parts)
        ai_response_text = response.text

        st.session_state.messages.append(
            {"role": "assistant", "content": ai_response_text}
        )
        st.markdown(
            f'<div class="ai-bubble-container"><div'
            f' class="ai-bubble">{ai_response_text}</div></div>',
            unsafe_allow_html=True,
        )
        st.rerun()
      except Exception as e:
        if "429" in str(e):
          st.error("⚠️ API limiti aşıldı! 1 dəqiqə gözləyin.")
        else:
          st.error(f"Xəta: {e}")

  if st.session_state.messages:
    st.markdown("---")
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
