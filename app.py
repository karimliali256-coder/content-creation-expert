import os
import tempfile
import time

import streamlit as st
import google.generativeai as genai


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

/* ============================================================
   GLOBAL
   ============================================================ */

* {
    box-sizing: border-box;
}

html,
body {
    margin: 0 !important;
    padding: 0 !important;
    width: 100% !important;
    overflow-x: hidden !important;
    background: #FFFFFF !important;
}

.stApp {
    background: #FFFFFF !important;
    color: #172033 !important;
    font-family:
        Inter,
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        sans-serif !important;
}

[data-testid="stAppViewContainer"] {
    background: #FFFFFF !important;
}

[data-testid="stMain"] {
    background: #FFFFFF !important;
}

/* Streamlit header */
header {
    display: block !important;
}

footer {
    display: none !important;
}

#MainMenu {
    display: none !important;
}


/* ============================================================
   MAIN CONTAINER
   ============================================================ */

.main .block-container {
    width: 100% !important;
    max-width: 900px !important;

    margin: 0 auto !important;

    padding-top: 12px !important;
    padding-bottom: 115px !important;

    padding-left: 10px !important;
    padding-right: 10px !important;
}


/* ============================================================
   HEADER
   ============================================================ */

.mobile-header {
    width: 100%;
    text-align: center;

    padding-top: 8px;
    padding-bottom: 16px;
}

.mobile-header h1 {
    margin: 0 !important;

    color: #0A192F !important;

    font-size: 27px !important;
    line-height: 1.15 !important;

    font-weight: 800 !important;

    letter-spacing: -0.6px !important;
}

.mobile-header p {
    margin: 7px 0 0 0 !important;

    color: #718096 !important;

    font-size: 13px !important;
    line-height: 1.4 !important;
}


/* ============================================================
   API SETTINGS
   ============================================================ */

[data-testid="stExpander"] {
    border: 1px solid #E3E7ED !important;
    border-radius: 15px !important;

    background: #FAFBFC !important;

    margin-bottom: 14px !important;
}

[data-testid="stExpander"] summary {
    font-weight: 600 !important;
    color: #172033 !important;
}

[data-testid="stExpander"] input {
    font-size: 16px !important;
}


/* ============================================================
   CHAT MESSAGES
   ============================================================ */

[data-testid="stChatMessage"] {
    width: fit-content !important;
    max-width: 89% !important;

    padding: 12px 15px !important;

    margin-top: 5px !important;
    margin-bottom: 11px !important;

    border-radius: 18px !important;

    font-size: 15px !important;
    line-height: 1.55 !important;

    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

[data-testid="stChatMessageAvatar"] {
    display: none !important;
}

[data-testid="stChatMessageContent"] {
    width: 100% !important;
    max-width: 100% !important;

    overflow-wrap: anywhere !important;
    word-break: break-word !important;
}

[data-testid="stChatMessageContent"] p {
    margin-top: 0 !important;
    margin-bottom: 8px !important;
}

[data-testid="stChatMessageContent"] p:last-child {
    margin-bottom: 0 !important;
}


/* ============================================================
   MARKDOWN
   ============================================================ */

[data-testid="stChatMessageContent"] h1,
[data-testid="stChatMessageContent"] h2,
[data-testid="stChatMessageContent"] h3,
[data-testid="stChatMessageContent"] h4 {
    max-width: 100% !important;
    overflow-wrap: anywhere !important;
}

[data-testid="stChatMessageContent"] pre {
    width: 100% !important;
    max-width: 100% !important;

    overflow-x: auto !important;

    border-radius: 11px !important;
}

[data-testid="stChatMessageContent"] code {
    overflow-wrap: anywhere !important;
}

[data-testid="stChatMessageContent"] table {
    display: block !important;

    max-width: 100% !important;

    overflow-x: auto !important;

    white-space: nowrap !important;
}

[data-testid="stChatMessageContent"] img {
    display: block !important;

    max-width: 100% !important;
    width: auto !important;
    height: auto !important;

    border-radius: 13px !important;
}

[data-testid="stChatMessageContent"] video {
    max-width: 100% !important;
    height: auto !important;

    border-radius: 13px !important;
}


/* ============================================================
   CHAT INPUT
   ============================================================ */

[data-testid="stChatInput"] {
    position: fixed !important;

    left: 0 !important;
    right: 0 !important;
    bottom: 0 !important;

    width: 100% !important;

    z-index: 999999 !important;

    background: rgba(255, 255, 255, 0.97) !important;

    backdrop-filter: blur(16px) !important;
    -webkit-backdrop-filter: blur(16px) !important;

    border-top: 1px solid #E6E9EE !important;

    padding-top: 8px !important;
    padding-left: 9px !important;
    padding-right: 9px !important;

    padding-bottom:
        calc(8px + env(safe-area-inset-bottom))
        !important;
}

[data-testid="stChatInput"] > div {
    max-width: 900px !important;

    margin: 0 auto !important;
}

[data-testid="stChatInput"] textarea {
    min-height: 47px !important;
    max-height: 130px !important;

    border-radius: 24px !important;

    border: 1px solid #D8DEE7 !important;

    background: #FFFFFF !important;

    color: #172033 !important;

    font-size: 16px !important;

    padding: 12px 48px 12px 17px !important;

    outline: none !important;

    box-shadow:
        0 2px 12px rgba(10, 25, 47, 0.05) !important;
}

[data-testid="stChatInput"] textarea:focus {
    border-color: #1A73E8 !important;

    box-shadow:
        0 0 0 2px rgba(26, 115, 232, 0.08) !important;
}


/* ============================================================
   PLUS BUTTON
   ============================================================ */

[data-testid="stPopover"] {
    margin-bottom: 8px !important;
}

[data-testid="stPopover"] > button {
    min-width: 48px !important;

    width: 48px !important;
    height: 48px !important;

    padding: 0 !important;

    border-radius: 50% !important;

    background: #F1F3F6 !important;

    border: 1px solid #DDE2E8 !important;

    color: #0A192F !important;

    font-size: 23px !important;
}


/* ============================================================
   ACTION BUTTONS
   ============================================================ */

.stButton > button {
    min-height: 46px !important;

    width: 100% !important;

    border-radius: 13px !important;

    font-size: 14px !important;

    font-weight: 600 !important;

    border: 1px solid #DFE4EA !important;

    background: #F7F8FA !important;

    color: #172033 !important;
}

.stButton > button:active {
    transform: scale(0.98) !important;
}


/* ============================================================
   FILE UPLOADER
   ============================================================ */

[data-testid="stFileUploader"] {
    width: 100% !important;
}

[data-testid="stFileUploaderDropzone"] {
    min-height: 105px !important;

    border-radius: 14px !important;

    border: 1px dashed #C8D0DB !important;

    background: #FAFBFC !important;
}

[data-testid="stFileUploaderDropzone"] * {
    font-size: 13px !important;
}


/* ============================================================
   ALERTS
   ============================================================ */

[data-testid="stAlert"] {
    border-radius: 14px !important;

    font-size: 14px !important;

    line-height: 1.5 !important;
}


/* ============================================================
   SPINNER
   ============================================================ */

[data-testid="stSpinner"] {
    font-size: 14px !important;
}


/* ============================================================
   MOBILE
   ============================================================ */

@media (max-width: 600px) {

    .main .block-container {
        width: 100% !important;
        max-width: 100% !important;

        padding-top: 7px !important;
        padding-left: 8px !important;
        padding-right: 8px !important;
        padding-bottom: 105px !important;
    }

    .mobile-header {
        padding-top: 5px !important;
        padding-bottom: 12px !important;
    }

    .mobile-header h1 {
        font-size: 23px !important;
    }

    .mobile-header p {
        font-size: 12px !important;
    }

    [data-testid="stChatMessage"] {
        max-width: 92% !important;

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


/* ============================================================
   SMALL PHONES
   ============================================================ */

@media (max-width: 360px) {

    .mobile-header h1 {
        font-size: 21px !important;
    }

    .mobile-header p {
        font-size: 11px !important;
    }

    [data-testid="stChatMessage"] {
        max-width: 94% !important;

        font-size: 14px !important;
    }

    .main .block-container {
        padding-left: 6px !important;
        padding-right: 6px !important;
    }

}


/* ============================================================
   LANDSCAPE
   ============================================================ */

@media (
    max-width: 900px
) and (
    orientation: landscape
) {

    .main .block-container {
        padding-bottom: 95px !important;
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
- viral content
- retention
- hooks
- storytelling
- audience psychology
- social media algorithms
- trend analysis
- A/B testing
- short-form video strategy

Your goal is to help the creator make content with strong
retention and viral potential.

BRAINSTORM MODE:

Generate 3 strong video concepts.

For every concept include:

1. Hook
2. Core idea
3. Retention mechanism
4. Visual direction
5. Ending
6. CTA

DEEP RESEARCH MODE:

Analyze the topic deeply from:

- algorithmic perspective
- psychological perspective
- visual perspective
- retention perspective
- audience perspective
- current trend perspective

Use Google Search when current information is needed.

A/B TEST MODE:

Create:

- Hook A
- Hook B
- Title A
- Title B
- CTA A
- CTA B

Then explain which version is stronger and why.

IMPORTANT:

Avoid generic motivational clichés.

Prioritize:

- curiosity
- emotional tension
- specificity
- strong hooks
- retention
- practical value
- shareability
- comments
- saves

Give actionable answers.
"""


# ============================================================
# SESSION STATE
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# ============================================================
# CSS
# ============================================================

inject_mobile_css()


# ============================================================
# HEADER
# ============================================================

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
# API SETTINGS
# ============================================================

with st.expander(
    "⚙️ Gemini API Settings",
    expanded=False,
):

    api_key = st.text_input(
        "Google Gemini API Key",
        type="password",
        placeholder="AIza...",
        help="Google AI Studio API Key daxil et.",
    )

    st.caption(
        "API Key bu sessiyada istifadə olunur."
    )


# ============================================================
# API KEY CHECK
# ============================================================

if not api_key:

    st.info(
        "🚀 Başlamaq üçün yuxarıdakı "
        "Gemini API Settings bölməsinə API Key əlavə et."
    )

    st.markdown(
        """
<div style="
    margin-top:22px;
    padding:22px;
    border-radius:18px;
    background:#F7F8FA;
    text-align:center;
">

    <div style="font-size:40px;">🎯</div>

    <h3 style="
        margin:8px 0;
        color:#0A192F;
        font-size:20px;
    ">
        Viral Creator AI
    </h3>

    <p style="
        color:#64748B;
        font-size:14px;
        margin:0;
        line-height:1.6;
    ">
        Viral ideyalar yarat.<br>
        Videoları analiz et.<br>
        Hook və CTA-ları test et.
    </p>

</div>
""",
        unsafe_allow_html=True,
    )

    st.stop()


# ============================================================
# GEMINI CONFIGURATION
# ============================================================

try:

    genai.configure(
        api_key=api_key
    )

    model = genai.GenerativeModel(
        model_name="gemini-3.6-flash",
        system_instruction=SYSTEM_INSTRUCTION,
        tools=[
            "google_search_retrieval"
        ],
    )

except Exception as e:

    st.error(
        f"Gemini konfiqurasiya xətası: {e}"
    )

    st.stop()


# ============================================================
# CHAT HISTORY
# ============================================================

for message in st.session_state.messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ============================================================
# PLUS MENU
# ============================================================

action_prompt = None
uploaded_file = None

with st.popover("➕"):

    st.markdown(
        "### 🧠 Ağıllı Rejimlər"
    )

    st.caption(
        "Agentə nə etmək istədiyini seç."
    )

    if st.button(
        "💡 Brainstorm",
        use_container_width=True,
    ):

        action_prompt = (
            "Mənim üçün 3 yüksək retention "
            "ehtimallı viral video ideyası brainstorm et."
        )

    if st.button(
        "🔍 Deep Research",
        use_container_width=True,
    ):

        action_prompt = (
            "Aşağıdakı mövzunu dərin araşdır. "
            "Alqoritmik, psixoloji, vizual, "
            "retention və trend baxımından analiz et:"
        )

    if st.button(
        "🅰️/🅱️ A/B Test",
        use_container_width=True,
    ):

        action_prompt = (
            "Bu mövzu üçün A/B test hazırla. "
            "2 Hook, 2 Title və 2 CTA yarat. "
            "Sonra hansının daha güclü olduğunu izah et:"
        )

    st.divider()

    uploaded_file = st.file_uploader(
        "📎 Şəkil və ya video yüklə",
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
# NOTHING TO DO
# ============================================================

if not final_input and not uploaded_file:

    st.stop()


# ============================================================
# CONTENT
# ============================================================

content_parts = []


# ============================================================
# MEDIA UPLOAD
# ============================================================

if uploaded_file:

    try:

        file_extension = os.path.splitext(
            uploaded_file.name
        )[1]

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=file_extension,
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue()
            )

            temp_path = temp_file.name

        with st.spinner(
            "📎 Media emal olunur..."
        ):

            media_file = genai.upload_file(
                temp_path
            )

            while (
                media_file.state.name
                == "PROCESSING"
            ):

                time.sleep(1)

                media_file = genai.get_file(
                    media_file.name
                )

        content_parts.append(
            media_file
        )

    except Exception as e:

        st.error(
            f"Media yüklənərkən xəta: {e}"
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

content_parts.append(
    prompt_text
)


# ============================================================
# USER MESSAGE
# ============================================================

st.session_state.messages.append(
    {
        "role": "user",
        "content": prompt_text,
    }
)

with st.chat_message("user"):

    st.markdown(
        prompt_text
    )


# ============================================================
# AI RESPONSE
# ============================================================

with st.chat_message("assistant"):

    with st.spinner(
        "Agent cavab hazırlayır..."
    ):

        try:

            response = model.generate_content(
                content_parts
            )

            answer = response.text

            st.markdown(
                answer
            )

            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "content": answer,
                }
            )

        except Exception as e:

            st.error(
                f"Gemini xətası: {e}"
            )
