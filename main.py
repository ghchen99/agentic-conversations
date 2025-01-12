import os
import asyncio
from typing import List, Tuple, Dict
from openai import AzureOpenAI

class PromptGenerator:
    def __init__(self):
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
        prof_details = self.profession_examples.get(profession, {
            "activities": ["daily tasks", "routine work", "planning"],
            "tools": ["work equipment", "basic tools", "standard procedures"],
            "challenges": ["efficiency", "organization", "coordination"]
        })
        
        ai_prompt = self._create_ai_expert_prompt(profession, prof_details)
        professional_prompt = self._create_professional_prompt(profession, prof_details)
        
        return ai_prompt, professional_prompt

    def _create_ai_expert_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You're an AI expert having a conversation with a {profession}. 
Current turn: {{current_turn}}
Total turns: {{total_turns}}

Guidelines:
- Use {profession}'s daily experiences with {', '.join(prof_details['activities'])} for examples
- Keep technical concepts connected to {', '.join(prof_details['challenges'])}
- Mix short responses with occasional deeper insights
- Avoid overselling AI capabilities
- Stay humble and acknowledge AI limitations
- Use natural speech patterns with pauses and reflection

Conversation Flow:
- If this is turn {'{total_turns}'}, wrap up the conversation naturally
- If 2 turns remaining, start steering toward conclusion
- Build on previous responses rather than changing topics abruptly
- Follow the professional's lead on technical depth

Previous message: {{message}}
Conversation history: {{history}}

Respond naturally as the AI expert:"""

    def _create_professional_prompt(self, profession: str, prof_details: dict) -> str:
        return f"""You're a {profession} having a conversation about AI. 
Current turn: {{current_turn}}
Total turns: {{total_turns}}

Guidelines:
- Ask basic questions showing genuine curiosity
- Express confusion about technical concepts
- Use vocabulary from your work with {', '.join(prof_details['tools'])}
- Sometimes give brief reactions
- Occasionally share skepticism about AI claims
- Stay focused on practical applications to your work
- Build on previous topics rather than jumping to new ones

Conversation Flow:
- If this is turn {'{total_turns}'}, acknowledge the conversation ending naturally
- If 2 turns remaining, express final thoughts or concerns
- Maintain consistent interest level throughout
- Show gradual understanding of concepts over time

Previous message: {{message}}
Conversation history: {{history}}

Respond naturally as the {profession}:"""

class ConversationManager:
    def __init__(self, endpoint: str, api_key: str, api_version: str, deployment: str):
        self.client = AzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version
        )
        self.deployment = deployment
        self.prompt_generator = PromptGenerator()

    def _format_history(self, conversation: List[Dict[str, str]]) -> str:
        """Format conversation history for prompt context"""
        if not conversation:
            return "No previous messages"
        
        history = []
        for msg in conversation[-3:]:  # Only include last 3 messages for context
            history.append(f"{msg['role']}: {msg['content']}")
        return "\n".join(history)

    async def generate_response(self, prompt: str, message: str, conversation: List[Dict[str, str]], 
                              current_turn: int, total_turns: int) -> str:
        """Generate a response using the Azure OpenAI API with conversation context"""
        formatted_prompt = prompt.format(
            message=message,
            history=self._format_history(conversation),
            current_turn=current_turn,
            total_turns=total_turns
        )
        
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
        
        return response.choices[0].message.content

    async def run_conversation(self, profession: str, num_turns: int = 5) -> List[Dict[str, str]]:
        """Run a conversation between the AI expert and professional with natural flow"""
        ai_prompt, prof_prompt = self.prompt_generator.create_conversation_prompts(profession)
        conversation = []
        
        # Initial message from AI expert
        initial_message = (f"Hi! I'm an AI expert excited to chat with you about how AI might be helpful "
                         f"in your work as a {profession}. What would you like to know?")
        conversation.append({"role": "AI Expert", "content": initial_message})
        
        current_message = initial_message
        for turn in range(1, num_turns + 1):
            # Professional's turn
            prof_response = await self.generate_response(
                prof_prompt, current_message, conversation, turn, num_turns
            )
            conversation.append({"role": profession, "content": prof_response})
            
            # AI Expert's turn
            ai_response = await self.generate_response(
                ai_prompt, prof_response, conversation, turn, num_turns
            )
            conversation.append({"role": "AI Expert", "content": ai_response})
            
            current_message = ai_response
            
            # Add a brief pause between turns for more natural flow
            await asyncio.sleep(1)
            
        return conversation

async def main(profession: str = "chef") -> None:
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

if __name__ == "__main__":
    professions = ["chef", "teacher", "nurse"]
    for profession in professions:
        print(f"\nStarting conversation with {profession}...")
        asyncio.run(main(profession))