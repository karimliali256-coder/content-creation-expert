import tempfile
import time
import google.generativeai as genai
import streamlit as st

# 1. MOBİL ÜÇÜN XÜSUSİ SƏHİFƏ KONFİQURASİYASI
st.set_page_config(
    page_title="Viral Creator AI",
    page_icon="🚀",
    layout="wide",  # Telefon ekranını tam əhatə etmək üçün wide
    initial_sidebar_state="collapsed",
)

# 2. XÜSUSİ MOBİL VƏ GEMİNİ UI CSS KODLARI
def inject_mobile_css():
    st.markdown(
        """
        <style>
        /* --- Mobil Ekran Boşluqlarını Təmizlə --- */
        .main .block-container {
            padding-top: 20px !important;
            padding-bottom: 15px !important;
            padding-left: 10px !important;
            padding-right: 10px !important;
            max-width: 100% !important;
        }
        
        .stApp {
            background-color: #FFFFFF !important;
            font-family: 'Inter', -apple-system, sans-serif;
        }

        header { visibility: hidden; }
        footer { visibility: hidden; }

        /* Başlıq */
        .main-header {
            text-align: center;
            padding-bottom: 15px;
        }
        .main-header h1 {
            color: #0A192F !important; /* Navy Blue */
            font-size: 1.8rem !important;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .main-header p {
            color: #64748B !important;
            font-size: 0.85rem !important;
        }

        /* --- API Xəbərdarlığı (Navy Blue & Ağ) --- */
        [data-testid="stWarning"] {
            background-color: #0A192F !important;
            color: #FFFFFF !important;
            border-radius: 12px;
            border: none;
            padding: 15px;
        }
        [data-testid="stWarning"] .stAlertContent, 
        [data-testid="stWarning"] p {
            color: #FFFFFF !important;
            font-size: 15px !important;
        }

        /* --- Gemini Chat UI (Mobildə) --- */
        [data-testid="stChatMessage"] {
            padding: 12px 16px !important;
            margin-bottom: 12px !important;
            border-radius: 20px !important;
            max-width: 85% !important; /* Mesajların ekranı tam tutmaması üçün */
            font-size: 15px !important;
            line-height: 1.5 !important;
        }

        /* İstifadəçi (Mən) - Zəngin Mavi (Sağda) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) {
            background-color: #1A73E8 !important;
            color: #FFFFFF !important;
            margin-left: auto !important; 
            border-bottom-right-radius: 4px !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) p,
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("user")) .stAlertContent {
            color: #FFFFFF !important;
        }

        /* Chatbot (Agent) - Boz (Solda) */
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")) {
            background-color: #F0F2F5 !important;
            color: #1F1F1F !important;
            margin-right: auto !important; 
            border-bottom-left-radius: 4px !important;
        }
        [data-testid="stChatMessage"]:has([data-testid="stChatMessageContent"]:contains("assistant")) p {
            color: #1F1F1F !important;
        }

        /* Avatarları gizlət */
        [data-testid="stChatMessageAvatar"] {
            display: none !important;
        }

        /* --- Alt Giriş Sahəsi (+ və Mesaj Yeri) --- */
        
        /* Sütunların telefonda alt-alta düşməməsi üçün məcburi yan-yana düzmə */
        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
            align-items: center !important;
            margin-bottom: 5px !important;
        }

        /* + Düyməsi (Boz Fon, Navy İkon) */
        [data-testid="stPopover"] > button {
            border-radius: 50% !important;
            width: 46px !important;
            height: 46px !important;
            background-color: #F0F2F5 !important;
            color: #0A192F !important;
            border: 1px solid #DADCE0 !important;
            font-size: 24px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
        }

        /* Çat giriş qutusu (Ağ) */
        [data-testid="stChatInput"] {
            background-color: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        [data-testid="stChatInput"] input {
            background-color: #FFFFFF !important;
            border: 1px solid #DADCE0 !important;
            border-radius: 24px !important;
            font-size: 16px !important; /* iOS Zoom qarşısını almaq üçün 16px */
            padding: 12px 18px !important;
            color: #1F1F1F !important;
        }

        /* Göndər düyməsi (Navy Blue) */
        [data-testid="stChatInputSubmitBtn"] {
            background-color: #0A192F !important;
            color: #FFFFFF !important;
            border-radius: 50% !important;
            width: 38px !important;
            height: 38px !important;
        }

        /* Popover daxili düymələr */
        .stButton > button {
            border-radius: 12px !important;
            height: 45px !important;
            font-size: 15px !important;
        }

        img, video { border-radius: 12px !important; max-width: 100% !important; height: auto !important;}
        </style>
        """,
        unsafe_allow_html=True,
    )

# 3. ƏSAS FUNKSİYA (Bütün struktur buradadır)
def main():
    inject_mobile_css()

    st.markdown(
        """
        <div class="main-header">
            <h1>🚀 Viral Creator AI</h1>
            <p>Shorts & TikTok üçün Gemini v3.6 Asistenti</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.sidebar:
        st.title("⚙️ Tənzimləmələr")
        st.write("Sistemi aktivləşdirmək üçün API Key daxil edin.")
        api_key = st.text_input("Google AI Studio API Key:", type="password")

    SYSTEM_INSTRUCTION = """
    Sən TikTok, Instagram Reels və YouTube Shorts alqoritmləri üzrə baş ekspert, canlı trend analitiki və multimodal sosial media köməkçisisən.
    Rejim qaydaları:
    1. Brainstorm: 3 ədəd trendə uyğun, yüksək retention ehtimallı video konsepti təqdim et.
    2. Deep Research: Mövzunu və ya medianı alqoritmik, psixoloji və vizual baxımdan addım-addım dərin analiz et.
    3. A/B Test Generator: 2 fərqli Hook, Başlıq və CTA yaradaraq A/B müqayisəsi et.
    """

    if api_key:
        genai.configure(api_key=api_key)

        # Gemini 3.6 Flash + Canlı Axtarış
        model = genai.GenerativeModel(
            model_name="gemini-3.6-flash",
            system_instruction=SYSTEM_INSTRUCTION,
            tools=["google_search_retrieval"],
        )

        if "messages" not in st.session_state:
            st.session_state.messages = []

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

        # İnput üçün xüsusi sütunlar
        col1, col2 = st.columns([1.5, 8.5])

        action_prompt = None
        uploaded_file = None

        with col1:
            with st.popover("➕"):
                st.markdown("**Ağıllı Rejimlər:**")
                if st.button("💡 Brainstorm", use_container_width=True):
                    action_prompt = "Mənim üçün bu mövzuda 3 viral video ideyası brainstorm et:"
                if st.button("🔍 Deep Research", use_container_width=True):
                    action_prompt = "Aşağıdakı mövzunu və ya faylı alqoritmik və psixoloji baxımdan dərin analiz (Deep Research) et:"
                if st.button("🅰️/🅱️ A/B Test", use_container_width=True):
                    action_prompt = "Bu mövzu/video üçün 2 fərqli Hook və Başlıq variantı ilə A/B Test ssenarisi hazırla:"
                st.divider()
                uploaded_file = st.file_uploader(
                    "📎 Fayl Yüklə", type=["jpg", "jpeg", "png", "mp4", "mov"], label_visibility="collapsed"
                )

        with col2:
            user_input = st.chat_input("Mesajınızı yazın...")

        final_input = user_input
        if action_prompt and not user_input:
            final_input = action_prompt

        if uploaded_file and action_prompt:
            st.toast("📎 Fayl və rejim seçildi!", icon="✅")

        # Məlumatın Göndərilməsi
        if final_input or uploaded_file:
            content_parts = []

            if uploaded_file:
                with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
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

            # İstifadəçi Mesajı
            st.session_state.messages.append({"role": "user", "content": prompt_text})
            with st.chat_message("user"):
                st.markdown(prompt_text)

            # Agent Mesajı
            with st.chat_message("assistant"):
                with st.spinner("Agent cavab hazırlayır..."):
                    try:
                        response = model.generate_content(content_parts)
                        st.markdown(response.text)
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Xəta: {e}")
    else:
        st.warning("🚀 Tətbiqi işlətmək üçün zəhmət olmasa sol paneldən API Key daxil edin.")

# Proqramı işə salmaq
if __name__ == "__main__":
    main()
