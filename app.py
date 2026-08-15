import io
import tempfile
import time
import google.generativeai as genai
import streamlit as st

# Səhifə Tənzimləmələri
st.set_page_config(
    page_title="Viral Creator AI Agent",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS: Dərin Navy Blue, Zəngin Boz və Saf Ağ
st.markdown(
    """
    <style>
    /* Ümumi Arxa Fon və Şrift */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Animasiyalar */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(12px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    /* Başlıq İnterfeysi */
    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
        animation: fadeInUp 0.4s ease-out;
    }
    .main-header h1 {
        color: #0B192C;
        font-size: 2.2rem;
        font-weight: 800;
        letter-spacing: -0.5px;
        margin-bottom: 4px;
    }
    .main-header p {
        color: #64748B;
        font-size: 0.95rem;
        font-weight: 500;
    }

    /* Çat Mesaj Qutuları */
    [data-testid="stChatMessage"] {
        border-radius: 24px !important;
        padding: 16px 22px !important;
        margin-bottom: 14px !important;
        animation: fadeInUp 0.3s ease-out !important;
    }

    /* AI Chatbot Mesajı - Zəngin Premium Boz */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")),
    div[data-testid="stChatMessage"]:nth-child(even) {
        background-color: #E2E8F0 !important;
        color: #0F172A !important;
        border: 1px solid #CBD5E1 !important;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.03) !important;
    }

    /* İstifadəçi Mesajı - Dərin Navy Blue */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")),
    div[data-testid="stChatMessage"]:nth-child(odd) {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border: none !important;
        box-shadow: 0 6px 18px rgba(11, 25, 44, 0.18) !important;
    }

    /* Oval Floating Chat Input Qutusu */
    div[data-testid="stChatInput"] {
        border-radius: 40px !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #CBD5E1 !important;
        box-shadow: 0 10px 30px rgba(11, 25, 44, 0.08) !important;
        padding: 4px 8px !important;
    }
    div[data-testid="stChatInput"]:focus-within {
        border-color: #0B192C !important;
    }

    /* Popover (+) Düyməsi Style */
    [data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 42px !important;
        height: 42px !important;
        background-color: #F1F5F9 !important;
        color: #0B192C !important;
        border: 1px solid #CBD5E1 !important;
        font-size: 20px !important;
        font-weight: bold !important;
        transition: all 0.2s ease !important;
    }
    [data-testid="stPopover"] > button:hover {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        transform: scale(1.05);
    }

    /* Göndərmə Düyməsi - Navy Blue */
    button[aria-label="Send message"] {
        background-color: #0B192C !important;
        color: #FFFFFF !important;
        border-radius: 50% !important;
    }

    /* Media və Yükləmə Elementləri */
    img, video {
        border-radius: 16px !important;
    }
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# Başlıq
st.markdown(
    """
    <div class="main-header">
        <h1>🚀 Viral Creator AI Agent</h1>
        <p>TikTok, Reels və Shorts üçün Multimodal Kontent Köməkçisi</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sol Panel: API, Platforma Seçimi və Yükləmə
with st.sidebar:
  st.title("⚙️ Tənzimləmələr")
  api_key = st.text_input("Google AI Studio API Key:", type="password")

  st.markdown("---")
  st.markdown("**🎯 Platforma Adaptasiyası:**")
  platform = st.selectbox(
      "Platforma seçin:", ["General", "TikTok", "Instagram Reels", "YouTube Shorts"]
  )

SYSTEM_INSTRUCTION = """
Sən TikTok, Instagram Reels və YouTube Shorts alqoritmləri üzrə baş ekspert, canlı trend analitiki və multimodal sosial media köməkçisisən.

İŞ REJİMLƏRİ VƏ QAYDALAR:
1. PLATFORMA ADAPTASİYASI: Verilən cavabları seçilmiş platformaya (TikTok, Reels və ya Shorts) xüsusi alqoritmik qaydalara uyğunlaşdır.
2. DƏRİN RESEARCH REJİMİ: Mövzunu və ya media faylını alqoritmik (retention rate), psixoloji təsir (viewer trigger) və kadr ritmi baxımından dərindən araşdır.
3. BRAINSTORM REJİMİ: Təqdim olunan mövzu üçün 5 fərqli viral konsept və fərqli bucaqlardan ideyalar təklif et.
4. A/B TEST İDEYA GENERATORU: Eyni kontent üçün 3 fərqli vizual hook və 3 fərqli başlanğıc cümləsi yaradaraq A/B test variantları təqdim et.
5. VIRAL FAİZİ: Əgər istifadəçi viral ehtimalını soruşarsa, cavabın İLK SƏTİRİNDƏ "📊 VIRAL EHTİMAL: [X]%" formatında göstər.
6. SEO & HASHTAGS: "Təsvir yaz" dedikdə 📌 Description, 🏷️ Hashtags (3 broad + 3 niche), 💬 Call to Action (CTA) çıxar.
"""

if api_key:
  genai.configure(api_key=api_key)

  # Gemini 2.0 Flash Modeli
  model = genai.GenerativeModel(
      model_name="gemini-2.0-flash",
      system_instruction=SYSTEM_INSTRUCTION,
  )

  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Keçmiş Mesajların Göstərilməsi
  for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # İnput Zonası: Popover (+) + Chat Input
  col_plus, col_input = st.columns([1, 8])

  uploaded_file = None
  action_type = "Standard"

  with col_plus:
    with st.popover("➕", help="Aətlər və Media"):
      st.markdown("**🛠️ Alətlər və Rejimlər:**")
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
    st.toast(f"📎 Fayl əlavə edildi: {uploaded_file.name}", icon="✅")

  # Göndərmə Prosesi
  if user_input or uploaded_file:
    content_parts = []

    # Rejim və Platforma prefiksi
    prefix_prompt = f"[PLATFORMA: {platform}] "
    if action_type == "🔍 Dərin Research":
      prefix_prompt += "[REJİM: DƏRİN RESEARCH] Mövzunu və ya media faylını alqoritmik və psixoloji baxımdan dərindən analiz et: "
    elif action_type == "💡 Brainstorm":
      prefix_prompt += "[REJİM: BRAINSTORM] Bu mövzu üçün 5 müxtəlif viral konsept və bucaqlar təklif et: "
    elif action_type == "🧪 A/B Test Generator":
      prefix_prompt += "[REJİM: A/B TEST GENERATORU] Bu kontent üçün 3 fərqli vizual hook və 3 fərqli başlanğıc cümləsi ilə A/B test variantları hazırla: "

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

    display_text = user_input or f"[{action_type} - Media analiz edilir]"
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
      st.markdown(display_text)

    with st.chat_message("assistant"):
      with st.spinner("Viral Agent cavab hazırlayır..."):
        try:
          response = model.generate_content(content_parts)
          st.markdown(response.text)
          st.session_state.messages.append(
              {"role": "assistant", "content": response.text}
          )
        except Exception as e:
          if "429" in str(e):
            st.error(
                "⚠️ API limiti aşıldı! 1 dəqiqə gözləyin və ya sol paneldən yeni"
                " API Key daxil edin."
            )
          else:
            st.error(f"Xəta baş verdi: {e}")

  # TXT İxracı (Söhbət Yaddaşını Yükləmə Düyməsi)
  if st.session_state.messages:
    st.markdown("---")
    chat_export_text = ""
    for m in st.session_state.messages:
      role = "İstifadəçi" if m["role"] == "user" else "Viral AI Agent"
      chat_export_text += f"{role}:\n{m['content']}\n\n" + "-" * 40 + "\n\n"

    st.download_button(
        label="📥 Söhbəti TXT Faylı Kimi Yüklə",
        data=chat_export_text,
        file_name="viral_agent_analysis.txt",
        mime="text/plain",
    )
else:
  st.warning("Zəhmət olmasa sol paneldən API Key daxil edin.")
