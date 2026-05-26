import pytest
from content_generation_crew import ContentGenerationCrew
from quality_scorer import ContentQualityScorer

def test_crew_initialization():
    crew = ContentGenerationCrew()
    assert crew.llm is not None
    assert len(crew.agents) == 5

def test_quality_scorer():
    scorer = ContentQualityScorer()
    content = "# Test\nThis is a test content with enough words to pass some basic checks. It has a header and some sentences."
    results = scorer.score_content(content, "Test")
    assert "overall_score" in results
    assert results["overall_score"] > 0
    assert results["grade"] in ["A", "B", "C", "D", "F"]

def test_agent_roles():
    crew = ContentGenerationCrew()
    roles = [agent.role for agent in crew.agents.values()]
    assert "Senior Research Analyst" in roles
    assert "Expert Content Writer" in roles
