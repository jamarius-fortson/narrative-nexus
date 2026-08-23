import sqlite3
import hashlib
import json
import re
from datetime import datetime
from typing import List, Dict, Optional


class ContentVersionControl:
    """
    Track content versions and changes using SQLite.

    Enhancement (jackson-marcus):
        - Added `tags` column to content_versions for auto-tagging.
        - Added `model_used` and `tone` provenance columns.
        - New `get_version_content()` method to retrieve full content of a version.
        - New `auto_tag()` static helper that extracts topic tags from content.
        - `get_history()` now returns tags in the result set.
    """

    def __init__(self, db_path: str = "content_versions.db"):
        self.db_path = db_path
        self._create_tables()

    # ------------------------------------------------------------------
    # Schema Management
    # ------------------------------------------------------------------

    def _create_tables(self):
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS content_versions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content_id TEXT NOT NULL,
                version INTEGER NOT NULL,
                content TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                word_count INTEGER,
                tags TEXT,
                model_used TEXT,
                tone TEXT
            )
            """)
            # Migrate: add new columns if they don't exist yet (safe for existing DBs)
            existing_cols = {
                row[1] for row in cursor.execute("PRAGMA table_info(content_versions)")
            }
            migration_cols = {
                "tags":       "TEXT",
                "model_used": "TEXT",
                "tone":       "TEXT",
            }
            for col, col_type in migration_cols.items():
                if col not in existing_cols:
                    cursor.execute(
                        f"ALTER TABLE content_versions ADD COLUMN {col} {col_type}"
                    )
            conn.commit()

    # ------------------------------------------------------------------
    # Write
    # ------------------------------------------------------------------

    def save_version(
        self,
        content_id: str,
        content: str,
        model_used: Optional[str] = None,
        tone: Optional[str] = None,
    ) -> int:
        """
        Persist a new version of the content.

        Args:
            content_id: Unique identifier (typically the topic string).
            content:    The full generated content.
            model_used: LLM model name used for generation.
            tone:       Tone/style label applied during generation.

        Returns:
            The new version number.
        """
        tags = json.dumps(self.auto_tag(content))
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT MAX(version) FROM content_versions WHERE content_id = ?",
                (content_id,),
            )
            result = cursor.fetchone()
            new_version = (result[0] or 0) + 1
            content_hash = hashlib.md5(content.encode()).hexdigest()
            cursor.execute(
                """
                INSERT INTO content_versions
                    (content_id, version, content, content_hash, word_count, tags, model_used, tone)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    content_id,
                    new_version,
                    content,
                    content_hash,
                    len(content.split()),
                    tags,
                    model_used or "unknown",
                    tone or "Professional",
                ),
            )
            conn.commit()
        return new_version

    # ------------------------------------------------------------------
    # Read
    # ------------------------------------------------------------------

    def get_history(self, content_id: str) -> List[Dict]:
        """Return version history (without full content body) for a topic."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT version, created_at, word_count, tags, model_used, tone
                FROM content_versions
                WHERE content_id = ?
                ORDER BY version DESC
                """,
                (content_id,),
            )
            rows = cursor.fetchall()
        return [
            {
                "version":    r[0],
                "date":       r[1],
                "words":      r[2],
                "tags":       json.loads(r[3]) if r[3] else [],
                "model":      r[4] or "—",
                "tone":       r[5] or "—",
            }
            for r in rows
        ]

    def get_version_content(self, content_id: str, version: int) -> Optional[str]:
        """Retrieve the full content text for a specific version."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content FROM content_versions WHERE content_id = ? AND version = ?",
                (content_id, version),
            )
            row = cursor.fetchone()
        return row[0] if row else None

    def get_all_topics(self) -> List[str]:
        """Return a list of all unique content_ids (topics) stored in the DB."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT DISTINCT content_id FROM content_versions ORDER BY content_id"
            )
            return [r[0] for r in cursor.fetchall()]

    # ------------------------------------------------------------------
    # Auto-tagging Helper (jackson-marcus)
    # ------------------------------------------------------------------

    @staticmethod
    def auto_tag(content: str, max_tags: int = 8) -> List[str]:
        """
        Extract lightweight topic tags from generated content by pulling
        the most frequent meaningful words from headings.

        Strategy:
            1. Extract all heading text (# … ### lines).
            2. Tokenise, lowercase, remove stop-words.
            3. Return the top `max_tags` words by frequency.

        Args:
            content:  The full content body.
            max_tags: Maximum number of tags to return.

        Returns:
            A list of tag strings.
        """
        STOP_WORDS = {
            "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
            "for", "of", "with", "by", "from", "is", "are", "was", "were",
            "it", "its", "this", "that", "these", "those", "be", "been",
            "has", "have", "had", "do", "does", "did", "will", "would",
            "can", "could", "should", "may", "might", "shall", "not",
            "as", "if", "so", "than", "then", "when", "how", "what",
            "which", "who", "all", "any", "their", "they", "we", "our",
            "your", "you", "he", "she", "his", "her", "us", "my", "i",
            "into", "about", "up", "out", "over", "more", "also", "just",
            "new", "key", "top", "best", "each", "per",
        }

        # Extract heading lines
        headings = re.findall(r"^#{1,3}\s+(.+)$", content, re.MULTILINE)
        heading_text = " ".join(headings)

        # Tokenise
        words = re.findall(r"[a-zA-Z]{3,}", heading_text.lower())

        # Frequency count, excluding stop-words
        freq: Dict[str, int] = {}
        for word in words:
            if word not in STOP_WORDS:
                freq[word] = freq.get(word, 0) + 1

        # Sort by frequency desc
        sorted_words = sorted(freq, key=lambda w: freq[w], reverse=True)
        return sorted_words[:max_tags]
