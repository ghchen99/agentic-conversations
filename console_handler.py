from conversation_logger import ConversationLogger

async def logging_console(stream, logger: ConversationLogger):
    """Print and log conversation messages."""
    async for message in stream:
        content = getattr(message, "content", "")
        
        if not content or "Have a casual chat about AI with" in content:
            continue
            
        extracted_messages = logger.extract_messages(content)
        
        for msg in extracted_messages:
            await logger.log_message(message)
            if msg["speaker"] and msg["content"]:
                print(f"{msg['speaker']}: {msg['content']}\n")