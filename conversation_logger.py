import os
import json
from datetime import datetime

class ConversationLogger:
    def __init__(self, profession: str):
        self.profession = profession
        self.conversation = []
        
    def extract_messages(self, content: str) -> list[dict]:
        """Extract individual messages from the conversation format."""
        name_mapping = {
            "AIExpert": "AI Expert"
        }
        messages = []
        
        if not content or '**' not in content:
            return messages
            
        parts = content.split('\n\n')
        for part in parts:
            if '**' in part:
                speaker = part[part.find('**')+2:part.find(':**')]
                message_content = part[part.find(':')+2:].strip()
                
                if message_content.startswith('* '):
                    message_content = message_content[2:]
                message_content = message_content.strip()
                
                speaker = name_mapping.get(speaker, speaker)
                
                if speaker and message_content:
                    messages.append({
                        "speaker": speaker,
                        "content": message_content
                    })
        
        return messages

    async def log_message(self, message):
        content = getattr(message, "content", "")
        
        if not content or "Have a casual chat about AI with" in content:
            return
            
        messages = self.extract_messages(content)
        for msg in messages:
            if msg["speaker"] and msg["content"]:
                self.conversation.append({
                    "speaker": msg["speaker"],
                    "content": msg["content"],
                    "timestamp": datetime.now().isoformat()
                })
    
    def save_to_file(self) -> str:
        os.makedirs("conversations", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"conversations/conversation_{self.profession}_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump({
                "profession": self.profession,
                "date": datetime.now().isoformat(),
                "messages": self.conversation
            }, f, indent=2, ensure_ascii=False)
        
        return filename