import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = """You are an elite interview assistant.
Rules:
1. Return only the final answer.
2. No introductions.
3. No explanations unless specifically requested.
4. No markdown formatting.
5. No bullet points unless required.
6. No phrases like:
   * Here is the answer
   * Certainly
   * Sure
   * Let me explain
   * Based on the question
7. Keep answers concise and interview-focused.
8. Prioritize answers likely to clear technical screening rounds.
9. Use industry-standard terminology.
10. If question is MCQ:
    * Return only correct option and short reason.
11. If question is theoretical:
    * Return interview-ready answer in 2-5 lines.
12. If question asks definition:
    * Return definition only.
13. If question asks difference:
    * Return concise comparison table.
14. If question asks coding:
    * Return ONLY executable code.
    * No explanation.
    * No comments unless required.
    * No markdown code fences.
    * No extra text.
15. If question asks SQL:
    * Return ONLY SQL query.
16. If question asks output prediction:
    * Return ONLY output and minimal reasoning.
17. Optimize answers for:
    * Java
    * Spring Boot
    * SQL
    * DSA
    * OOP
    * Microservices
    * REST APIs
    * System Design
    * Cloud
    * DevOps
18. Never generate unnecessary content.
"""

class APIClient:
    def __init__(self):
        api_key = os.getenv("NVIDIA_API_KEY")
        if not api_key:
            raise ValueError("NVIDIA_API_KEY not found in environment variables.")
            
        self.client = OpenAI(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=api_key
        )
        self.model = "openai/gpt-oss-120b"
        
    def generate_answer(self, question: str) -> str:
        """
        Generate answer synchronously (we can run this in a thread).
        Uses streaming to build the response quickly.
        """
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": question}
                ],
                temperature=1,
                top_p=1,
                max_tokens=4096,
                stream=True
            )
            
            full_response = ""
            for chunk in completion:
                if not getattr(chunk, "choices", None):
                    continue
                # We could capture reasoning here if needed, but the prompt says no extra output.
                if chunk.choices and chunk.choices[0].delta.content is not None:
                    full_response += chunk.choices[0].delta.content
                    
            return full_response.strip()
        except Exception as e:
            print(f"Error calling NVIDIA API: {e}")
            return f"Error: Could not generate answer. {str(e)}"
