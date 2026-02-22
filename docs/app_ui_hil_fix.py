import streamlit as st
import asyncio
import os
import sys

# Ensure the root project directory is in the Python path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.orchestrator import DebateOrchestrator, AGENT_META
from src.config import ResponseLevel
from dotenv import load_dotenv

# Ensure we have our environment variables (like GEMINI_API_KEY)
load_dotenv()

st.set_page_config(
    page_title="🤖 Group Debate Agents",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS for Beautiful UI ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');

    /* ── 1. Full-app outer background: light blue gradient ── */
    .stApp {
        background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 50%, #93c5fd 100%) !important;
        font-family: 'Inter', sans-serif;
    }

    /* ── 2. Top header bar (Streamlit toolbar) ── */
    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    /* ── 3. Main content white card ── */
    .block-container {
        background: #ffffff !important;
        border-radius: 16px !important;
        padding: 0 2rem 2rem 2rem !important;
        margin-top: 1.5rem !important;
        box-shadow: 0 6px 30px rgba(59,130,246,0.18) !important;
        overflow-x: hidden !important;
    }

    /* ── Human-in-the-Loop banner ── */
    .hil-banner {
        background: linear-gradient(120deg, #1e3a8a 0%, #0369a1 100%);
        border: 2px solid #38bdf8;
        border-radius: 14px;
        padding: 16px 22px;
        margin: 12px 0 8px 0;
        color: #e0f2fe;
        font-family: 'Inter', sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        display: flex;
        align-items: center;
        gap: 12px;
        animation: hil-pulse 1.5s ease-in-out infinite;
        box-shadow: 0 0 0 0 rgba(56,189,248,0.7);
    }
    .hil-banner .hil-arrow {
        font-size: 1.4rem;
        animation: bounce-down 1s ease-in-out infinite;
    }
    @keyframes hil-pulse {
        0%   { box-shadow: 0 0 0 0 rgba(56,189,248,0.6); border-color: #38bdf8; }
        50%  { box-shadow: 0 0 0 10px rgba(56,189,248,0); border-color: #7dd3fc; }
        100% { box-shadow: 0 0 0 0 rgba(56,189,248,0); border-color: #38bdf8; }
    }
    @keyframes bounce-down {
        0%, 100% { transform: translateY(0); }
        50%       { transform: translateY(5px); }
    }

    /* Glow on chat input during HIL phase */
    .hil-active [data-testid="stChatInput"] textarea {
        border: 2px solid #38bdf8 !important;
        box-shadow: 0 0 0 4px rgba(56,189,248,0.25), 0 0 16px rgba(56,189,248,0.3) !important;
        animation: input-glow 1.5s ease-in-out infinite;
    }
    @keyframes input-glow {
        0%, 100% { box-shadow: 0 0 0 3px rgba(56,189,248,0.2), 0 0 12px rgba(56,189,248,0.2); }
        50%       { box-shadow: 0 0 0 6px rgba(56,189,248,0.35), 0 0 22px rgba(56,189,248,0.4); }
    }

    /* ── 4. Sidebar: dark navy blue gradient ── */
    [data-testid="stSidebar"] > div {
        background: linear-gradient(180deg, #1e3a5f 0%, #1e40af 100%) !important;
    }
    [data-testid="stSidebar"] .block-container {
        background: transparent !important;
        box-shadow: none !important;
        border-radius: 0 !important;
    }
    [data-testid="stSidebar"] * {
        color: #e0f2fe !important;
    }
    [data-testid="stSidebar"] .stButton > button {
        background: rgba(255,255,255,0.15) !important;
        color: #fff !important;
        border: 1px solid rgba(255,255,255,0.3) !important;
        border-radius: 8px;
    }
    [data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(255,255,255,0.28) !important;
    }
    /* Sidebar selectbox: dark dropdown with white text */
    [data-testid="stSidebar"] [data-baseweb="select"] {
        background-color: rgba(255,255,255,0.12) !important;
        border-color: rgba(255,255,255,0.3) !important;
        border-radius: 8px;
    }
    [data-testid="stSidebar"] [data-baseweb="select"] * {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    /* Sidebar selectbox dropdown menu list */
    [data-baseweb="popover"] ul,
    [data-baseweb="popover"] li {
        background-color: #1e3a5f !important;
        color: #e0f2fe !important;
    }
    [data-baseweb="popover"] li:hover {
        background-color: #2563eb !important;
    }

    /* HIL text-area */
    [data-testid="stTextArea"] textarea {
        background: #f8fafc !important;
        color: #1e293b !important;
        border: 1px solid #94a3b8 !important;
        border-radius: 10px;
        font-size: 1rem;
        line-height: 1.5;
    }

    /* ── 5. Chat message bubbles ── */
    [data-testid="stChatMessage"] {
        background: #f8fafc !important;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        margin-bottom: 0.75rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3,
    [data-testid="stChatMessage"] span {
        color: #1e293b !important;
    }

    /* ── 6. Streaming/thinking block: full-width left-aligned ── */
    [data-testid="stChatMessage"] .stMarkdown {
        width: 100% !important;
        text-align: left !important;
    }

    /* ── 7. Chat input area ── */
    [data-testid="stChatInput"] textarea {
        background: #f1f5f9 !important;
        color: #1e293b !important;
        border: 1px solid #cbd5e1 !important;
        border-radius: 12px;
    }

    /* ── 8. Primary button ── */
    button[kind="primary"] {
        background: linear-gradient(90deg, #2563eb, #1d4ed8) !important;
        color: #fff !important;
        border: none !important;
        border-radius: 8px;
        font-weight: 600;
    }

    /* ── 9. Warning / info alert boxes ── */
    [data-testid="stAlert"] {
        background: #fef9c3 !important;
        border-left: 4px solid #facc15;
        color: #713f12 !important;
    }

    /* ── 10. Chat input: make it taller ── */
    [data-testid="stChatInput"] {
        padding: 0.6rem 1rem !important;
    }
    [data-testid="stChatInput"] textarea {
        min-height: 56px !important;
        font-size: 1rem !important;
        line-height: 1.6 !important;
        padding: 0.7rem 1rem !important;
        border-radius: 14px !important;
        background: #f8fafc !important;
        color: #1e293b !important;
        border: 1.5px solid #94a3b8 !important;
        transition: border 0.2s;
    }
    [data-testid="stChatInput"] textarea:focus {
        border-color: #2563eb !important;
        box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
    }

    /* ── 11. Hero header banner ── */
    .hero-banner {
        background: linear-gradient(120deg, #0f172a 0%, #1e3a8a 45%, #0369a1 100%);
        margin: 0 -2rem 1.5rem -2rem;
        padding: 18px 2.2rem 16px 2.2rem;
        display: flex;
        align-items: center;
        gap: 18px;
        position: relative;
        overflow: hidden;
    }
    /* subtle sheen overlay */
    .hero-banner::before {
        content: '';
        position: absolute;
        inset: 0;
        background: radial-gradient(ellipse at 70% 50%, rgba(56,189,248,0.18) 0%, transparent 70%);
        pointer-events: none;
    }
    /* sparkle dots */
    .hero-banner::after {
        content: '';
        position: absolute;
        right: 3rem; top: 50%;
        transform: translateY(-50%);
        width: 90px; height: 90px;
        background: radial-gradient(circle at 30% 40%, rgba(255,255,255,0.12) 2px, transparent 2px),
                    radial-gradient(circle at 70% 20%, rgba(255,255,255,0.10) 2px, transparent 2px),
                    radial-gradient(circle at 50% 80%, rgba(255,255,255,0.08) 2px, transparent 2px),
                    radial-gradient(circle at 85% 65%, rgba(255,255,255,0.10) 2px, transparent 2px);
        pointer-events: none;
    }
    .hero-icon {
        flex-shrink: 0;
        width: 72px; height: 42px;
        background: linear-gradient(135deg, #0f2d5e, #1e3a8a);
        border-radius: 10px;
        display: flex; align-items: center; justify-content: center;
        padding: 4px 6px;
        box-shadow: 0 0 16px rgba(56,189,248,0.4);
    }
    .hero-title {
        font-family: 'Inter', sans-serif;
        font-size: 1.45rem;
        font-weight: 800;
        color: #ffffff;
        text-shadow: 0 0 24px rgba(147,197,253,0.6);
        line-height: 1.15;
        margin: 0;
        letter-spacing: -0.01em;
    }
    .hero-title span {
        color: #7dd3fc !important;
    }
    .hero-sub {
        font-size: 0.75rem;
        color: rgba(186,230,253,0.85);
        margin: 4px 0 0 0;
        letter-spacing: 0.03em;
    }
    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 4px;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(147,197,253,0.35);
        color: #bae6fd;
        font-size: 0.6rem;
        font-weight: 700;
        padding: 3px 9px;
        border-radius: 20px;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        margin-top: 5px;
    }

    /* ── 11. General text ── */
    p, li, label, span {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)


# ── Main Header ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <div class="hero-icon">
    <svg width="72" height="42" viewBox="0 0 72 42" fill="none" xmlns="http://www.w3.org/2000/svg">
      <defs>
        <linearGradient id="bg1" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="#38bdf8" />
          <stop offset="100%" stop-color="#2563eb" />
        </linearGradient>
        <linearGradient id="bg2" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#c084fc" />
          <stop offset="100%" stop-color="#7c3aed" />
        </linearGradient>
        <linearGradient id="bg3" x1="1" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#2dd4bf" />
          <stop offset="100%" stop-color="#059669" />
        </linearGradient>
        <filter id="drop" x="-20%" y="-20%" width="140%" height="140%">
          <feDropShadow dx="0" dy="2" stdDeviation="1.5" flood-color="#000" flood-opacity="0.3"/>
        </filter>
      </defs>
      <!-- Background sync lines -->
      <path d="M20 22 L36 10 L52 22 Z" stroke="rgba(255,255,255,0.25)" stroke-width="1.5" stroke-dasharray="2 2" fill="none"/>
      <circle cx="20" cy="22" r="2" fill="#38bdf8" opacity="0.8"/>
      <circle cx="52" cy="22" r="2" fill="#c084fc" opacity="0.8"/>
      <circle cx="36" cy="10" r="2" fill="#2dd4bf" opacity="0.8"/>
      <!-- Left Bot Bubble -->
      <g filter="url(#drop)">
        <rect x="8" y="14" width="22" height="15" rx="5" fill="url(#bg1)"/>
        <polygon points="12,29 18,29 12,34" fill="url(#bg1)"/>
        <rect x="12" y="18" width="14" height="3" rx="1.5" fill="#0f172a"/>
        <rect x="13" y="18.5" width="5" height="2" rx="1" fill="#38bdf8"/>
      </g>
      <!-- Right Bot Bubble -->
      <g filter="url(#drop)">
        <rect x="42" y="14" width="22" height="15" rx="5" fill="url(#bg2)"/>
        <polygon points="60,29 54,29 60,34" fill="url(#bg2)"/>
        <rect x="46" y="18" width="14" height="3" rx="1.5" fill="#0f172a"/>
        <rect x="53" y="18.5" width="6" height="2" rx="1" fill="#c084fc"/>
      </g>
      <!-- Top Center Bot Bubble -->
      <g filter="url(#drop)">
        <rect x="25" y="2" width="22" height="15" rx="5" fill="url(#bg3)"/>
        <polygon points="36,17 42,17 36,22" fill="url(#bg3)"/>
        <rect x="29" y="6" width="14" height="3" rx="1.5" fill="#0f172a"/>
        <rect x="30" y="6.5" width="4" height="2" rx="1" fill="#2dd4bf"/>
      </g>
    </svg>
  </div>
  <div>
    <p class="hero-title">Architecture <span>Debate</span> Agents</p>
    <p class="hero-sub">⚡ AutoGen 0.4 &nbsp;·&nbsp; Gemini 2.5 Flash &nbsp;·&nbsp; Adversarial Multi-Agent AI</p>
    <span class="hero-badge">🧠 AI-Powered Technical Debate</span>
  </div>
</div>
""", unsafe_allow_html=True)


# ── State Management ─────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "consultant_options" not in st.session_state:
    st.session_state.consultant_options = ""
if "phase" not in st.session_state:
    st.session_state.phase = 0  # 0=Not Started, 1=Options Generated (Wait for HIL), 2=Debate Complete
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = None

# ── Dynamic Layout Adjustment ────────────────────────────────────────────────
# Add hil-active class to body during phase 1 to trigger glow on input
if st.session_state.phase == 1:
    st.markdown("<style>body { } [data-testid='stChatInput'] textarea { border: 2px solid #38bdf8 !important; box-shadow: 0 0 0 5px rgba(56,189,248,0.25), 0 0 18px rgba(56,189,248,0.35) !important; animation: input-glow 1.5s ease-in-out infinite; }</style>", unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.title("⚙️ Debate Settings")
    st.markdown("Configure how the agents debate your topic.")
    
    num_solutions = st.slider("Initial Solutions (Consultant)", min_value=1, max_value=5, value=2)
    max_rounds = st.slider("Max Debate Rounds", min_value=2, max_value=12, value=6)
    
    resp_level_str = st.selectbox(
        "Response Detail Level", 
        ["Simple", "Intermediate", "Advanced", "Expert"],
        index=0
    )
    
    level_map = {
        "Simple": ResponseLevel.SIMPLE,
        "Intermediate": ResponseLevel.INTERMEDIATE,
        "Advanced": ResponseLevel.ADVANCED,
        "Expert": ResponseLevel.EXPERT,
    }
    response_level = level_map[resp_level_str]

    if st.button("🔄 Reset Debate", use_container_width=True):
        st.session_state.chat_history = []
        st.session_state.consultant_options = ""
        st.session_state.phase = 0
        st.session_state.orchestrator = None
        st.rerun()

# ── UI Renderer ───────────────────────────────────────────────────────────────
def render_chat_history():
    """Renders the chat history from session state."""
    for msg in st.session_state.chat_history:
        role = msg.get("role")
        content = msg.get("content")
        avatar = msg.get("avatar", "🤖")
        # Always use 'user' or 'assistant' so Streamlit places messages on the left
        display_role = "user" if role == "user" else "assistant"
        with st.chat_message(display_role, avatar=avatar):
            st.markdown(content, unsafe_allow_html=True)

render_chat_history()

# ── Async Logic Wrappers ──────────────────────────────────────────────────────
async def run_phase1_async(topic: str):
    """Triggers Phase 1 of the debate (generating options if needed)."""
    orch = DebateOrchestrator(
        requirement_topic=topic,
        max_rounds=max_rounds,
        response_level=response_level,
        num_solutions=num_solutions
    )
    st.session_state.orchestrator = orch
    
    # Render user prompt
    st.session_state.chat_history.append({"role": "user", "content": topic, "avatar": "👤"})
    with st.chat_message("user", avatar="👤"):
        st.markdown(topic)
        
    if num_solutions > 1:
        # Stream Phase 1
        with st.chat_message("assistant", avatar="🤝"):
            st.markdown("### ⏳ Consultant is generating initial options...")
            message_placeholder = st.empty()
            full_response = ""
            
            async for chunk in orch.run_phase1_options():
                full_response = chunk.content
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)
            
            message_placeholder.markdown(full_response, unsafe_allow_html=True)
            
        st.session_state.consultant_options = full_response
        st.session_state.chat_history.append({
            "role": "assistant", 
            "content": "**Phase 1: Initial Options**\n\n" + full_response,
            "avatar": "🤝"
        })
        st.session_state.phase = 1
    else:
        # If only 1 solution is requested, immediately jump to Phase 2 (no options phase needed)
        st.session_state.phase = 1

async def run_phase2_async(user_opinion: str):
    """Triggers Phase 2 of the debate."""
    orch = st.session_state.orchestrator
    
    # Store and render user opinion
    if num_solutions > 1:
        opinion_text = f"**User Selection/Feedback:**\n{user_opinion}" if user_opinion else "*User skipped feedback. Architect will decide.*"
        st.session_state.chat_history.append({"role": "user", "content": opinion_text, "avatar": "👤"})
        with st.chat_message("user", avatar="👤"):
            st.markdown(opinion_text)

    # Stream the debate!
    async for chunk in orch.run_phase2_debate(st.session_state.consultant_options, user_opinion):
        source = chunk.source
        meta = AGENT_META.get(source, {"icon": "🤖"})
        avatar = meta["icon"]
        content = chunk.content
        
        with st.chat_message("assistant", avatar=avatar):  # always 'assistant' → left-aligned
            st.markdown(f"**{source.upper()}**\n\n{content}", unsafe_allow_html=True)
            
        st.session_state.chat_history.append({"role": "assistant", "content": f"**{source.upper()}**\n\n{content}", "avatar": avatar})

    st.session_state.phase = 2

# ── Dynamic Input Area ────────────────────────────────────────────────────────
if st.session_state.phase == 0:
    prompt = st.chat_input("Enter your architecture requirement or problem...")
    if prompt:
        # Check API key first
        if not os.environ.get("GEMINI_API_KEY"):
            st.error("🚨 GEMINI_API_KEY environment variable is not set!")
            st.stop()
            
        asyncio.run(run_phase1_async(prompt))
        st.rerun()

elif st.session_state.phase == 1:
    if num_solutions > 1:
        # Human in the loop!
        st.markdown("""
        <div class="hil-banner">
          <span>🧑</span>
          <div>
            <div style="font-size:1.1rem;">⬆️ Review the options above, then type your preference below</div>
            <div style="font-weight:400; font-size:0.88rem; color:#bae6fd; margin-top:4px;">
              Type your preferred option or feedback, or press <strong>Enter</strong> with an empty message to let the Architect decide automatically.
            </div>
          </div>
          <span class="hil-arrow">👇</span>
        </div>
        """, unsafe_allow_html=True)
        opinion = st.chat_input("💬 Your preference here — or press Enter to let the Architect decide...")
        if opinion is not None:
            asyncio.run(run_phase2_async(opinion))
            st.rerun()
    else:
        # If num_solutions == 1, skip straight to phase 2 automatically
        with st.spinner("Starting debate..."):
            asyncio.run(run_phase2_async(""))
            st.rerun()

elif st.session_state.phase == 2:
    st.success("✅ **Debate Concluded!** You can find the transcript inside the `docs/debate_history` folder.")
    if st.button("Start New Topic"):
        st.session_state.chat_history = []
        st.session_state.consultant_options = ""
        st.session_state.phase = 0
        st.session_state.orchestrator = None
        st.rerun()
