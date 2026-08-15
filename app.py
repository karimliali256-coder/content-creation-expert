import tempfile
import time
import google.generativeai as genai
import streamlit as st

# Streamlit Səhifə Konfiqurasiyası
st.set_page_config(
    page_title="Viral Creator AI Agent",
    page_icon="🚀",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Custom CSS: Modern Navy Blue & Ağ Dizayn, Kavisli Çat və Motion
st.markdown(
    """
    <style>
    /* Bütün səhifə üçün fon və şrift ayarları */
    .stApp {
        background-color: #F8FAFC;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* Yüngül Giriş Animasiyası (Motion) */
    @keyframes slideInUp {
        from {
            opacity: 0;
            transform: translateY(15px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes rotatePlus {
        from { transform: rotate(0deg); }
        to { transform: rotate(90deg); }
    }

    /* Başlıq sahəsi */
    .main-header {
        text-align: center;
        padding: 20px 0 10px 0;
        animation: slideInUp 0.4s ease-out;
    }
    .main-header h1 {
        color: #0A192F;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .main-header p {
        color: #4A5568;
        font-size: 0.95rem;
    }

    /* Çat Mesaj Qutuları - Kavisli və Animasiyalı */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0 !important;
        border-radius: 20px !important;
        padding: 16px 20px !important;
        margin-bottom: 12px !important;
        box-shadow: 0 4px 12px rgba(10, 25, 47, 0.03) !important;
        animation: slideInUp 0.3s ease-out !important;
    }

    /* İstifadəçi Mesajı Style - Navy Blue Vurğusu */
    [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) {
        background-color: #0A192F !important;
        color: #FFFFFF !important;
        border: none !important;
    }

    /* Pop-over Fayl Yükləmə Düyməsi (+) Style */
    [data-testid="stPopover"] > button {
        border-radius: 50% !important;
        width: 46px !important;
        height: 46px !important;
        background-color: #0A192F !important;
        color: #FFFFFF !important;
        border: none !important;
        font-size: 22px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 10px rgba(10, 25, 47, 0.15) !important;
    }
    [data-testid="stPopover"] > button:hover {
        background-color: #1E293B !important;
        transform: scale(1.05);
    }
    
    /* Şəkillərin kavisli göstərilməsi */
    img {
        border-radius: 14px !important;
    }

    /* Səhifə alt hissəsi təmizliyi */
    footer {visibility: hidden;}
    </style>
""",
    unsafe_allow_html=True,
)

# İnterfeys Başlığı
st.markdown(
    """
    <div class="main-header">
        <h1>🚀 Viral Creator AI</h1>
        <p>TikTok, Reels və Shorts üçün Modern Kontent Asistenti</p>
    </div>
""",
    unsafe_allow_html=True,
)

# Sol panel: API Key Girişi
with st.sidebar:
  st.title("⚙️ Tənzimləmələr")
  api_key = st.text_input("Google AI Studio API Key:", type="password")

SYSTEM_INSTRUCTION = """
Sən TikTok, Instagram Reels və YouTube Shorts alqoritmləri üzrə baş ekspert, canlı trend analitiki və multimodal sosial media köməkçisisən.

MÜHÜM QAYDALAR:
1. NORMAL DİALOQ: Kontent ideyaları, ssenarilər, montaj və hook təklifləri ver.
2. VİRAL FAİZİ: YALNIZ istifadəçi xüsusi olaraq viral ehtimalını/qiymətləndirməsini soruşduqda (məsələn: "Viral ehtimalı neçədir?") cavabın İLK SƏTİRİNDƏ mütləq "📊 VIRAL EHTİMAL: [X]%" formatında göstərici ver (0-100% arası).
3. DESCRIPTION & HASHTAGS: Əgər istifadəçi "Description yaz", "Təsvir ver" və ya "SEO tərtib et" desə, aşağıdakı strukturda hazır mətn çıxar:
   - 📌 **Description:** (İlk 2 saniyədə maraq oyadan, keyword-lərlə zəngin 2-3 cümləlik mətn)
   - 🏷️ **Hashtag-lər:** (3 ədəd geniş kütlə üçün + 3 ədəd spesifik nisa uyğun hashtag)
   - 💬 **Call to Action (CTA):** (Rəy yazmağa və ya paylaşmağa təşviq edən sual)
4. DEEP RESEARCH (DƏRİN ANALİZ): Əgər istifadəçi "Dərin analiz et" və ya "Research et" desə, mövzunu və ya media faylını alqoritmik, psixoloji və vizual baxımdan detallı kəşf et.
"""

if api_key:
  genai.configure(api_key=api_key)

  # Ən son güncəl Gemini modeli
  model = genai.GenerativeModel(
      model_name="gemini-3.6-flash",
      system_instruction=SYSTEM_INSTRUCTION,
      tools=["google_search_retrieval"]  # Canlı web research imkanı əlavə edir
  )

  # Sesiyaların yadda saxlanması
  if "messages" not in st.session_state:
    st.session_state.messages = []

  # Keçmiş mesajların ekranda göstərilməsi
  for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
      st.markdown(msg["content"])

  # İnput Sahəsi: Modern Layout (+ fayl yükləmə və mətn girişi)
  col1, col2 = st.columns([1, 7])

  with col1:
    with st.popover("➕", help="Şəkil və ya Video əlavə et"):
      uploaded_file = st.file_uploader(
          "Media seçin:",
          type=["jpg", "jpeg", "png", "mp4", "mov"],
          label_visibility="collapsed",
      )

  with col2:
    user_input = st.chat_input("Fikir yazın və ya 'Dərin analiz et' deyin...")

  # Media yükləndikdə kiçik xəbərdarlıq qutusu
  if uploaded_file:
    st.toast(f"📎 Fayl seçildi: {uploaded_file.name}", icon="✅")

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
          time.sleep(1.5)
          media_file = genai.get_file(media_file.name)

      content_parts.append(media_file)

    if user_input:
      content_parts.append(user_input)

    # İstifadəçi mesajını yaddaşa yazmaq və göstərmək
    display_text = user_input or "[Media faylı gönderildi]"
    st.session_state.messages.append({"role": "user", "content": display_text})
    with st.chat_message("user"):
      st.markdown(display_text)

    # AI Cavabının hazırlanması
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
