import re
from typing import Dict, List


class ContentQualityScorer:
    """
    Score content quality across multiple dimensions.

    Dimensions:
        - readability     : Average sentence length heuristic.
        - structure       : Presence of headers and lists.
        - engagement      : Questions, examples, CTAs, quotes.
        - seo             : Keyword coverage and word-count thresholds.
        - completeness    : Total word-count thresholds.
        - keyword_density : Optimal keyword frequency (1-3 %).
        - tone_consistency: Penalty when informal signals appear in formal passages.

    Contributor note (jackson-marcus):
        Added `keyword_density` and `tone_consistency` metrics with weighted
        integration into the overall score, reading time estimate, and more
        actionable recommendation messages.
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def score_content(self, content: str, keyword: str = None) -> Dict:
        """Generate a comprehensive quality score report."""

        scores = {
            "readability": self._score_readability(content),
            "structure": self._score_structure(content),
            "engagement": self._score_engagement(content),
            "seo": self._score_seo(content, keyword) if keyword else 0,
            "completeness": self._score_completeness(content),
            "keyword_density": (
                self._score_keyword_density(content, keyword) if keyword else 0
            ),
            "tone_consistency": self._score_tone_consistency(content),
        }

        # Weighted average ---------------------------------------------------
        weights = {
            "readability": 0.20,
            "structure": 0.18,
            "engagement": 0.20,
            "seo": 0.12,
            "completeness": 0.12,
            "keyword_density": 0.10,
            "tone_consistency": 0.08,
        }

        overall = sum(scores[k] * weights[k] for k in scores)

        return {
            "overall_score": round(overall, 1),
            "scores": scores,
            "grade": self._get_grade(overall),
            "recommendations": self._get_recommendations(scores),
            "word_count": len(content.split()),
            "reading_time_min": max(1, round(len(content.split()) / 200)),
        }

    # ------------------------------------------------------------------
    # Individual Scorers
    # ------------------------------------------------------------------

    def _score_readability(self, content: str) -> float:
        sentences = len(re.findall(r"[.!?]+", content))
        words = len(content.split())
        if sentences == 0 or words == 0:
            return 0
        avg_sentence_length = words / sentences
        if avg_sentence_length <= 15:
            return 100
        elif avg_sentence_length <= 20:
            return 80
        elif avg_sentence_length <= 25:
            return 60
        else:
            return 40

    def _score_structure(self, content: str) -> float:
        score = 0
        h1_count = len(re.findall(r"^#\s+", content, re.MULTILINE))
        h2_count = len(re.findall(r"^##\s+", content, re.MULTILINE))
        h3_count = len(re.findall(r"^###\s+", content, re.MULTILINE))
        if h1_count == 1:
            score += 20
        if h2_count >= 3:
            score += 30
        if h3_count >= 2:
            score += 20
        if "- " in content or "1. " in content:
            score += 15
        return min(score, 100)

    def _score_engagement(self, content: str) -> float:
        score = 0
        if "?" in content:
            score += 20
        if "example" in content.lower():
            score += 20
        if re.search(r"\d+", content):
            score += 20
        if '"' in content:
            score += 15
        cta_phrases = [
            "learn more",
            "get started",
            "try",
            "discover",
            "explore",
            "take action",
            "find out",
        ]
        if any(phrase in content.lower() for phrase in cta_phrases):
            score += 25
        return min(score, 100)

    def _score_seo(self, content: str, keyword: str) -> float:
        if not keyword:
            return 0
        score = 0
        if keyword.lower() in content.lower():
            score += 50
        word_count = len(content.split())
        if word_count >= 1000:
            score += 50
        return min(score, 100)

    def _score_completeness(self, content: str) -> float:
        word_count = len(content.split())
        if word_count >= 1500:
            return 100
        if word_count >= 1000:
            return 80
        if word_count >= 500:
            return 60
        return 40

    # ------------------------------------------------------------------
    # Additional Scorers (jackson-marcus)
    # ------------------------------------------------------------------

    def _score_keyword_density(self, content: str, keyword: str) -> float:
        """
        Score based on keyword density.
        Optimal range: 1 – 3 % of total words.
        Under-optimized (<1 %) or over-stuffed (>4 %) both lose points.
        """
        if not keyword:
            return 0
        words = content.lower().split()
        total = len(words)
        if total == 0:
            return 0
        keyword_lower = keyword.lower()
        # Count partial matches (keyword phrase can be multi-word)
        kw_words = keyword_lower.split()
        count = 0
        for i in range(len(words) - len(kw_words) + 1):
            if words[i : i + len(kw_words)] == kw_words:
                count += 1
        density = (count / total) * 100
        if 1.0 <= density <= 3.0:
            return 100
        elif 0.5 <= density < 1.0 or 3.0 < density <= 4.0:
            return 70
        elif density > 4.0:
            return 30  # keyword stuffing penalty
        else:
            return 50  # too low

    def _score_tone_consistency(self, content: str) -> float:
        """
        Detect casual/informal signals that indicate inconsistent tone.
        Penalise for slang, excessive exclamation marks, and emoji in body text.
        Returns 100 for clean professional copy, lower if issues found.
        """
        score = 100
        # Excessive exclamation marks (more than 3 in body text)
        exclamations = len(re.findall(r"!", content))
        if exclamations > 5:
            score -= 20
        elif exclamations > 3:
            score -= 10
        # Informal contractions (gonna, wanna, kinda, etc.)
        informal = re.findall(
            r"\b(gonna|wanna|kinda|sorta|gotta|yep|nope|ain't|yeah|lol|omg)\b",
            content,
            re.IGNORECASE,
        )
        score -= min(len(informal) * 10, 40)
        # Emoji in body text (a rough check)
        emoji_pattern = re.compile("[\U00010000-\U0010ffff]", flags=re.UNICODE)
        emoji_hits = len(emoji_pattern.findall(content))
        if emoji_hits > 3:
            score -= 15
        return max(score, 0)

    # ------------------------------------------------------------------
    # Grading & Recommendations
    # ------------------------------------------------------------------

    def _get_grade(self, score: float) -> str:
        """Standard grading rubric."""
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _get_recommendations(self, scores: Dict) -> List[str]:
        recommendations = []
        if scores["readability"] < 70:
            recommendations.append("Use shorter sentences.")
        if scores["structure"] < 70:
            recommendations.append("Add more headers.")
        if scores.get("engagement", 100) < 70:
            recommendations.append("Boost engagement with questions and examples.")
        if scores.get("keyword_density", 100) < 70 and scores.get("seo", 0) > 0:
            recommendations.append("Adjust keyword density to 1-3% of total words.")
        if not recommendations:
            recommendations.append("Content looks great!")
        return recommendations
