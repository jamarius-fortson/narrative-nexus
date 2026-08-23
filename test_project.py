import os
import sqlite3
import pytest
from unittest.mock import patch, MagicMock
from content_generation_crew import ContentGenerationCrew, get_default_llm
from quality_scorer import ContentQualityScorer
from content_versioning import ContentVersionControl
from custom_tools import search_tool
from auth import get_auth_config_from_env, check_authentication
from logger import log_progress

# ==========================================
# Content Generation Crew Tests
# ==========================================


def test_crew_initialization():
    crew = ContentGenerationCrew()
    assert crew.llm is not None
    assert len(crew.agents) == 5
    assert crew.model_name == "deepseek-chat"


def test_agent_roles():
    crew = ContentGenerationCrew()
    roles = [agent.role for agent in crew.agents.values()]
    assert "Senior Research Analyst" in roles
    assert "Expert Content Writer" in roles
    assert "Senior Content Editor" in roles
    assert "Professional Fact Checker" in roles
    assert "SEO Optimization Expert" in roles


def test_crew_tasks_creation():
    crew = ContentGenerationCrew()
    tasks = crew._create_tasks(
        topic="Artificial Intelligence", content_type="blog_post"
    )
    assert len(tasks) == 6
    # Verify task agents
    assert tasks[0].agent == crew.agents["researcher"]
    assert tasks[1].agent == crew.agents["writer"]
    assert tasks[2].agent == crew.agents["writer"]
    assert tasks[3].agent == crew.agents["editor"]
    assert tasks[4].agent == crew.agents["fact_checker"]
    assert tasks[5].agent == crew.agents["seo_specialist"]


def test_get_default_llm_variants():
    deepseek_llm = get_default_llm("deepseek-chat")
    assert deepseek_llm is not None

    gpt_llm = get_default_llm("gpt-4o")
    assert gpt_llm is not None

    fallback_llm = get_default_llm("unknown-model")
    assert fallback_llm is not None


# ==========================================
# Quality Scorer Tests
# ==========================================


def test_quality_scorer_basic():
    scorer = ContentQualityScorer()
    content = (
        "# Main Title\n"
        "## Section 1\n"
        "This is an engaging guide.\n"
        "## Section 2\n"
        'Here is an example with 100% data and "quotes".\n'
        "## Section 3\n"
        "- Item 1\n"
        "- Item 2\n"
        "Try to learn more today!"
    )
    results = scorer.score_content(content, "guide")
    assert "overall_score" in results
    assert results["overall_score"] > 0
    assert results["grade"] in ["A", "B", "C", "D", "F"]
    assert "scores" in results
    assert "recommendations" in results


def test_quality_scorer_readability():
    scorer = ContentQualityScorer()
    # Short sentences -> high readability
    short_content = "This is good. It is easy. We love this. Simple words work."
    score_short = scorer._score_readability(short_content)
    assert score_short >= 80

    # Empty content
    assert scorer._score_readability("") == 0


def test_quality_scorer_structure():
    scorer = ContentQualityScorer()
    content = "# Title\n## S1\n## S2\n## S3\n### Sub1\n### Sub2\n- list item"
    score = scorer._score_structure(content)
    assert score >= 80


def test_quality_scorer_engagement():
    scorer = ContentQualityScorer()
    engaging_content = 'Do you want an example? Here are 42 tips. "Success is key." Try to get started!'
    score = scorer._score_engagement(engaging_content)
    assert score == 100


def test_quality_scorer_seo():
    scorer = ContentQualityScorer()
    # No keyword
    assert scorer._score_seo("Some content", None) == 0

    # With keyword
    seo_score = scorer._score_seo("The best AI tools in 2026.", "AI tools")
    assert seo_score >= 50


def test_quality_scorer_completeness():
    scorer = ContentQualityScorer()
    assert scorer._score_completeness("word " * 1600) == 100
    assert scorer._score_completeness("word " * 1100) == 80
    assert scorer._score_completeness("word " * 600) == 60
    assert scorer._score_completeness("word " * 100) == 40


def test_quality_scorer_grades():
    scorer = ContentQualityScorer()
    assert scorer._get_grade(95) == "A"
    assert scorer._get_grade(85) == "B"
    assert scorer._get_grade(75) == "C"
    assert scorer._get_grade(65) == "D"
    assert scorer._get_grade(50) == "F"


# ==========================================
# Content Version Control Tests
# ==========================================


def test_version_control(tmp_path):
    db_file = str(tmp_path / "test_versions.db")
    vc = ContentVersionControl(db_path=db_file)

    # Save initial version
    v1 = vc.save_version("post_1", "Initial blog content with 5 words.")
    assert v1 == 1

    # Save second version
    v2 = vc.save_version(
        "post_1", "Updated blog content with more detailed information."
    )
    assert v2 == 2

    # Get history
    history = vc.get_history("post_1")
    assert len(history) == 2
    assert history[0]["version"] == 2
    assert history[1]["version"] == 1
    assert history[0]["words"] > 0


# ==========================================
# Custom Tools Tests
# ==========================================


def test_search_tool_success():
    with patch("custom_tools.DuckDuckGoSearchRun") as MockSearch:
        mock_instance = MagicMock()
        mock_instance.run.return_value = "Search results for query"
        MockSearch.return_value = mock_instance

        result = search_tool.func("test query")
        assert "Search results for query" in result


def test_search_tool_error_handling():
    with patch("custom_tools.DuckDuckGoSearchRun") as MockSearch:
        mock_instance = MagicMock()
        mock_instance.run.side_effect = Exception("Connection timeout")
        MockSearch.return_value = mock_instance

        result = search_tool.func("error query")
        assert "Error searching" in result


# ==========================================
# Auth Module Tests
# ==========================================


def test_auth_config_from_env(monkeypatch):
    monkeypatch.setenv("APP_USERNAME", "testadmin")
    monkeypatch.setenv("APP_PASSWORD", "secret123")
    monkeypatch.setenv("APP_SECRET_KEY", "securecookiekey")

    config = get_auth_config_from_env()
    assert "credentials" in config
    assert "testadmin" in config["credentials"]["usernames"]
    assert config["cookie"]["key"] == "securecookiekey"


def test_auth_disabled_bypass(monkeypatch):
    monkeypatch.setenv("ENABLE_AUTH", "false")
    assert check_authentication() is True
    from auth import setup_auth

    auth_obj, name, status, username = setup_auth()
    assert auth_obj is None
    assert name == "Dev User"
    assert status is True
    assert username == "dev"


def test_quality_scorer_readability_tiers():
    scorer = ContentQualityScorer()
    # <= 20 words/sentence
    content_20 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen."
    assert scorer._score_readability(content_20) == 80

    # <= 25 words/sentence
    content_25 = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo."
    assert scorer._score_readability(content_25) == 60

    # > 25 words/sentence
    content_long = "One two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen twenty twentyone twentytwo twentythree twentyfour twentyfive twentysix."
    assert scorer._score_readability(content_long) == 40


# ==========================================
# Logger Module Tests
# ==========================================


def test_log_progress(tmp_path, monkeypatch):
    log_file = str(tmp_path / "test_log.txt")
    monkeypatch.setenv("LOG_FILE_PATH", log_file)

    log_progress("Test log entry message")
    assert os.path.exists(log_file)
    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
    assert "Test log entry message" in content


# ==========================================
# Content Templates Tests (jackson-marcus)
# ==========================================


def test_content_templates_meta():
    from content_templates import (
        CONTENT_TEMPLATES,
        TONE_STYLES,
        get_template_names,
        get_tone_names,
        get_template_meta,
        get_tone_meta,
        build_enriched_topic,
    )

    templates = get_template_names()
    assert "Technology & AI" in templates
    assert "Finance & Investment" in templates
    assert "General (No Template)" in templates

    tones = get_tone_names()
    assert "Professional" in tones
    assert "Conversational" in tones
    assert "Academic" in tones

    meta = get_template_meta("Technology & AI")
    assert meta["icon"] == "🤖"
    assert "prompt_prefix" in meta

    tone_meta = get_tone_meta("Professional")
    assert "instruction" in tone_meta

    # Test enriched prompt construction
    enriched = build_enriched_topic(
        "Quantum Computing", "Technology & AI", "Analytical"
    )
    assert "Quantum Computing" in enriched
    assert "[Industry Context]" in enriched
    assert "[Tone & Style]" in enriched

    # General template without extra prefix
    enriched_gen = build_enriched_topic(
        "Simple Topic", "General (No Template)", "Conversational"
    )
    assert "Simple Topic" in enriched_gen
    assert "[Industry Context]" not in enriched_gen
    assert "[Tone & Style]" in enriched_gen


# ==========================================
# Content Versioning Extensions (jackson-marcus)
# ==========================================


def test_content_versioning_extensions(tmp_path):
    db_file = str(tmp_path / "test_versions_ext.db")
    vc = ContentVersionControl(db_path=db_file)

    sample_content = (
        "# Artificial Intelligence Revolution\n"
        "## Neural Networks and Deep Learning\n"
        "## Generative Architecture\n"
        "AI is transforming industries rapidly with neural networks."
    )

    tags = vc.auto_tag(sample_content)
    assert isinstance(tags, list)
    assert len(tags) > 0
    assert any("intelligence" in t or "artificial" in t or "neural" in t for t in tags)

    v1 = vc.save_version(
        "ai_topic", sample_content, model_used="gpt-4o", tone="Academic"
    )
    assert v1 == 1

    history = vc.get_history("ai_topic")
    assert len(history) == 1
    assert history[0]["model"] == "gpt-4o"
    assert history[0]["tone"] == "Academic"
    assert isinstance(history[0]["tags"], list)

    # Test content retrieval
    retrieved = vc.get_version_content("ai_topic", 1)
    assert retrieved == sample_content

    # Test list of topics
    topics = vc.get_all_topics()
    assert "ai_topic" in topics


# ==========================================
# Quality Scorer Extensions (jackson-marcus)
# ==========================================


def test_quality_scorer_extensions():
    scorer = ContentQualityScorer()

    sample = (
        "# Overview of Next-Gen Architecture\n"
        "## Core Principles\n"
        "## Implementation Strategy\n"
        "### Technical Details\n"
        "### Benchmarking\n"
        "Is this system scalable? For example, in 2026 we saw 99.9% uptime. "
        '"Reliability is paramount." Try to get started today!\n'
        "- Point 1\n- Point 2\n" + ("Architecture is modern and robust. " * 80)
    )

    report = scorer.score_content(sample, keyword="Architecture")
    assert "overall_score" in report
    assert "scores" in report
    assert "grade" in report
    assert "word_count" in report
    assert "reading_time_min" in report
    assert report["word_count"] > 0
    assert report["reading_time_min"] >= 1
    assert "keyword_density" in report["scores"]
    assert "tone_consistency" in report["scores"]
    assert report["scores"]["tone_consistency"] == 100

