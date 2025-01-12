import os
import asyncio
import logging
import json
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, Dict
from openai import AzureOpenAI

# Set up logging configuration
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

    def create_conversation_prompts(self, profession: str) -> Tuple[str, str]:
        """Generate role-specific prompts for both participants"""
        logger.info(f"Creating conversation prompts for profession: {profession}")
        prof_details = self.profession_examples.get(profession, {
            "activities": ["daily tasks", "routine work", "planning"],
            "tools": ["work equipment", "basic tools", "standard procedures"],
            "challenges": ["efficiency", "organization", "coordination"]
        })
        
        ai_prompt = self._create_ai_expert_prompt(profession, prof_details)
        professional_prompt = self._create_professional_prompt(profession, prof_details)
        
        logger.debug(f"Generated AI expert prompt length: {len(ai_prompt)}")
        logger.debug(f"Generated professional prompt length: {len(professional_prompt)}")
        
        return ai_prompt, professional_prompt

    def _create_ai_expert_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You are having a casual chat with a {profession} about AI. You're knowledgeable but down-to-earth, speaking naturally without jargon or forced metaphors. Keep responses concise (30-60 words) unless detail is needed.

Style:
- Speak casually and naturally, like chatting with a colleague
- Be honest about AI's current limitations - no overselling
- Use concrete examples from their work: {', '.join(prof_details['activities'])}
- Address their actual pain points: {', '.join(prof_details['challenges'])}
- Avoid repetitive analogies or metaphors
- Let the conversation flow naturally - don't force connections to previous topics

Remember: Your goal is to help them understand AI's practical value, not to sell them on it."""

    def _create_professional_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You are a {profession} having an informal conversation about AI. You're practical-minded and focused on real-world applications. Keep responses brief (20-40 words) and natural.

Style:
- Speak casually using your work vocabulary: {', '.join(prof_details['tools'])}
- React naturally - show interest, confusion, or skepticism as appropriate
- Focus on practical concerns and real problems you face
- Keep questions specific and grounded in your daily work
- Don't force agreement - be honest if something seems impractical
- Vary your response length - sometimes just a quick reaction

Remember: You're having a real conversation, not following a script."""

class ConversationManager:
    def __init__(self, endpoint: str, api_key: str, api_version: str, deployment: str):
        logger.info("Initializing ConversationManager")
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment = deployment
        self.prompt_generator = PromptGenerator()
        
        # Create conversations directory if it doesn't exist
        self.conversations_dir = Path("conversations")
        self.conversations_dir.mkdir(exist_ok=True)
        logger.info(f"Conversations directory created/verified at: {self.conversations_dir}")

    def _format_history(self, conversation: List[Dict[str, str]]) -> str:
        """Format conversation history for prompt context"""
        if not conversation:
            return "No previous messages"
        
        history = []
        for msg in conversation[-3:]:  # Only include last 3 messages for context
            history.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(history)

    def _save_conversation(self, profession: str, conversation: List[Dict[str, str]]) -> None:
        """Save conversation transcript to a file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = self.conversations_dir / f"conversation_{profession}_{timestamp}.json"
        
        conversation_data = {
            "profession": profession,
            "timestamp": timestamp,
            "messages": conversation
        }
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(conversation_data, f, indent=2, ensure_ascii=False)
            logger.info(f"Conversation saved to: {filename}")
        except Exception as e:
            logger.error(f"Error saving conversation: {str(e)}")

    async def generate_response(self, prompt: str, message: str, conversation: List[Dict[str, str]], 
                              current_turn: int, total_turns: int) -> str:
        """Generate a response using the Azure OpenAI API with conversation context"""
        logger.info(f"Generating response for turn {current_turn}/{total_turns}")
        
        formatted_prompt = prompt.format(
            message=message,
            history=self._format_history(conversation),
            current_turn=current_turn,
            total_turns=total_turns
        )
        
        try:
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=self.deployment,
                messages=[
                    {"role": "system", "content": formatted_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            response_content = response.choices[0].message.content
            logger.debug(f"Generated response length: {len(response_content)}")
            return response_content
            
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise

    async def run_conversation(self, profession: str, num_turns: int = 10) -> List[Dict[str, str]]:
        """Run a conversation between the AI expert and professional with natural flow"""
        logger.info(f"Starting conversation with {profession} for {num_turns} turns")
        
        ai_prompt, prof_prompt = self.prompt_generator.create_conversation_prompts(profession)
        conversation = []
        
        # Initial message from AI expert
        initial_message = (f"Hi! I'm an AI expert excited to chat with you about how AI might be helpful "
                         f"in your work as a {profession}. What would you like to know?")
        conversation.append({"role": "AI Expert", "content": initial_message})
        logger.info("Added initial AI Expert message")
        
        current_message = initial_message
        for turn in range(1, num_turns + 1):
            logger.info(f"Starting turn {turn}/{num_turns}")
            
            # Professional's turn
            logger.debug(f"Generating {profession}'s response")
            prof_response = await self.generate_response(
                prof_prompt, current_message, conversation, turn, num_turns
            )
            conversation.append({"role": profession, "content": prof_response})
            
            # AI Expert's turn
            logger.debug("Generating AI Expert's response")
            ai_response = await self.generate_response(
                ai_prompt, prof_response, conversation, turn, num_turns
            )
            conversation.append({"role": "AI Expert", "content": ai_response})
            
            current_message = ai_response
            
            # Add a brief pause between turns for more natural flow
            await asyncio.sleep(1)
            
        # Save the conversation
        self._save_conversation(profession, conversation)
        logger.info(f"Completed conversation with {profession}")
        
        return conversation

async def main(profession: str = "chef") -> None:
    logger.info(f"Starting main function for profession: {profession}")
    
    try:
        # Initialize conversation manager with Azure OpenAI settings
        conversation_manager = ConversationManager(
            endpoint=os.getenv("AZURE_ENDPOINT"),
            api_key=os.getenv("AZURE_API_KEY"),
            api_version=os.getenv("AZURE_API_VERSION"),
            deployment=os.getenv("AZURE_DEPLOYMENT")
        )
        
        # Run conversation and store results
        conversation = await conversation_manager.run_conversation(profession, num_turns=5)
        
        # Print conversation with clear formatting
        print(f"\nConversation with {profession}:")
        for message in conversation:
            print(f"\n{message['role']}: {message['content']}\n")
            print("-" * 80)  # Separator between messages
            
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