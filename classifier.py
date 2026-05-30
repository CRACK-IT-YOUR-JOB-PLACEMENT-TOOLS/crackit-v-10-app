import re

class Classifier:
    @staticmethod
    def should_process(text: str) -> bool:
        if not text:
            return False
            
        text = text.strip()
        
        # Rule 1: Ignore content under 5 characters
        if len(text) < 5:
            return False
            
        # Rule 2: Ignore single words
        if " " not in text and "\n" not in text:
            return False
            
        # Rule 3: Ignore URLs
        url_pattern = re.compile(
            r'^(?:http|ftp)s?://' # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
            r'localhost|' #localhost...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
            r'(?::\d+)?' # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
            
        if url_pattern.match(text):
            return False
            
        # Rule 4: Ignore generated answers (covered by marker check, but we can do a simple check here too)
        # Actually, the marker check will happen in the main loop before calling this, but we can double check.
        if "[AI_RESPONSE_IGNORE_7XK29]" in text:
            return False

        # Additional basic heuristic to avoid random text:
        # We can assume if it's multiple words and > 5 chars, it might be an interview question.
        # It's better to send it and let the model handle it than block valid questions.
        
        return True
