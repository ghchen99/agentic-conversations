import os
import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict
from openai import AzureOpenAI

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('conversation_logs.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PromptGenerator:
    def __init__(self):
        logger.info("Initializing PromptGenerator")
        self.profession_examples = {
            "chef": {
                "activities": ["cooking meals", "managing kitchen inventory", "planning menus"],
                "tools": ["ovens", "ingredients", "recipes"],
                "challenges": ["timing dishes", "food waste", "kitchen efficiency"]
            },
            "teacher": {
                "activities": ["grading assignments", "lesson planning", "student assessment"],
                "tools": ["textbooks", "learning materials", "classroom tech"],
                "challenges": ["personalized learning", "student engagement", "time management"]
            },
            "nurse": {
                "activities": ["patient care", "medical records", "vital sign monitoring"],
                "tools": ["medical equipment", "patient charts", "medications"],
                "challenges": ["patient monitoring", "care coordination", "shift scheduling"]
            }
        }

    def create_conversation_prompt(self, profession: str, ai_name: str, prof_name: str) -> str:
        """Generate a combined prompt for multi-turn conversation with strict turn-taking"""
        logger.info(f"Creating multi-turn conversation prompt for profession: {profession}")
        prof_details = self.profession_examples.get(profession, {
            "activities": ["daily tasks", "routine work", "planning"],
            "tools": ["work equipment", "basic tools", "standard procedures"],
            "challenges": ["efficiency", "organization", "coordination"]
        })

        return f"""You are simulating a natural conversation between an AI Expert and a {profession}. Generate exactly 15 complete exchanges (30 messages total) with strict alternating turns. Each exchange should consist of one message from the AI Expert followed by one message from the {profession}. 

AI Expert ({ai_name}) style:
- Speak casually and naturally, like chatting with a colleague
- Be honest about AI's current limitations - no overselling
- Use concrete examples from their work: {', '.join(prof_details['activities'])}
- Address their actual pain points: {', '.join(prof_details['challenges'])}

{profession} ({prof_name}) style:
- Speak casually using work vocabulary: {', '.join(prof_details['tools'])}
- React naturally - show interest, confusion, or skepticism as appropriate
- Focus on practical concerns and real problems
- Be honest if something seems impractical

Rules for formatting:
1. Start each message with either "AI Expert:" or "{profession}:"
2. Each role speaks exactly once before the other responds
3. Maintain a clear back-and-forth pattern
4. Keep the conversation natural and flowing

Previous conversation context:
{{history}}

Continue the conversation naturally with exactly 15 complete exchanges, starting with the AI Expert's response to the last message"""

class ConversationManager:
    def __init__(self, endpoint: str, api_key: str, api_version: str, deployment: str):
        logger.info("Initializing ConversationManager")
        self.name_map = {
            "chef": "Brian",
            "teacher": "Sarah",
            "nurse": "Emma"
        }
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment = deployment
        self.prompt_generator = PromptGenerator()
        
        self.conversations_dir = Path("conversations")
        self.conversations_dir.mkdir(exist_ok=True)

    def _format_history(self, conversation: List[Dict[str, str]], chunk_num: int) -> str:
        """Format conversation history with awareness of chunk position and last speaker"""
        if not conversation:
            return "No previous messages"
        
        # For first chunk, include initial messages
        if chunk_num == 0:
            if len(conversation) >= 2:
                return f"{conversation[0]['role']}: {conversation[0]['content']}\n{conversation[1]['role']}: {conversation[1]['content']}"
            return f"{conversation[0]['role']}: {conversation[0]['content']}"
            
        # For subsequent chunks, include last 6 messages for better context
        last_messages = conversation[-6:] if len(conversation) >= 6 else conversation
        history = []
        for msg in last_messages:
            history.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(history)
    
    def _get_next_speaker(self, conversation: List[Dict[str, str]]) -> str:
        """Determine who should speak next based on conversation history"""
        if not conversation:
            return "AI Expert"
        last_speaker = conversation[-1]["role"]
        return self.current_profession if last_speaker == "AI Expert" else "AI Expert"


    def _format_history(self, conversation: List[Dict[str, str]], chunk_num: int) -> str:
        """Format conversation history with awareness of chunk position and last speaker"""
        if not conversation:
            return "No previous messages"
        
        # For first chunk, only include welcome message and add first question instruction
        if chunk_num == 0:
            history = f"{conversation[0]['role']}: {conversation[0]['content']}"
            history += "\n\nThe AI Expert should start with a first question to the professional."
            return history
            
        # For subsequent chunks, include last 6 messages for better context
        last_messages = conversation[-6:] if len(conversation) >= 6 else conversation
        history = []
        for msg in last_messages:
            history.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(history)

    def _get_next_speaker(self, conversation: List[Dict[str, str]]) -> str:
        """Determine who should speak next based on conversation history"""
        if not conversation:
            return "AI Expert"
        last_speaker = conversation[-1]["role"]
        return self.current_profession if last_speaker == "AI Expert" else "AI Expert"

    # TODO: CHeck this works properly
    async def generate_conversation_chunk(self, prompt: str, conversation: List[Dict[str, str]], chunk_num: int, ai_name: str, prof_name: str) -> List[Dict[str, str]]:
        """Generate conversation chunk with strict turn-taking enforcement"""
        next_speaker = self._get_next_speaker(conversation)
        formatted_prompt = prompt.format(
            history=self._format_history(conversation, chunk_num)
        )

        # Add clear instruction about who must speak next based on history
        if conversation:  # If there's a previous message
            formatted_prompt += f"\n\nCRITICAL: The last message was from {conversation[-1]['role']}. Therefore, the NEXT message MUST be from {next_speaker}. Generate a natural continuation of the conversation that STARTS with {next_speaker} and maintains strict alternating turns between AI Expert and {self.current_profession}."
        else:
            formatted_prompt += f"\n\nCRITICAL: This is the start of the conversation. The FIRST message MUST be from {next_speaker}, followed by strict alternating turns between AI Expert and {self.current_profession}."

        if chunk_num == 0:
            formatted_prompt += f"\nThis is the start of the conversation. {ai_name}'s welcome message and first question have already been given. The next message must be from {prof_name} responding to the question. Do not generate any AI Expert messages until after {prof_name} has responded. Maintain natural flow and end on an open question or point that leads into more discussion. Avoid any sense of wrapping up. "
        elif chunk_num == 4:  # Last chunk
            formatted_prompt += f"\nThis is the final part of the conversation. Work towards a natural conclusion in the last exchange between {ai_name} and {prof_name}."
        else:
            formatted_prompt += f"\nThis is a continuation of an ongoing conversation between {ai_name} and {prof_name}. Maintain natural flow and end on an open question or point that leads into more discussion. Avoid any sense of wrapping up. Always use their names when referring to them."
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.deployment,
                messages=[{"role": "system", "content": formatted_prompt}],
                temperature=0.7
            )
            
            new_messages = self._parse_conversation_chunk(response.choices[0].message.content)
            
            # Validate turn order but with simpler logic since we've given clearer instructions
            validated_messages = []
            expected_speaker = next_speaker
            
            for msg in new_messages:
                if msg["role"] != expected_speaker:
                    logger.warning(f"Message out of turn. Expected: {expected_speaker}, Got: {msg['role']}")
                    continue
                validated_messages.append(msg)
                expected_speaker = "AI Expert" if expected_speaker == self.current_profession else self.current_profession
            
            return validated_messages
            
        except Exception as e:
            logger.error(f"Error generating chunk: {str(e)}")
            raise
        
    def _parse_conversation_chunk(self, text: str) -> List[Dict[str, str]]:
        """Parse multi-turn conversation text into structured format, handling mixed dialogue"""
        messages = []
        
        # Split into lines and clean up
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        current_role = None
        current_content = []
        
        for line in lines:
            # Look for role markers at start of line
            if "AI Expert:" in line or f"{self.current_profession}:" in line:
                # If we have a previous message, save it
                if current_role and current_content:
                    messages.append({
                        "role": current_role,
                        "content": " ".join(current_content).strip()
                    })
                    current_content = []
                
                # Start new message
                if line.startswith("AI Expert:"):
                    current_role = "AI Expert"
                    content = line.replace("AI Expert:", "", 1)
                else:
                    current_role = self.current_profession
                    content = line.replace(f"{self.current_profession}:", "", 1)
                current_content = [content.strip()]
            
            # Handle mid-message role changes
            elif ": " in line:
                role_split = line.split(": ", 1)
                if role_split[0] in ["AI Expert", self.current_profession]:
                    # Save previous message if exists
                    if current_role and current_content:
                        messages.append({
                            "role": current_role,
                            "content": " ".join(current_content).strip()
                        })
                        current_content = []
                    
                    # Start new message
                    current_role = role_split[0]
                    current_content = [role_split[1]]
                else:
                    # If not a role marker, treat as continuation
                    if current_role:
                        current_content.append(line)
            else:
                # Continue current message
                if current_role:
                    current_content.append(line)
        
        # Add final message if exists
        if current_role and current_content:
            messages.append({
                "role": current_role,
                "content": " ".join(current_content).strip()
            })
        
        return messages

    def _save_conversation(self, profession: str, conversation: List[Dict[str, str]]) -> None:
        """Save conversation transcript to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.conversations_dir / f"conversation_{profession}_{timestamp}.json"
        
        conversation_data = {
            "profession": profession,
            "timestamp": timestamp,
            "messages": conversation
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(conversation_data, f, indent=2, ensure_ascii=False)
        logger.info(f"Conversation saved to: {filename}")

    async def run_conversation(self, profession: str, num_chunks: int = 5) -> List[Dict[str, str]]:
        """Run a multi-turn conversation with strict turn-taking"""
        logger.info(f"Starting chunked conversation with {profession}")
        self.current_profession = profession
        
        ai_name = "George"
        prof_name = self.name_map.get(profession, profession.title())
        self.ai_name = ai_name
        self.prof_name = prof_name
        
        conversation = []
        prompt = self.prompt_generator.create_conversation_prompt(
            profession=profession,
            ai_name=ai_name,
            prof_name=prof_name)
        
        # Initialize with welcome message and first question
        conversation.extend([
            {
                "role": "AI Expert",
                "content": f"Hey everyone, welcome to our podcast series about AI in the workplace! I'm George, and today we're joined by {prof_name} who's going to share their experiences as a {profession}. Great to have you with us!"
            },
            {
                "role": "AI Expert",
                "content": f"Hey {prof_name}, thanks for joining us! So, as a {profession}, have you had any experience with AI tools in your work yet?"
            }
        ])
        
        for chunk in range(num_chunks):
            logger.info(f"Generating conversation chunk {chunk + 1}/{num_chunks}")
            
            new_messages = await self.generate_conversation_chunk(
                prompt=prompt,
                conversation=conversation,
                chunk_num=chunk,
                ai_name=self.ai_name,
                prof_name=self.prof_name)
            
            # Only take messages that maintain proper turn order
            for msg in new_messages:
                if not conversation or msg["role"] != conversation[-1]["role"]:
                    conversation.append(msg)
            
            await asyncio.sleep(1)
        
        self._save_conversation(profession, conversation)
        return conversation

async def main(profession: str = "chef") -> None:
    logger.info(f"Starting main function for profession: {profession}")
    
    try:
        conversation_manager = ConversationManager(
            endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            deployment=os.getenv("AZURE_DEPLOYMENT")
        )
        
        conversation = await conversation_manager.run_conversation(profession)
        
        print(f"\nConversation with {profession}:")
        for message in conversation:
            print(f"\n{message['role']}: {message['content']}\n")
            print("-" * 80)
            
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    logger.info("Starting conversation script")
    professions = ["chef", "teacher", "nurse"]
    
    for profession in professions:
        try:
            logger.info(f"\nStarting conversation with {profession}...")
            asyncio.run(main(profession))
        except Exception as e:
            logger.error(f"Error in conversation with {profession}: {str(e)}", exc_info=True)
            continue
            
    logger.info("Completed all conversations")