import tempfile
import google.generativeai as genai
import streamlit as st

st.set_page_config(
    page_title="Viral AI Agent", page_icon="🚀", layout="centered"
)

st.title("🚀 Viral Creator AI Agent")
st.caption(
    "Deep Research, İnternet Analizi, Description Generator & Multimodal"
    " Asistent"
)

api_key = st.sidebar.text_input("Google AI Studio API Key:", type="password")

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

    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=SYSTEM_INSTRUCTION,
    )

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    uploaded_file = st.file_uploader(
        "📸 Şəkil və ya 🎥 Video əlavə et:", type=["jpg", "png", "mp4", "mov"]
    )
    user_input = st.chat_input(
        "Sual yaz, trend soruş, 'Description yaz' və ya 'Dərin analiz et' de..."
    )

    if user_input or uploaded_file:
        content_parts = []

        if uploaded_file:
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=uploaded_file.name
            ) as tmp:
                tmp.write(uploaded_file.getvalue())
                tmp_path = tmp.name

            st.info("Media faylı emal edilir...")
            media_file = genai.upload_file(tmp_path)
            content_parts.append(media_file)

        if user_input:
            content_parts.append(user_input)

        st.session_state.messages.append(
            {"role": "user", "content": user_input or "[Media yükləndi]"}
        )
        with st.chat_message("user"):
            st.markdown(user_input or "[Media yükləndi]")

        with st.chat_message("assistant"):
            with st.spinner("Cavab hazırlanır..."):
                response = model.generate_content(content_parts)
                st.markdown(response.text)
                st.session_state.messages.append(
                    {"role": "assistant", "content": response.text}
                )
else:
    st.warning("Zəhmət olmasa sol paneldən API Key-i daxil et.")
