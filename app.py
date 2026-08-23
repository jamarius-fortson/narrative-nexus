import time
from datetime import datetime
import markdown
import streamlit as st
from auth import check_authentication
from content_generation_crew import ContentGenerationCrew
from content_templates import (
    build_enriched_topic,
    get_template_meta,
    get_template_names,
    get_tone_meta,
    get_tone_names,
)
from content_versioning import ContentVersionControl
from quality_scorer import ContentQualityScorer

# Page Configuration - NarrativeNexus Rebrand
st.set_page_config(
    page_title="NarrativeNexus | Multi-Agent Editorial Engine",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Authentication Check
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

    /* Tag pill styling */
    .tag-pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.15);
        border: 1px solid rgba(99, 102, 241, 0.35);
        color: #a5b4fc;
        padding: 0.2rem 0.65rem;
        border-radius: 999px;
        font-size: 0.72rem;
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        margin-right: 0.3rem;
        margin-bottom: 0.3rem;
        letter-spacing: 0.03em;
    }

    /* Template card */
    .template-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 14px;
        padding: 0.85rem 1rem;
        margin-bottom: 0.6rem;
        cursor: pointer;
        transition: border-color 0.2s ease;
    }
    .template-card:hover {
        border-color: rgba(99, 102, 241, 0.5);
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

    /* Grade badge */
    .grade-badge {
        display: inline-block;
        font-family: 'Outfit', sans-serif;
        font-size: 2rem;
        font-weight: 800;
        padding: 0.4rem 1.2rem;
        border-radius: 14px;
        background: var(--primary-gradient);
        color: white;
        letter-spacing: 0.05em;
    }
</style>
""",
    unsafe_allow_html=True,
)


# ─────────────────────────────────────────────────────────────────────────────
# Crew Cache
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_resource
def get_crew(model_name="deepseek-chat"):
    return ContentGenerationCrew(model=model_name)


# ─────────────────────────────────────────────────────────────────────────────
# Header
# ─────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<p class="main-header">NarrativeNexus</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-text">Decentralized Intelligence for Professional Content Production</p>',
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Sidebar — Configuration & Intelligence Overview
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ⚙️ Engine Configuration")
    selected_model = st.selectbox(
        "Large Language Model",
        ["deepseek-chat", "gpt-4o", "claude-3-5-sonnet-20240620"],
        index=0,
        help="Select the neural architecture to power the agent reasoning.",
    )

    st.divider()

    # ── Tone & Style Selector (jackson-marcus) ──────────────────────────────
    st.markdown("### 🎙️ Tone & Style")
    tone_names = get_tone_names()
    selected_tone = st.selectbox(
        "Writing Tone",
        tone_names,
        index=0,
        help="Controls the voice and register of the generated content.",
    )
    tone_meta = get_tone_meta(selected_tone)
    st.caption(f"{tone_meta['icon']} {tone_meta['description']}")

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


# ─────────────────────────────────────────────────────────────────────────────
# Input Section
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns([3, 1, 1])

with r1c1:
    topic = st.text_input(
        "Project Objective",
        placeholder="Enter the core topic or thesis for investigation...",
    )

with r1c2:
    content_type = st.selectbox(
        "Output Schema",
        [
            "White Paper",
            "Strategic Blog Post",
            "Technical Narrative",
            "Intelligence Brief",
        ],
    )

with r1c3:
    # ── Industry Template Selector (jackson-marcus) ─────────────────────────
    template_names = get_template_names()
    selected_template = st.selectbox(
        "Industry Template",
        template_names,
        index=template_names.index("General (No Template)"),
        help="Apply an industry-specific framing to your topic.",
    )

tmpl_meta = get_template_meta(selected_template)
if selected_template != "General (No Template)":
    st.info(f"{tmpl_meta['icon']} **{selected_template}**: {tmpl_meta['description']}")

st.markdown("</div>", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# Generation Button
# ─────────────────────────────────────────────────────────────────────────────
if st.button("🚀 ORCHESTRATE GENERATION"):
    if not topic:
        st.warning("Please define a project objective to begin orchestration.")
    else:
        try:
            crew = get_crew(selected_model)

            # Build enriched topic with template + tone context (jackson-marcus)
            enriched_topic = build_enriched_topic(
                topic, selected_template, selected_tone
            )

            with st.status(
                f"🌐 Orchestrating agents with {selected_model}...", expanded=True
            ) as status:
                st.write("📡 Initiating Secure Data Acquisition...")

                start_time = time.time()
                result = crew.generate_content(enriched_topic, content_type)
                end_time = time.time()

                status.update(
                    label="✨ Intelligence Synthesis Complete!",
                    state="complete",
                    expanded=False,
                )

            st.success(
                f"Production cycle completed in {end_time - start_time:.1f} seconds."
            )

            # ── Quality scoring & versioning ────────────────────────────────
            try:
                scorer = ContentQualityScorer()
                quality_results = scorer.score_content(result["final_content"], topic)

                vc = ContentVersionControl()
                # Pass model and tone provenance (jackson-marcus)
                version_id = vc.save_version(
                    topic,
                    result["final_content"],
                    model_used=selected_model,
                    tone=selected_tone,
                )
                # Extract auto-tags (jackson-marcus)
                content_tags = vc.auto_tag(result["final_content"])
            except ImportError:
                quality_results = None
                version_id = None
                content_tags = []

            # ─────────────────────────────────────────────────────────────────
            # Results Tabs
            # ─────────────────────────────────────────────────────────────────
            tab1, tab2, tab3, tab4, tab5 = st.tabs(
                [
                    "📄 Final Narrative",
                    "📊 Production Analytics",
                    "⭐ Quality Governance",
                    "🏷️ Tags & Provenance",
                    "📜 History",
                ]
            )

            # ── Tab 1: Final Narrative ───────────────────────────────────────
            with tab1:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                st.markdown(result["final_content"])
                st.markdown("</div>", unsafe_allow_html=True)

                dl_col1, dl_col2, dl_col3 = st.columns(3)

                with dl_col1:
                    st.download_button(
                        label="📥 Export to Markdown",
                        data=result["final_content"],
                        file_name=f"NarrativeNexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown",
                    )

                with dl_col2:
                    # ── HTML Export (jackson-marcus) ─────────────────────────
                    html_body = markdown.markdown(
                        result["final_content"], extensions=["tables", "fenced_code"]
                    )
                    full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{topic}</title>
    <style>
        body {{ font-family: 'Segoe UI', sans-serif; max-width: 860px; margin: 3rem auto; padding: 0 1.5rem; color: #1e293b; line-height: 1.8; }}
        h1,h2,h3 {{ color: #4f46e5; }}
        code {{ background: #f1f5f9; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }}
        pre {{ background: #f1f5f9; padding: 1rem; border-radius: 8px; overflow-x: auto; }}
        blockquote {{ border-left: 4px solid #6366f1; margin-left: 0; padding-left: 1rem; color: #64748b; }}
        table {{ border-collapse: collapse; width: 100%; }}
        th, td {{ border: 1px solid #e2e8f0; padding: 0.5rem 0.75rem; text-align: left; }}
        th {{ background: #f8fafc; }}
    </style>
</head>
<body>
{html_body}
<hr>
<footer style="color:#94a3b8;font-size:0.8rem;margin-top:2rem;">
  Generated by NarrativeNexus &middot; {datetime.now().strftime('%B %d, %Y')} &middot; Model: {selected_model}
</footer>
</body>
</html>"""
                    st.download_button(
                        label="🌐 Export to HTML",
                        data=full_html,
                        file_name=f"NarrativeNexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
                        mime="text/html",
                    )

                with dl_col3:
                    # ── Plain Text Export (jackson-marcus) ───────────────────
                    import re as _re

                    plain_text = _re.sub(r"[#*`_>\[\]!]", "", result["final_content"])
                    st.download_button(
                        label="📋 Export to Plain Text",
                        data=plain_text,
                        file_name=f"NarrativeNexus_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
                        mime="text/plain",
                    )

            # ── Tab 2: Production Analytics ──────────────────────────────────
            with tab2:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Node Count", result["agents_used"], "Active Agents")
                m2.metric(
                    "Sequential Steps", result["tasks_completed"], "Verified Tasks"
                )
                m3.metric(
                    "Word Velocity",
                    len(result["final_content"].split()),
                    "Words Generated",
                )
                # Reading time metric (jackson-marcus)
                reading_time = max(1, round(len(result["final_content"].split()) / 200))
                m4.metric("Reading Time", f"{reading_time} min", "Estimated")

                st.divider()
                st.markdown(f"**🎙️ Tone Applied:** `{selected_tone}`")
                st.markdown(f"**🏭 Industry Template:** `{selected_template}`")
                st.markdown(f"**🤖 Model Used:** `{selected_model}`")
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Tab 3: Quality Governance ────────────────────────────────────
            with tab3:
                if quality_results:
                    st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)

                    gc1, gc2 = st.columns([1, 3])
                    with gc1:
                        st.markdown(
                            f'<span class="grade-badge">{quality_results["grade"]}</span>',
                            unsafe_allow_html=True,
                        )
                        st.caption("Governance Grade")
                    with gc2:
                        st.markdown(
                            f"**Overall Score: {quality_results['overall_score']} / 100**"
                        )
                        st.progress(quality_results["overall_score"] / 100)

                    st.divider()

                    # Extended metrics (jackson-marcus)
                    sc = quality_results["scores"]
                    m_cols = st.columns(4)
                    m_cols[0].metric("Linguistic Clarity", sc["readability"])
                    m_cols[1].metric("Logical Structure", sc["structure"])
                    m_cols[2].metric("Strategic Engagement", sc["engagement"])
                    m_cols[3].metric("SEO Coverage", sc["seo"])

                    m_cols2 = st.columns(3)
                    m_cols2[0].metric("Keyword Density", sc.get("keyword_density", "—"))
                    m_cols2[1].metric(
                        "Tone Consistency", sc.get("tone_consistency", "—")
                    )
                    m_cols2[2].metric("Content Completeness", sc["completeness"])

                    st.markdown("#### 📋 Strategic Recommendations")
                    for rec in quality_results["recommendations"]:
                        st.markdown(f"- {rec}")
                    st.markdown("</div>", unsafe_allow_html=True)
                else:
                    st.info("Quality governance module not initialized.")

            # ── Tab 4: Tags & Provenance (jackson-marcus) ────────────────────
            with tab4:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                st.markdown("#### 🏷️ Auto-Generated Content Tags")
                if content_tags:
                    tags_html = "".join(
                        f'<span class="tag-pill">#{tag}</span>' for tag in content_tags
                    )
                    st.markdown(tags_html, unsafe_allow_html=True)
                else:
                    st.caption("No tags extracted.")

                st.divider()
                st.markdown("#### 🔍 Generation Provenance")
                prov_col1, prov_col2, prov_col3 = st.columns(3)
                prov_col1.markdown(f"**LLM Model**\n\n`{selected_model}`")
                prov_col2.markdown(f"**Tone Style**\n\n`{selected_tone}`")
                prov_col3.markdown(f"**Industry Template**\n\n`{selected_template}`")
                st.caption(
                    f"Generated on {datetime.now().strftime('%A, %B %d %Y at %H:%M:%S')}"
                )
                st.markdown("</div>", unsafe_allow_html=True)

            # ── Tab 5: History ───────────────────────────────────────────────
            with tab5:
                st.markdown('<div class="nexus-panel">', unsafe_allow_html=True)
                if version_id:
                    history = vc.get_history(topic)
                    if history:
                        for entry in history:
                            tag_pills = "".join(
                                f'<span class="tag-pill">#{t}</span>'
                                for t in (entry.get("tags") or [])
                            )
                            st.markdown(
                                f"""
                                <div style="padding:0.75rem 1rem; border-radius:12px;
                                            background:rgba(255,255,255,0.04);
                                            border:1px solid rgba(255,255,255,0.08);
                                            margin-bottom:0.6rem;">
                                  <strong style="color:#a5b4fc">v{entry['version']}</strong>
                                  &nbsp;·&nbsp;
                                  <span style="color:#94a3b8;font-size:0.85rem;">{entry['date']}</span>
                                  &nbsp;·&nbsp;
                                  <span style="color:#64748b;font-size:0.8rem;">
                                    {entry['words']} words &nbsp;|&nbsp;
                                    Model: {entry.get('model','—')} &nbsp;|&nbsp;
                                    Tone: {entry.get('tone','—')}
                                  </span>
                                  <br>{tag_pills}
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )
                    else:
                        st.info("No history entries yet for this topic.")
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
