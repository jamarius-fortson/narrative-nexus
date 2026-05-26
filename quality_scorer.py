import re
from typing import Dict, List

class ContentQualityScorer:
    """Score content quality across multiple dimensions"""
    
    def score_content(self, content: str, keyword: str = None) -> Dict:
        """Generate comprehensive quality score"""
        
        scores = {
            "readability": self._score_readability(content),
            "structure": self._score_structure(content),
            "engagement": self._score_engagement(content),
            "seo": self._score_seo(content, keyword) if keyword else 0,
            "completeness": self._score_completeness(content)
        }
        
        # Overall score (weighted average)
        weights = {
            "readability": 0.25,
            "structure": 0.20,
            "engagement": 0.25,
            "seo": 0.15,
            "completeness": 0.15
        }
        
        overall = sum(scores[k] * weights[k] for k in scores)
        
        return {
            "overall_score": round(overall, 1),
            "scores": scores,
            "grade": self._get_grade(overall),
            "recommendations": self._get_recommendations(scores)
        }
    
    def _score_readability(self, content: str) -> float:
        sentences = len(re.findall(r'[.!?]+', content))
        words = len(content.split())
        if sentences == 0 or words == 0: return 0
        avg_sentence_length = words / sentences
        if avg_sentence_length <= 15: score = 100
        elif avg_sentence_length <= 20: score = 80
        elif avg_sentence_length <= 25: score = 60
        else: score = 40
        return score
    
    def _score_structure(self, content: str) -> float:
        score = 0
        h1_count = content.count('# ')
        h2_count = content.count('## ')
        h3_count = content.count('### ')
        if h1_count == 1: score += 20
        if h2_count >= 3: score += 30
        if h3_count >= 2: score += 20
        if '- ' in content or '1. ' in content: score += 15
        return min(score, 100)
    
    def _score_engagement(self, content: str) -> float:
        score = 0
        if '?' in content: score += 20
        if 'example' in content.lower(): score += 20
        if re.search(r'\d+', content): score += 20
        if '"' in content: score += 15
        cta_phrases = ['learn more', 'get started', 'try', 'discover']
        if any(phrase in content.lower() for phrase in cta_phrases): score += 25
        return min(score, 100)
    
    def _score_seo(self, content: str, keyword: str) -> float:
        if not keyword: return 0
        score = 0
        if keyword.lower() in content.lower(): score += 50
        word_count = len(content.split())
        if word_count >= 1000: score += 50
        return min(score, 100)
    
    def _score_completeness(self, content: str) -> float:
        word_count = len(content.split())
        if word_count >= 1500: return 100
        if word_count >= 1000: return 80
        if word_count >= 500: return 60
        return 40
    
    def _get_grade(self, score: float) -> str:
        if score >= 90: return "A"
        elif score >= 80: return "B"
        elif score >= 70: return "C"
        elif score >= 60: return "D"
        else: return "F"
    
    def _get_recommendations(self, scores: Dict) -> List[str]:
        recommendations = []
        if scores["readability"] < 70: recommendations.append("Use shorter sentences.")
        if scores["structure"] < 70: recommendations.append("Add more headers.")
        if not recommendations: recommendations.append("Content looks great!")
        return recommendations
