"""
content_templates.py
--------------------
Pre-built content templates and tone/style configurations for NarrativeNexus.

Contributor: jackson-marcus
"""

from typing import Dict, List

# ---------------------------------------------------------------------------
# Industry Content Templates
# ---------------------------------------------------------------------------

CONTENT_TEMPLATES: Dict[str, Dict] = {
    "Technology & AI": {
        "icon": "🤖",
        "description": "Deep-dives into emerging tech, AI breakthroughs, and software trends.",
        "prompt_prefix": (
            "Focus on technical accuracy, innovation implications, and real-world adoption. "
            "Include benchmark data, GitHub stats where relevant, and developer ecosystem insights."
        ),
        "suggested_types": ["Technical Narrative", "White Paper", "Intelligence Brief"],
        "tone": "Analytical",
    },
    "Finance & Investment": {
        "icon": "📈",
        "description": "Market analysis, investment strategy, and fintech innovation.",
        "prompt_prefix": (
            "Include macroeconomic context, risk/reward analysis, regulatory implications, "
            "and cite reputable financial sources (Bloomberg, Reuters, SEC filings)."
        ),
        "suggested_types": ["Intelligence Brief", "White Paper", "Strategic Blog Post"],
        "tone": "Professional",
    },
    "Health & Wellness": {
        "icon": "🏥",
        "description": "Medical research, wellness trends, and healthcare technology.",
        "prompt_prefix": (
            "Cite peer-reviewed studies, include expert medical commentary, "
            "and always add appropriate disclaimers. Prioritize evidence-based claims."
        ),
        "suggested_types": [
            "Technical Narrative",
            "Strategic Blog Post",
            "White Paper",
        ],
        "tone": "Authoritative",
    },
    "Marketing & Growth": {
        "icon": "🎯",
        "description": "Growth strategies, brand storytelling, and marketing campaigns.",
        "prompt_prefix": (
            "Focus on actionable frameworks, real case studies, conversion metrics, "
            "and audience psychology. Include calls-to-action and distribution strategies."
        ),
        "suggested_types": [
            "Strategic Blog Post",
            "Intelligence Brief",
            "Technical Narrative",
        ],
        "tone": "Persuasive",
    },
    "Sustainability & ESG": {
        "icon": "🌱",
        "description": "Climate tech, ESG investing, and green innovation.",
        "prompt_prefix": (
            "Ground content in IPCC reports, ESG frameworks, and verified carbon data. "
            "Highlight both challenges and scalable solutions. Avoid greenwashing."
        ),
        "suggested_types": ["White Paper", "Intelligence Brief", "Strategic Blog Post"],
        "tone": "Balanced",
    },
    "General (No Template)": {
        "icon": "📝",
        "description": "No industry-specific framing applied.",
        "prompt_prefix": "",
        "suggested_types": [
            "White Paper",
            "Strategic Blog Post",
            "Technical Narrative",
            "Intelligence Brief",
        ],
        "tone": "Professional",
    },
}


# ---------------------------------------------------------------------------
# Tone & Style Definitions
# ---------------------------------------------------------------------------

TONE_STYLES: Dict[str, Dict] = {
    "Professional": {
        "icon": "💼",
        "description": "Formal, data-driven, authoritative. Ideal for B2B and enterprise audiences.",
        "instruction": (
            "Write in a formal, authoritative tone. Use precise vocabulary, avoid contractions, "
            "and maintain an objective perspective. Structure arguments logically with supporting evidence."
        ),
    },
    "Conversational": {
        "icon": "💬",
        "description": "Friendly, accessible, relatable. Great for blogs and consumer content.",
        "instruction": (
            "Write in a warm, conversational tone. Use contractions naturally, speak directly to the reader, "
            "and use relatable analogies. Make complex ideas feel approachable without dumbing them down."
        ),
    },
    "Academic": {
        "icon": "🎓",
        "description": "Scholarly, citation-heavy, rigorous. Suitable for research papers and white papers.",
        "instruction": (
            "Write with scholarly rigor. Use formal academic register, passive voice where appropriate, "
            "precise terminology, and extensive citation of primary sources. Maintain critical distance."
        ),
    },
    "Creative & Narrative": {
        "icon": "✨",
        "description": "Story-driven, vivid, engaging. Perfect for thought leadership and brand storytelling.",
        "instruction": (
            "Write with narrative flair. Open with a compelling story or vivid scene. "
            "Use metaphors, analogies, and varied sentence rhythm. Make the content feel like a journey."
        ),
    },
    "Analytical": {
        "icon": "🔬",
        "description": "Data-forward, structured, precise. Best for technical reports and market analysis.",
        "instruction": (
            "Lead with data and structured analysis. Use clear headers, bullet points, and comparative tables. "
            "Every claim must be backed by quantifiable evidence. Minimize editorial opinion."
        ),
    },
}


# ---------------------------------------------------------------------------
# Helper Functions
# ---------------------------------------------------------------------------


def get_template_names() -> List[str]:
    """Return list of all available template names."""
    return list(CONTENT_TEMPLATES.keys())


def get_tone_names() -> List[str]:
    """Return list of all available tone names."""
    return list(TONE_STYLES.keys())


def build_enriched_topic(
    topic: str,
    template_name: str,
    tone_name: str,
) -> str:
    """
    Combines the raw topic with template context and tone instructions
    to produce an enriched prompt string for the agent crew.

    Args:
        topic: The raw user-supplied topic string.
        template_name: Selected industry template key.
        tone_name: Selected tone/style key.

    Returns:
        Enriched topic string ready for content generation.
    """
    template = CONTENT_TEMPLATES.get(
        template_name, CONTENT_TEMPLATES["General (No Template)"]
    )
    tone = TONE_STYLES.get(tone_name, TONE_STYLES["Professional"])

    parts = [topic]

    if template["prompt_prefix"]:
        parts.append(f"\n\n[Industry Context]: {template['prompt_prefix']}")

    parts.append(f"\n[Tone & Style]: {tone['instruction']}")

    return "".join(parts)


def get_template_meta(template_name: str) -> Dict:
    """Return metadata for a given template."""
    return CONTENT_TEMPLATES.get(
        template_name, CONTENT_TEMPLATES["General (No Template)"]
    )


def get_tone_meta(tone_name: str) -> Dict:
    """Return metadata for a given tone."""
    return TONE_STYLES.get(tone_name, TONE_STYLES["Professional"])
