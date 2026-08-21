import streamlit as st
from content_generation_crew import ContentGenerationCrew
import time
from datetime import datetime
import markdown

# Page Configuration - NarrativeNexus Rebrand
st.set_page_config(
    page_title="NarrativeNexus | Multi-Agent Editorial Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Authentication Check
from auth import check_authentication

if not check_authentication():
    st.stop()

# Custom CSS for NarrativeNexus Premium Design System (High-End Dark Mode & Glassmorphism)
st.markdown(
    """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@400;500;600&display=swap');
    
    :root {
        --primary-gradient: linear-gradient(135deg, #6366f1 0%, #a855f7 100%);
        --accent-color: #f43f5e;
        --bg-color: #0f172a;
        --card-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.1);
    }

    body {
        font-family: 'Inter', sans-serif;
        background-color: var(--bg-color);
    }

    .main-header {
        font-family: 'Outfit', sans-serif;
        font-size: 3.5rem;
        font-weight: 800;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
        text-align: left;
        letter-spacing: -0.02em;
    }
    
    .sub-text {
        font-family: 'Outfit', sans-serif;
        color: #94a3b8;
        font-size: 1.25rem;
        text-align: left;
        margin-bottom: 3rem;
        font-weight: 400;
    }

    /* Glass Panels */
    .nexus-panel {
        background: var(--card-bg);
        border: 1px solid var(--glass-border);
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 24px;
        margin-bottom: 1.5rem;
        transition: all 0.3s ease;
    }

    .nexus-panel:hover {
        border-color: rgba(99, 102, 241, 0.4);
        box-shadow: 0 10px 30px -15px rgba(0, 0, 0, 0.3);
    }

    /* Agent Identity Cards */
    .agent-id-card {
        background: rgba(255, 255, 255, 0.05);
        padding: 1rem 1.25rem;
        border-radius: 16px;
        margin-bottom: 0.75rem;
        border-left: 4px solid #6366f1;
        display: flex;
        align-items: center;
        gap: 1rem;
    }

    .agent-icon {
        font-size: 1.5rem;
        background: rgba(99, 102, 241, 0.1);
        padding: 0.5rem;
        border-radius: 12px;
    }

    /* Buttons */
    .stButton>button {
        background: var(--primary-gradient);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 14px;
        font-weight: 600;
        font-family: 'Outfit', sans-serif;
        letter-spacing: 0.5px;
        width: 100%;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 15px 35px -10px rgba(99, 102, 241, 0.5);
    }
    
    .stButton>button:hover {
        transform: translateY(-5px);
        box-shadow: 0 20px 40px -10px rgba(99, 102, 241, 0.6);
    }

    /* Metrics UI */
    [data-testid="stMetricValue"] {
        font-family: 'Outfit', sans-serif;
        font-weight: 700;
        color: #f8fafc !important;
    }

    /* Tabs Customization */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: transparent;
        border-bottom: 2px solid transparent;
        color: #94a3b8;
        font-weight: 600;
        transition: all 0.3s;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: #6366f1;
    }

    .stTabs [aria-selected="true"] {
        color: #6366f1 !important;
        border-bottom-color: #6366f1 !important;
    }
</style>
""",
    unsafe_allow_html=True,
)


# Initialize crew
@st.cache_resource
def get_crew(model_name="deepseek-chat"):
    return ContentGenerationCrew(model=model_name)


# Layout
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="main-header">NarrativeNexus</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-text">Decentralized Intelligence for Professional Content Production</p>',
        unsafe_allow_html=True,
    )

# Sidebar - Configuration & Intelligence Overview
with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")
    selected_model = st.selectbox(
        "Large Language Model",
        ["deepseek-chat", "gpt-4o", "claude-3-5-sonnet-20240620"],
        index=0,
        help="Select the neural architecture to power the agent reasoning.",
    )

    st.divider()
    st.markdown("### 🤖 The Intelligence Nexus")
    agents_info = [
        ("🔍", "Strategic Researcher", "Data Acquisition"),
        ("✍️", "Narrative Architect", "Content Synthesis"),
        ("📝", "Executive Editor", "Quality Control"),
        ("✅", "Integrity Scout", "Fact Verification"),
        ("📈", "Growth Strategist", "SEO & Distribution"),
    ]

    for icon, name, role in agents_info:
        st.markdown(
            f"""
        <div class="agent-id-card">
            <div class="agent-icon">{icon}</div>
            <div>
                <div style="font-weight: 700; font-size: 0.95rem; color: #f8fafc;">{name}</div>
                <div style="font-size: 0.75rem; color: #94a3b8;">{role}</div>
            </div>
        </div>
        """,
            unsafe_allow_html=True,
        )

# Inputs Section
st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
c1, c2 = st.columns([3, 1])
with c1:
    topic = st.text_input(
        "Project Objective",
        placeholder="Enter the core topic or thesis for investigation...",
    )
with c2:
    content_type = st.selectbox(
        "Output Schema",
        [
            "White Paper",
            "Strategic Blog Post",
            "Technical Narrative",
            "Intelligence Brief",
        ],
    )
st.markdown("</div>", unsafe_allow_html=True)

if st.button("🚀 ORCHESTRATE GENERATION"):
    if not topic:
        st.warning("Please define a project objective to begin orchestration.")
    else:
        try:
            # Re-initialize crew with selected model
            crew = get_crew(selected_model)

            with st.status(
                f"🌐 Orchestrating agents with {selected_model}...", expanded=True
            ) as status:
                st.write("📡 Initiating Secure Data Acquisition...")

                start_time = time.time()
                # Ensure the crew class supports the model parameter
                result = crew.generate_content(topic, content_type)
                end_time = time.time()

                status.update(
                    label="✨ Intelligence Synthesis Complete!",
                    state="complete",
                    expanded=False,
                )

            # Analytics & Content Rendering
            st.success(
                f"Production cycle completed in {end_time - start_time:.1f} seconds."
            )

            # Logic for scoring and saving (assuming these classes are available)
            try:
                from quality_scorer import ContentQualityScorer
                from content_versioning import ContentVersionControl

                scorer = ContentQualityScorer()
                quality_results = scorer.score_content(result["final_content"], topic)

                vc = ContentVersionControl()
                version_id = vc.save_version(topic, result["final_content"])
            except ImportError:
                quality_results = None
                version_id = None

            # Results Display
            tab1, tab2, tab3, tab4 = st.tabs(
                [
                    "📄 Final Narrative",
                    "📊 Production Analytics",
                    "⭐ Quality Governance",
                    "📜 History",
                ]
            )

            with tab1:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                st.markdown(result["final_content"])
                st.markdown("</div>", unsafe_allow_html=True)

                st.download_button(
                    label="📥 Export to Markdown",
                    data=result["final_content"],
                    file_name=f"NarrativeNexus_{datetime.now().strftime('%Y%m%d')}.md",
                    mime="text/markdown",
                )

            with tab2:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                m1, m2, m3 = st.columns(3)
                m1.metric("Node Count", result["agents_used"], "Active Agents")
                m2.metric(
                    "Sequential Steps", result["tasks_completed"], "Verified Tasks"
                )
                m3.metric(
                    "Word Velocity",
                    len(result["final_content"].split()),
                    "Words Generated",
                )
                st.markdown("</div>", unsafe_allow_html=True)

            with tab3:
                if quality_results:
                    st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                    st.markdown(
                        f"### Governance Rating: **{quality_results['grade']}**"
                    )
                    st.progress(quality_results["overall_score"] / 100)

                    c1, c2, c3 = st.columns(3)
                    c1.metric(
                        "Linguistic Clarity", quality_results["scores"]["readability"]
                    )
                    c2.metric(
                        "Logical Structure", quality_results["scores"]["structure"]
                    )
                    c3.metric(
                        "Strategic Engagement", quality_results["scores"]["engagement"]
                    )

                    st.markdown("#### Strategic Recommendations")
                    for rec in quality_results["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Quality governance module not initialized.")

            with tab4:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                if version_id:
                    history = vc.get_history(topic)
                    st.table(history)
                else:
                    st.info("No historical data available for this objective.")
                st.markdown("</div>", unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Orchestration Failure: {str(e)}")
            st.exception(e)

st.markdown("---")
st.markdown(
    f'<p style="text-align: center; color: #64748b; font-size: 0.8rem;">© {datetime.now().year} NarrativeNexus | Advanced Multi-Agent Intelligence Platform</p>',
    unsafe_allow_html=True,
)
