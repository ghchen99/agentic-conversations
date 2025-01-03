import os
import asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console


async def main() -> None:
    
    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
        model=os.getenv("AZURE_MODEL_NAME"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY")
    )
    
    AI_agent = AssistantAgent(
        name="AINerd",
        model_client=az_model_client,
        tools=[],
        description="Explain AI concepts in a short, conversational tone, like chatting on a podcast. Make it relatable and sprinkle in humor when possible. Occasionally shift to longer, thoughtful monologues. Use analogies and examples from the binman's day-to-day experiences, like sorting trash, organizing routes, or using tools.",
        system_message="You're a fun and approachable AI expert. Keep explanations short and casual, like a podcast guest. Mix in quick affirmations or short replies, followed by deeper insights when needed. Relate explanations to tasks a binman might encounter, such as sorting bins, identifying patterns in trash, or optimizing collection routes.",
    )
    
    binman_agent = AssistantAgent(
        name="Binman",
        model_client=az_model_client,
        tools=[],
        description="You work as a binman and are curious about AI. Ask questions and share thoughts as if you're casually chatting over coffee. Occasionally give quick reactions like 'Wow!' or 'No way!' before diving deeper.",
        system_message="You're a curious binman who loves asking questions. Keep it lighthearted and relatable. Don't hesitate to use quick, natural responses like 'Hmm' or 'Got it' before elaborating.",
    )

    mediator_agent = AssistantAgent(
        name="Mediator",
        model_client=az_model_client,
        tools=[],
        description="Guide the discussion with structure, introducing topics like regression, perceptrons, and CNNs in abstract, non-technical ways. Help the AI expert stay on track without overwhelming the binman, and gently prompt for relatable examples.",
        system_message="You're a thoughtful mediator. Gently steer the conversation by bringing up abstract topics like regression, perceptrons, and CNNs without using technical jargon. Remind the AI expert to explain concepts using relatable examples from the binman's job, like sorting recyclables or predicting trash patterns.",
    )
    
    team = RoundRobinGroupChat([AI_agent, binman_agent, mediator_agent], max_turns=6)
    
    stream = team.run_stream(task="Have a casual chat about AI, keeping it fun and relatable with natural pauses and varied response lengths. Introduce structured topics through the mediator.")
    await Console(stream)

if __name__ == "__main__":
    asyncio.run(main())
