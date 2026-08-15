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

# MOBILE-FRIENDLY RESPONSIVE CSS
st.markdown(
    """
    <style>
    /* Bütün Səhifə */
    .stApp {
        background-color: #FAFAFC !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    }

    /* Gizlədilən standart Streamlit elementləri */
    header, footer, [data-testid="stHeader"] {
        visibility: hidden !important;
        height: 0px !important;
    }

    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 7rem !important;
        padding-left: 0.8rem !important;
        padding-right: 0.8rem !important;
        max-width: 100% !important;
    }

    /* Başlıq */
    .app-header {
        text-align: center;
        margin-bottom: 20px;
    }
    .app-header h1 {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0B192C;
        margin-bottom: 2px;
    }
    .app-header p {
        font-size: 0.85rem;
        color: #64748B;
    }

    /* MESAJ KUTULARI (MOBİL UYGUN) */
    .user-bubble-container {
        display: flex;
        justify-content: flex-end;
        margin-bottom: 12px;
        width: 100%;
    }
    .user-bubble {
        background-color: #0B192C;
        color: #FFFFFF;
        border-radius: 18px 18px 2px 18px;
        padding: 10px 16px;
        max-width: 85%;
        font-size: 0.92rem;
        line-height: 1.4;
        word-wrap: break-word;
    }

    .ai-bubble-container {
        display: flex;
        justify-content: flex-start;
        margin-bottom: 14px;
        width: 100%;
    }
    .ai-bubble {
        background-color: #F1F5F9;
        color: #0F172A;
        border: 1px solid #E2E8F0;
        border-radius: 18px 18px 18px 2px;
        padding: 12px 16px;
        max-width: 90%;
        font-size: 0.92rem;
        line-height: 1.5;
        word-wrap: break-word;
    }

    /* MOBİL CHAT İNPUT VƏ POPOVER DÜZƏLİŞİ */
    div[data-testid="stChatInput"] {
        border-radius: 28px !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important;
    }
    
    /* Standart ChatMessage Elementlərini Gizlət */
    [data-testid="stChatMessage"] {
        display: none !important;
    }

    /* Telefonda Sütunların Üst-Üstə Düşməsini Önlemek */
    @media (max-width: 768px) {
        .block-container {
            padding-bottom: 8rem !important;
        }
        .user-bubble, .ai-bubble {
            max-width: 92% !important;
        }
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

# Sidebar (API Key və Ayarlar)
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

  # MESAJLARIN RENDER EDİLMƏSİ
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

  # Mobil Uyğun Alət və Yükləmə Menyusu
  with st.expander("🛠️ Rejimlər və Fayl Yüklə", expanded=False):
    action_type = st.radio(
        "Rejim:",
        ["Standard", "🔍 Dərin Research", "💡 Brainstorm", "🧪 A/B Test Generator"],
        horizontal=True,
    )
    uploaded_file = st.file_uploader(
        "Media yüklə:", type=["jpg", "jpeg", "png", "mp4", "mov"]
    )

  # Əsas Chat Paneli
  user_input = st.chat_input("Mesaj yazın...")

  if uploaded_file:
    st.toast(f"📎 Fayl seçildi: {uploaded_file.name}", icon="✅")

  if user_input or (
      'uploaded_file' in locals() and uploaded_file is not None
  ):
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
    st.markdown(
        f'<div class="user-bubble-container"><div'
        f' class="user-bubble">{display_text}</div></div>',
        unsafe_allow_html=True,
    )

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
  st.warning("Sol paneldən (Sidebar) API Key daxil edin.")
