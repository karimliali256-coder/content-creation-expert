import os
import tempfile
import streamlit as st
from google import genai
from google.genai import types


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Viral Creator AI",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# MOBILE-FIRST CSS
# ============================================================

def inject_mobile_css():

    st.markdown(
        """
        <style>

        /* =====================================================
           GLOBAL
        ===================================================== */

        * {
            box-sizing: border-box;
        }

        html, body {
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            overflow-x: hidden !important;
            background: #ffffff !important;
        }

        .stApp {
            background: #ffffff !important;
            color: #172033 !important;
            font-family:
                Inter,
                -apple-system,
                BlinkMacSystemFont,
                "Segoe UI",
                Roboto,
                sans-serif !important;
        }

        /* Remove Streamlit top spacing */

        header {
            display: none !important;
        }

        footer {
            display: none !important;
        }

        #MainMenu {
            visibility: hidden !important;
        }

        [data-testid="stAppViewContainer"] {
            background: #ffffff !important;
        }

        [data-testid="stMain"] {
            background: #ffffff !important;
        }


        /* =====================================================
           MAIN CONTAINER
        ===================================================== */

        .main .block-container {
            width: 100% !important;
            max-width: 900px !important;

            margin: 0 auto !important;

            padding-top: 14px !important;
            padding-bottom: 105px !important;
            padding-left: 12px !important;
            padding-right: 12px !important;
        }


        /* =====================================================
           HEADER
        ===================================================== */

        .mobile-header {
            width: 100%;
            text-align: center;
            padding: 8px 4px 18px 4px;
        }

        .mobile-header h1 {
            margin: 0 !important;
            color: #0A192F !important;
            font-size: 26px !important;
            line-height: 1.15 !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px !important;
        }

        .mobile-header p {
            margin: 6px 0 0 0 !important;
            color: #718096 !important;
            font-size: 13px !important;
            line-height: 1.4 !important;
        }


        /* =====================================================
           CHAT AREA
        ===================================================== */

        [data-testid="stChatMessage"] {
            width: fit-content !important;
            max-width: 88% !important;

            padding: 12px 15px !important;
            margin-top: 5px !important;
            margin-bottom: 10px !important;

            border-radius: 18px !important;

            font-size: 15px !important;
            line-height: 1.55 !important;

            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        /* Avatar */

        [data-testid="stChatMessageAvatar"] {
            display: none !important;
        }

        /* Message content */

        [data-testid="stChatMessageContent"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        [data-testid="stChatMessageContent"] p {
            margin-top: 0 !important;
            margin-bottom: 8px !important;
        }

        [data-testid="stChatMessageContent"] p:last-child {
            margin-bottom: 0 !important;
        }

        /* Markdown */

        [data-testid="stChatMessageContent"] pre {
            max-width: 100% !important;
            overflow-x: auto !important;
            border-radius: 10px !important;
        }

        [data-testid="stChatMessageContent"] code {
            word-break: break-word !important;
        }

        [data-testid="stChatMessageContent"] table {
            display: block !important;
            max-width: 100% !important;
            overflow-x: auto !important;
            white-space: nowrap !important;
        }

        /* Images */

        [data-testid="stChatMessageContent"] img {
            max-width: 100% !important;
            height: auto !important;
            border-radius: 12px !important;
        }


        /* =====================================================
           STREAMLIT CHAT INPUT
        ===================================================== */

        [data-testid="stChatInput"] {
            position: fixed !important;

            left: 0 !important;
            right: 0 !important;
            bottom: 0 !important;

            width: 100% !important;

            z-index: 999999 !important;

            background: rgba(255,255,255,0.96) !important;

            backdrop-filter: blur(14px) !important;
            -webkit-backdrop-filter: blur(14px) !important;

            border-top: 1px solid #E7EAF0 !important;

            padding:
                8px
                10px
                calc(8px + env(safe-area-inset-bottom))
                10px !important;
        }

        [data-testid="stChatInput"] > div {
            max-width: 900px !important;
            margin: 0 auto !important;
        }

        [data-testid="stChatInput"] textarea {
            min-height: 46px !important;
            max-height: 130px !important;

            border-radius: 24px !important;

            border: 1px solid #D9DEE7 !important;

            background: #FFFFFF !important;

            color: #172033 !important;

            font-size: 16px !important;

            padding: 12px 48px 12px 16px !important;

            box-shadow: 0 2px 10px rgba(10,25,47,0.04) !important;

            outline: none !important;
        }

        [data-testid="stChatInput"] textarea:focus {
            border-color: #1A73E8 !important;
            box-shadow:
                0 0 0 2px rgba(26,115,232,0.10) !important;
        }

        [data-testid="stChatInputSubmitButton"] {
            width: 38px !important;
            height: 38px !important;
        }


        /* =====================================================
           BUTTONS
        ===================================================== */

        .stButton > button {
            min-height: 46px !important;

            border-radius: 13px !important;

            font-size: 14px !important;
            font-weight: 600 !important;

            border: 1px solid #E0E4EA !important;

            background: #F7F8FA !important;
            color: #172033 !important;

            transition: 0.15s ease !important;
        }

        .stButton > button:active {
            transform: scale(0.98) !important;
        }


        /* =====================================================
           POPOVER
        ===================================================== */

        [data-testid="stPopover"] {
            width: 100% !important;
        }

        [data-testid="stPopover"] > button {
            width: 48px !important;
            height: 48px !important;

            min-width: 48px !important;

            padding: 0 !important;

            border-radius: 50% !important;

            background: #F1F3F6 !important;

            border: 1px solid #DDE1E7 !important;

            color: #0A192F !important;

            font-size: 23px !important;
        }


        /* =====================================================
           FILE UPLOADER
        ===================================================== */

        [data-testid="stFileUploader"] {
            width: 100% !important;
        }

        [data-testid="stFileUploaderDropzone"] {
            min-height: 100px !important;

            border-radius: 14px !important;

            border: 1px dashed #CBD2DC !important;

            background: #FAFBFC !important;
        }

        [data-testid="stFileUploaderDropzone"] * {
            font-size: 13px !important;
        }


        /* =====================================================
           ALERT
        ===================================================== */

        [data-testid="stAlert"] {
            border-radius: 14px !important;
            font-size: 14px !important;
        }


        /* =====================================================
           SPINNER
        ===================================================== */

        [data-testid="stSpinner"] {
            font-size: 14px !important;
        }


        /* =====================================================
           SIDEBAR
        ===================================================== */

        [data-testid="stSidebar"] {
            background: #FFFFFF !important;
        }

        [data-testid="stSidebar"] > div:first-child {
            padding: 20px 16px !important;
        }


        /* =====================================================
           MOBILE BREAKPOINT
        ===================================================== */

        @media (max-width: 600px) {

            .main .block-container {
                max-width: 100% !important;

                padding-left: 9px !important;
                padding-right: 9px !important;

                padding-top: 8px !important;
                padding-bottom: 100px !important;
            }

            .mobile-header {
                padding-bottom: 12px !important;
            }

            .mobile-header h1 {
                font-size: 23px !important;
            }

            .mobile-header p {
                font-size: 12px !important;
            }

            [data-testid="stChatMessage"] {
                max-width: 91% !important;

                padding: 10px 13px !important;

                border-radius: 17px !important;

                font-size: 15px !important;
            }

            [data-testid="stChatInput"] {
                padding-left: 7px !important;
                padding-right: 7px !important;
            }

            [data-testid="stChatInput"] textarea {
                font-size: 16px !important;
            }
        }


        /* =====================================================
           VERY SMALL PHONES
        ===================================================== */

        @media (max-width: 360px) {

            .mobile-header h1 {
                font-size: 21px !important;
            }

            [data-testid="stChatMessage"] {
                max-width: 94% !important;
                font-size: 14px !important;
            }

            .main .block-container {
                padding-left: 7px !important;
                padding-right: 7px !important;
            }
        }


        /* =====================================================
           LANDSCAPE MOBILE
        ===================================================== */

        @media (
            max-width: 900px
        ) and (
            orientation: landscape
        ) {

            .main .block-container {
                padding-bottom: 90px !important;
            }

            .mobile-header {
                padding-bottom: 7px !important;
            }
        }

        </style>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# SYSTEM INSTRUCTION
# ============================================================

SYSTEM_INSTRUCTION = """
You are Viral Creator AI.

You are an expert in:
- TikTok
- Instagram Reels
- YouTube Shorts
- retention
- hooks
- storytelling
- audience psychology
- content strategy
- trend analysis
- social media algorithms

Your job is to give practical, high-quality answers.

MODES:

1. BRAINSTORM
Generate 3 strong video concepts.
Each concept should contain:
- Hook
- Core idea
- Retention mechanism
- Suggested ending
- CTA

2. DEEP RESEARCH
Analyze the topic deeply from:
- algorithmic perspective
- psychological perspective
- visual perspective
- retention perspective
- audience perspective

If real-time information is required, use Google Search.

3. A/B TEST
Create:
- Hook A
- Hook B
- Title A
- Title B
- CTA A
- CTA B

Then explain which version is more likely to perform and why.

Always prioritize:
- strong hooks
- curiosity
- emotional tension
- retention
- specificity
- practical value

Avoid generic motivational clichés.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "pending_action" not in st.session_state:
    st.session_state.pending_action = None

if "uploaded_file" not in st.session_state:
    st.session_state.uploaded_file = None


# ============================================================
# API KEY
# ============================================================

api_key = st.sidebar.text_input(
    "Google Gemini API Key",
    type="password",
    placeholder="AIza...",
)

st.sidebar.markdown("---")

st.sidebar.caption(
    "API Key yalnız bu Streamlit sessiyası üçün istifadə olunur."
)


# ============================================================
# HEADER
# ============================================================

inject_mobile_css()

st.markdown(
    """
    <div class="mobile-header">
        <h1>🚀 Viral Creator AI</h1>
        <p>TikTok • Reels • Shorts üçün AI Content Agent</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# API KEY YOXDURSA
# ============================================================

if not api_key:

    st.info(
        "🚀 Başlamaq üçün yuxarıdakı menyudan Google Gemini API Key əlavə et."
    )

    st.markdown(
        """
        <div style="
            margin-top:25px;
            padding:20px;
            border-radius:18px;
            background:#F7F8FA;
            text-align:center;
        ">
            <div style="font-size:38px;">🎯</div>

            <h3 style="margin:8px 0;color:#0A192F;">
                Viral Creator AI
            </h3>

            <p style="
                color:#64748B;
                font-size:14px;
                margin:0;
            ">
                Hook yarat, trend araşdır, A/B test et və
                videolarını analiz etdir.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# GEMINI CLIENT
# ============================================================

try:

    client = genai.Client(api_key=api_key)

except Exception as e:

    st.error(f"Gemini Client xətası: {e}")
    st.stop()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    role = message["role"]

    with st.chat_message(role):
        st.markdown(message["content"])


# ============================================================
# MOBILE ACTION BUTTON
# ============================================================

action_prompt = None

with st.popover("➕"):

    st.markdown("### Ağıllı Rejimlər")

    if st.button(
        "💡 Brainstorm",
        use_container_width=True,
    ):

        action_prompt = (
            "Mənim üçün 3 yüksək retention ehtimallı "
            "viral video ideyası brainstorm et."
        )

    if st.button(
        "🔍 Deep Research",
        use_container_width=True,
    ):

        action_prompt = (
            "Bu mövzunu dərin araşdır və "
            "alqoritmik, psixoloji və vizual baxımdan analiz et:"
        )

    if st.button(
        "🅰️/🅱️ A/B Test",
        use_container_width=True,
    ):

        action_prompt = (
            "Bu mövzu üçün A/B test hazırla. "
            "2 Hook, 2 Title və 2 CTA yarat:"
        )

    st.divider()

    uploaded_file = st.file_uploader(
        "📎 Media yüklə",
        type=[
            "jpg",
            "jpeg",
            "png",
            "webp",
            "mp4",
            "mov",
            "webm",
        ],
    )


# ============================================================
# CHAT INPUT
# ============================================================

user_input = st.chat_input(
    "Mesajınızı yazın..."
)


# ============================================================
# FINAL INPUT
# ============================================================

final_input = user_input

if action_prompt and not user_input:
    final_input = action_prompt


# ============================================================
# NO INPUT
# ============================================================

if not final_input and not uploaded_file:
    st.stop()


# ============================================================
# BUILD GEMINI CONTENT
# ============================================================

content_parts = []


# ============================================================
# MEDIA
# ============================================================

if uploaded_file:

    try:

        suffix = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=suffix,
        ) as tmp:

            tmp.write(
                uploaded_file.getvalue()
            )

            tmp_path = tmp.name


        with st.spinner("📎 Media emal olunur..."):

            uploaded = client.files.upload(
                file=tmp_path
            )

        content_parts.append(uploaded)

    except Exception as e:

        st.error(
            f"Fayl yüklənərkən xəta baş verdi: {e}"
        )

        st.stop()


# ============================================================
# PROMPT
# ============================================================

prompt_text = (
    final_input
    if final_input
    else "Bu media faylını analiz et."
)

content_parts.append(prompt_text)


# ============================================================
# SHOW USER MESSAGE
# ============================================================

st.session_state.messages.append(
    {
        "role": "user",
        "content": prompt_text,
    }
)

with st.chat_message("user"):
    st.markdown(prompt_text)


# ============================================================
# GENERATE RESPONSE
# ============================================================

with st.chat_message("assistant"):

    with st.spinner("Agent düşünür..."):

        try:

            response = client.models.generate_content(

                model="gemini-3.6-flash",

                contents=content_parts,

                config=types.GenerateContentConfig(

                    system_instruction=SYSTEM_INSTRUCTION,

                    tools=[
                        types.Tool(
                            google_search=types.GoogleSearch()
                        )
                    ],
                ),
            )

            answer = response.text

            st.markdown(answer)

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:
