import os
import json
import asyncio
import logging
from pathlib import Path
import azure.cognitiveservices.speech as speechsdk
from typing import Dict, List

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tts_generation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class PodcastTTSGenerator:
    def __init__(self, speech_key: str, speech_region: str):
        """Initialize the TTS generator with Azure credentials"""
        self.speech_key = speech_key
        self.speech_region = speech_region
        
        # Define voice profiles for different roles
        self.voice_profiles = {
            "AI Expert": {
                "name": "en-US-DavisNeural",
                "style": "friendly"
            },
            "chef": {
                "name": "en-US-JasonNeural",
                "style": "casual"
            },
            "teacher": {
                "name": "en-US-JennyNeural",
                "style": "friendly"
            },
            "nurse": {
                "name": "en-US-AmberNeural",
                "style": "professional"
            }
        }
        
        # Create output directory
        self.output_dir = Path("podcast_audio")
        self.output_dir.mkdir(exist_ok=True)

    def _create_speech_config(self, voice_name: str) -> speechsdk.SpeechConfig:
        """Create speech configuration with specific voice settings"""
        speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        speech_config.speech_synthesis_voice_name = voice_name
        return speech_config

    async def synthesize_message(
        self,
        text: str,
        role: str,
        output_path: str
    ) -> None:
        """Synthesize a single message to audio file"""
        try:
            # Get voice profile based on role
            voice_profile = self.voice_profiles.get(
                role,
                self.voice_profiles["AI Expert"]  # default fallback
            )
            
            speech_config = self._create_speech_config(voice_profile["name"])
            
            # Configure audio output
            audio_config = speechsdk.AudioConfig(filename=output_path)
            
            # Create synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=audio_config
            )
            
            # Add SSML markup for style
            ssml_text = f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                   xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">
                <voice name="{voice_profile['name']}">
                    <mstts:express-as style="{voice_profile['style']}">
                        {text}
                    </mstts:express-as>
                </voice>
            </speak>
            """
            
            # Synthesize speech
            result = await asyncio.to_thread(
                synthesizer.speak_ssml_async,
                ssml_text
            )
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Speech synthesized for text [{text[:50]}...] and saved to [{output_path}]")
            else:
                logger.error(f"Speech synthesis failed: {result.reason}")
                
        except Exception as e:
            logger.error(f"Error synthesizing speech: {str(e)}")
            raise

    async def process_conversation(self, transcript_path: Path) -> None:
        """Process entire conversation transcript and generate audio files"""
        try:
            # Load conversation transcript
            with open(transcript_path, 'r', encoding='utf-8') as f:
                conversation_data = json.load(f)
            
            profession = conversation_data["profession"]
            timestamp = conversation_data["timestamp"]
            
            # Create output directory for this conversation
            conversation_dir = self.output_dir / f"{profession}_{timestamp}"
            conversation_dir.mkdir(exist_ok=True)
            
            # Process each message
            for idx, message in enumerate(conversation_data["messages"]):
                output_filename = f"{idx:03d}_{message['role'].lower()}.wav"
                output_path = str(conversation_dir / output_filename)
                
                await self.synthesize_message(
                    text=message["content"],
                    role=message["role"],
                    output_path=output_path
                )
                
                # Add small delay between requests
                await asyncio.sleep(0.5)
            
            logger.info(f"Completed processing conversation: {transcript_path}")
            
        except Exception as e:
            logger.error(f"Error processing conversation {transcript_path}: {str(e)}")
            raise

async def main():
    # Load Azure credentials from environment variables
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    
    if not speech_key or not speech_region:
        raise ValueError("Azure Speech credentials not found in environment variables")
    
    try:
        # Initialize TTS generator
        tts_generator = PodcastTTSGenerator(
            speech_key=speech_key,
            speech_region=speech_region
        )
        
        # Process all conversation transcripts in the conversations directory
        conversations_dir = Path("conversations")
        if not conversations_dir.exists():
            raise FileNotFoundError("Conversations directory not found")
        
        # Get all JSON files in conversations directory
        transcript_files = list(conversations_dir.glob("*.json"))
        
        if not transcript_files:
            logger.warning("No conversation transcripts found")
            return
        
        # Process each transcript
        for transcript_path in transcript_files:
            logger.info(f"Processing transcript: {transcript_path}")
            await tts_generator.process_conversation(transcript_path)
            
        logger.info("Completed processing all conversations")
        
    except Exception as e:
        logger.error(f"Error in main function: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    asyncio.run(main())