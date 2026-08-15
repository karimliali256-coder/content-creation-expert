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

# 2. Custom CSS: Gemini Chat UI Dizaynı, Rənglər və Animasiya
st.markdown(
    """
    <style>
    /* Bütün səhifə üçün təmiz ağ fon */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Giriş Animasiyası (Yüngül Motion) */
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(15px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Başlıq sahəsi */
    .main-header {
        text-align: center;
        padding: 30px 0 20px 0;
        animation: slideUp 0.5s ease-out;
    }
    .main-header h1 {
        color: #0A192F; /* Navy Blue */
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #64748B;
        font-size: 0.95rem;
    }

    /* --- Çat Mesajları Dizaynı (Gemini Style) --- */
    [data-testid="stChatMessage"] {
        animation: slideUp 0.3s ease-out !important;
        padding: 1rem !important;
        margin-bottom: 0.8rem !important;
        border-radius: 20px !important;
        max-width: 85% !important;
    }

    /* İstifadəçi Mesajı (Zəngin Mavi) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) {
        background-color: #1A73E8 !important; /* Rich Blue */
        color: #FFFFFF !important;
        margin-left: auto !important; /* Sağ tərəfə söykə */
        border-bottom-right-radius: 5px !important;
    }

    /* Çatbot (Gemini) Mesajı (Boz) */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")) {
        background-color: #F0F2F5 !important; /* Gray */
        color: #1F1F1F !important;
        margin-right: auto !important; /* Sol tərəfə söykə */
        border-bottom-left-radius: 5px !important;
    }

    /* Avatar simgələrini gizlət (Tam təmiz görünüş üçün) */
    [data-testid="stChatMessageAvatar"] {
        display: none !important;
    }

    /* --- Aşağı Giriş Sahəsi Dizaynı --- */
    /* Çat giriş sahəsi (Ağ) */
    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #DADCE0 !important;
        border-radius: 28px !important;
        padding-left: 15px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1) !important;
    }

    /* Göndər düyməsi (Navy Blue) */
    [data-testid="stChatInputSubmitBtn"] {
        background-color: #0A192F !important; /* Navy Blue */
        color: #FFFFFF !important;
        border-radius: 50% !important;
        width: 40px !important;
        height: 40px !important;
    }

    /* '+' Popover Düyməsi Style */
    [data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 45px !important;
        height: 45px !important;
        background-color: #F0F2F5 !important; /* Boz fon */
        color: #0A192F !important; /* Navy Blue icon */
        border: 1px solid #DADCE0 !important;
        font-size: 22px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: transform 0.2s ease !important;
    }
    [data-testid="stPopover"] > button:hover {
        background-color: #E8EAED !important;
        transform: scale(1.05);
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

# Sol panel: API Key Girişi
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

  # 6. Giriş Sahəsi Layout: '+' Düyməsi və Mətn Girişi
  input_col1, input_col2 = st.columns([1, 8])

  action_prompt = None
  uploaded_file = None

  with input_col1:
    with st.popover("➕", help="Funksiyalar və Media"):
      st.markdown("**Ağıllı Rejimlər:**")
      if st.button("💡 Brainstorm et", use_container_width=True):
        action_prompt = "Mənim üçün bu mövzuda 3 viral video ideyası brainstorm et:"
      if st.button("🔍 Deep Research", use_container_width=True):
        action_prompt = "Aşağıdakı mövzunu və ya faylı alqoritmik və psixoloji baxımdan dərin analiz (Deep Research) et:"
      if st.button("🅰️/🅱️ A/B Test Generator", use_container_width=True):
        action_prompt = "Bu mövzu/video üçün 2 fərqli Hook və Başlıq variantı ilə A/B Test ssenarisi hazırla:"

      st.divider()
      uploaded_file = st.file_uploader(
          "📎 Fayl əlavə et:",
          type=["jpg", "jpeg", "png", "mp4", "mov"],
          label_visibility="visible",
      )

  with input_col2:
    # AĞ rəngdə çat input, GÖNDƏR düyməsi NAVY rəngdə
    user_input = st.chat_input("Fikir yazın və ya 'Dərin analiz et' deyin...")

  # Hansı girişin istifadə edildiyini müəyyən etmək
  final_input = user_input
  if action_prompt and not user_input:
    final_input = action_prompt

  if uploaded_file and action_prompt:
    st.toast(f"📎 Rejim və Media seçildi!", icon="🚀")

  # Göndərmə prosesi
  if final_input or uploaded_file:
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

    prompt_text = final_input if final_input else "Bu faylı analiz et."
    content_parts.append(prompt_text)

    # İstifadəçi mesajını yaddaşa yazmaq və göstərmək (ZƏNGİN MAVİ)
    st.session_state.messages.append({"role": "user", "content": prompt_text})
    with st.chat_message("user"):
      st.markdown(prompt_text)

    # AI Cavabının hazırlanması və göstərilməsi (BOZ)
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
  st.warning("Zəhmət olmasa sol paneldən API Key daxil edin.")
