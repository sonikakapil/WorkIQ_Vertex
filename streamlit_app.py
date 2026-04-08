import asyncio
import uuid

import streamlit as st
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from workiq_agent.agent import root_agent

APP_NAME = "workiq_vertex_demo"
USER_ID = "demo_user"


@st.cache_resource
def get_session_service():
    return InMemorySessionService()


@st.cache_resource
def get_runner():
    return Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=get_session_service(),
    )


async def ensure_session(session_id: str):
    session_service = get_session_service()
    existing = await session_service.get_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=session_id,
    )
    if existing is None:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
        )


async def ask_agent(prompt: str, session_id: str) -> str:
    await ensure_session(session_id)

    runner = get_runner()
    content = types.Content(role="user", parts=[types.Part(text=prompt)])

    final_texts = []

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            for part in event.content.parts:
                text = getattr(part, "text", None)
                if text:
                    final_texts.append(text)

    if final_texts:
        return "\n".join(final_texts).strip()

    return "No response was returned."


def reset_chat():
    st.session_state.messages = []
    st.session_state.session_id = str(uuid.uuid4())


st.set_page_config(page_title="WorkIQ + Vertex Demo", page_icon="💼", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem; padding-bottom: 1.5rem; max-width: 1100px;}
    .demo-card {
        padding: 1rem 1.2rem;
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        margin-bottom: 1rem;
        background: rgba(255,255,255,0.02);
    }
    .small-note {font-size: 0.92rem; opacity: 0.8;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("💼 WorkIQ + Gemini on Vertex AI")
st.caption("Python demo with ADK orchestration, WorkIQ MCP tools, and a Streamlit UI")

col1, col2 = st.columns([4, 1])
with col1:
    st.markdown(
        f"""
        <div class="demo-card">
            <b>Session:</b> <code>{st.session_state.session_id}</code><br/>
            <span class="small-note">
            Ask about meetings, emails, Teams, documents, or people in Microsoft 365.
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
with col2:
    st.button("New chat", on_click=reset_chat, use_container_width=True)

with st.sidebar:
    st.header("Try these")
    sample_prompts = [
        "What meetings do I have this week?",
        "Summarize emails from Sarah about the budget",
        "Find documents I worked on yesterday",
        "Who is working on Project Alpha?",
    ]

    for sample in sample_prompts:
        if st.button(sample, use_container_width=True):
            st.session_state.pending_prompt = sample

    st.markdown("---")
    st.write("First-time setup reminders:")
    st.write("- Run WorkIQ once and complete sign-in/consent")
    st.write("- Authenticate to Vertex AI locally")
    st.write("- Keep Node.js available in PATH")

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_prompt = st.chat_input("Ask WorkIQ something...")
if "pending_prompt" in st.session_state and st.session_state.pending_prompt:
    user_prompt = st.session_state.pending_prompt
    st.session_state.pending_prompt = None

if user_prompt:
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    with st.chat_message("user"):
        st.markdown(user_prompt)

    with st.chat_message("assistant"):
        with st.spinner("Working..."):
            try:
                answer = asyncio.run(ask_agent(user_prompt, st.session_state.session_id))
            except Exception as e:
                answer = (
                    "The demo hit an error.\n\n"
                    f"Details: `{type(e).__name__}: {e}`\n\n"
                    "Common causes are missing Vertex authentication, missing WorkIQ consent, "
                    "or Node/npx not being available in PATH."
                )
        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
