from prompt_generator import PromptGenerator
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient

class ConversationManager:
    def __init__(self, model_client: AzureOpenAIChatCompletionClient, profession: str):
        self.model_client = model_client
        self.profession = profession
        self.prompt_generator = PromptGenerator()

    def create_agents(self) -> RoundRobinGroupChat:
        ai_prompt, professional_prompt = self.prompt_generator.create_profession_prompts(self.profession)
        
        ai_agent = self._create_ai_agent(ai_prompt)
        professional_agent = self._create_professional_agent(professional_prompt)
        
        return RoundRobinGroupChat([ai_agent, professional_agent], max_turns=15)

    def _create_ai_agent(self, ai_prompt: str) -> AssistantAgent:
        return AssistantAgent(
            name="AIExpert",
            model_client=self.model_client,
            tools=[],
            description=ai_prompt,
            system_message="Focus on realistic, practical applications. Avoid overhyping AI capabilities.",
        )

    def _create_professional_agent(self, professional_prompt: str) -> AssistantAgent:
        return AssistantAgent(
            name=self.profession.capitalize(),
            model_client=self.model_client,
            tools=[],
            description=professional_prompt,
            system_message="Keep responses natural and varied in length. Express genuine curiosity and occasional confusion.",
        )

    def get_initial_task(self) -> str:
        return f"""As an AI Expert, have a casual chat about AI with a {self.profession}, focusing on:
- Keep the tone natural and grounded
- Allow for confusion and clarification
- Vary response lengths naturally
- Discuss realistic AI applications
- Connect examples to {self.profession}'s work
- Avoid overhyping AI capabilities"""