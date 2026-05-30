import sqlite3
import hashlib
import os

class CacheManager:
    def __init__(self):
        app_data = os.getenv('LOCALAPPDATA', os.path.expanduser('~'))
        crackit_dir = os.path.join(app_data, 'CrackIt')
        if not os.path.exists(crackit_dir):
            os.makedirs(crackit_dir)
        self.db_path = os.path.join(crackit_dir, "questions.db")
        self._init_db()

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS answers_cache (
                question_hash TEXT PRIMARY KEY,
                answer TEXT
            )
        ''')
        conn.commit()
        conn.close()

    def _hash_question(self, question: str) -> str:
        # Normalize slightly by stripping whitespace
        normalized = question.strip()
        return hashlib.sha256(normalized.encode('utf-8')).hexdigest()

    def get_answer(self, question: str) -> str:
        q_hash = self._hash_question(question)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM answers_cache WHERE question_hash = ?", (q_hash,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return row[0]
        return None

    def save_answer(self, question: str, answer: str):
        q_hash = self._hash_question(question)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO answers_cache (question_hash, answer) VALUES (?, ?)",
            (q_hash, answer)
        )
        conn.commit()
        conn.close()
