import os
import asyncio
from autogen_ext.models.openai import AzureOpenAIChatCompletionClient
from conversation_manager import ConversationManager
from conversation_logger import ConversationLogger
from console_handler import logging_console

async def main(profession: str = "chef") -> None:
    # Initialize Azure OpenAI client
    az_model_client = AzureOpenAIChatCompletionClient(
        azure_deployment=os.getenv("AZURE_DEPLOYMENT"),
        model=os.getenv("AZURE_MODEL_NAME"),
        api_version=os.getenv("AZURE_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_ENDPOINT"),
        api_key=os.getenv("AZURE_API_KEY")
    )
    
    # Initialize conversation components
    conversation_manager = ConversationManager(az_model_client, profession)
    logger = ConversationLogger(profession)
    
    # Create and run conversation
    team = conversation_manager.create_agents()
    stream = team.run_stream(task=conversation_manager.get_initial_task())
    
    # Handle console output and logging
    await logging_console(stream, logger)
    
    # Save conversation
    filename = logger.save_to_file()
    print(f"\nConversation saved to: {filename}")

if __name__ == "__main__":
    professions = ["chef", "teacher", "nurse"]
    for profession in professions:
        print(f"\nStarting conversation with {profession}...")
        asyncio.run(main(profession))