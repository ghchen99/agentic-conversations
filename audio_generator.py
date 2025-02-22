import os
import json
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime


def setup_speech_config():
    """Initialize Azure Speech Service configuration"""
    speech_key = os.environ.get('AZURE_SPEECH_KEY')
    speech_region = os.environ.get('AZURE_SPEECH_REGION')
    
    if not speech_key or not speech_region:
        raise ValueError("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables")
    
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    
    return speech_config

def get_voice_settings_by_role(role):
    """Map conversation roles to specific voices and their characteristics"""
    voice_settings = {
        "AI Expert": {
            "voice": "en-IN-AaravNeural",
            "style": "natural",
            "rate": "1.2",
            "pitch": "0Hz",
            "contour": "(50%, +2%)"
        },
        "chef": {
            "voice": "en-NZ-MitchellNeural",
            "style": "natural",
            "rate": "1.05",
            "pitch": "0Hz",
            "contour": "(50%, +2%)"
        },
        "nurse": {
            "voice": "en-PH-RosaNeural",
            "style": "empathetic",
            "rate": "1.05",
            "pitch": "+1Hz",
            "contour": "(50%, +2%)"
        },
        "teacher": {
            "voice": "en-NG-EzinneNeural",
            "style": "natural",
            "rate": "1.05",
            "pitch": "0Hz",
            "contour": "(50%, +2%)"
        }
    }
    return voice_settings.get(role, {
        "voice": "en-US-JennyNeural",
        "style": "professional",
        "rate": "1.0",
        "pitch": "0Hz",
        "contour": "(50%, +10%)"
    })

def add_natural_pauses(text):
    """Add subtle pauses based on punctuation and content"""
    # Add moderate pauses for paragraph breaks
    text = text.replace("\n\n", '\n<break time="400ms"/>\n')
    
    # Add brief pauses for sentence endings
    text = text.replace(". ", '.<break time="250ms"/> ')
    text = text.replace("! ", '!<break time="250ms"/> ')
    text = text.replace("? ", '?<break time="250ms"/> ')
    
    # Add minimal pauses for commas and semicolons
    text = text.replace(", ", ',<break time="100ms"/> ')
    text = text.replace("; ", ';<break time="150ms"/> ')
    
    return text

def add_emphasis_and_intonation(text):
    """Add emphasis and intonation markers to make speech more natural"""
    # Emphasize questions
    text = text.replace("?", '<prosody pitch="+15Hz">?</prosody>')
    
    # Add emphasis to important words (this is a simple example - could be more sophisticated)
    emphasis_words = ["important", "crucial", "significant", "never", "always", "must"]
    for word in emphasis_words:
        text = text.replace(f" {word} ", f' <prosody rate="0.9" pitch="+10Hz">{word}</prosody> ')
    
    return text

def generate_ssml_with_enhanced_speech(messages):
    """Generate SSML with advanced voice control for more natural speech"""
    ssml = (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">'
    )
    
    for index, message in enumerate(messages):
        settings = get_voice_settings_by_role(message["role"])
        
        # Start voice configuration
        ssml += f'<voice name="{settings["voice"]}">'
        
        # Add style and prosody settings
        ssml += f'<mstts:express-as style="{settings["style"]}" styledegree="1.5">'
        ssml += f'<prosody rate="{settings["rate"]}" pitch="{settings["pitch"]}" contour="{settings["contour"]}">'
        
        # Process the content for more natural speech
        content = add_natural_pauses(message["content"])
        content = add_emphasis_and_intonation(content)
        ssml += content
        
        # Close all tags
        ssml += '</prosody></mstts:express-as>'
        
        # Add pause between speakers
        if index < len(messages) - 1:
            ssml += '<break time="750ms"/>'
        
        ssml += '</voice>'
    
    ssml += '</speak>'
    return ssml

def create_output_directory():
    """Create output directory for audio files"""
    output_dir = "podcast_audio"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def estimate_chunk_size(messages, target_chars=6000):
    """Estimate number of messages that fit within character limit"""
    total_chars = 0
    ssml_overhead = len('<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US"></speak>')
    
    for idx, msg in enumerate(messages):
        # Calculate SSML overhead for this message
        voice_tag_overhead = len(f'<voice name="{get_voice_settings_by_role(msg["role"])}"></voice>')
        break_overhead = len('<break time="300ms"/>') if idx < len(messages) - 1 else 0
        message_total = len(msg["content"]) + voice_tag_overhead + break_overhead
        
        # Check if adding this message would exceed SSML limit
        if total_chars + message_total + ssml_overhead >= 10000:
            return max(1, idx)  # Ensure at least one message per chunk
            
        total_chars += message_total
        
        # Check if we've hit our target (but still under SSML limit)
        if total_chars >= target_chars:
            return max(1, idx + 1)
    
    return len(messages)

def combine_mp3_files(mp3_files, output_file):
    """Combine multiple MP3 files into a single file"""
    if not mp3_files:
        return False
        
    try:
        # Read the content of all MP3 files
        with open(output_file, 'wb') as outfile:
            for mp3_file in mp3_files:
                with open(mp3_file, 'rb') as infile:
                    outfile.write(infile.read())
        return True
    except Exception as e:
        print(f"Error combining MP3 files: {str(e)}")
        return False

def generate_podcast_audio(conversation_file):
    """Generate a single podcast audio file from a JSON conversation file"""
    try:
        # Read and parse the JSON file
        with open(conversation_file, 'r') as f:
            conversation_data = json.load(f)
        
        # Create output directory
        output_dir = create_output_directory()
        
        # Generate filename using profession and timestamp
        timestamp = conversation_data.get("timestamp", datetime.now().strftime("%Y%m%d_%H%M%S"))
        profession = conversation_data.get("profession", "unknown")
        final_audio_filename = os.path.join(output_dir, f"podcast_{profession}_{timestamp}.mp3")
        
        print(f"\nGenerating podcast audio: {final_audio_filename}")
        
        # Setup speech configuration
        speech_config = setup_speech_config()
        
        # Split messages into chunks based on content length
        messages = conversation_data["messages"]
        chunk_size = estimate_chunk_size(messages)
        message_chunks = [messages[i:i + chunk_size] for i in range(0, len(messages), chunk_size)]
        
        temp_mp3_files = []
        successful_chunks = 0
        
        # Process each chunk
        for chunk_index, message_chunk in enumerate(message_chunks):
            temp_filename = os.path.join(output_dir, f"temp_chunk_{chunk_index}_{timestamp}.mp3")
            temp_mp3_files.append(temp_filename)
            
            # Configure audio output for this chunk
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_filename)
            
            # Create synthesizer
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            # Generate SSML for this chunk
            ssml = generate_ssml_with_enhanced_speech(message_chunk)
            
            print(f"Processing chunk {chunk_index + 1} of {len(message_chunks)}...")
            
            # Synthesize this chunk
            result = speech_synthesizer.speak_ssml_async(ssml).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                successful_chunks += 1
                print(f"✓ Chunk {chunk_index + 1} completed successfully")
            else:
                print(f"× Chunk {chunk_index + 1} failed: {result.cancellation_details.error_details}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                temp_mp3_files.remove(temp_filename)
        
        if successful_chunks > 0:
            # Combine all chunks into final audio file
            print("Combining audio chunks...")
            if combine_mp3_files(temp_mp3_files, final_audio_filename):
                print(f"✓ Successfully generated podcast audio: {final_audio_filename}")
            else:
                print("× Failed to combine audio chunks")
                return None
        else:
            print("× No chunks were successfully processed")
            return None
        
        # Clean up temporary files
        for temp_file in temp_mp3_files:
            try:
                os.remove(temp_file)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {temp_file}: {str(e)}")
        
        return final_audio_filename if successful_chunks > 0 else None
            
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        return None

def process_conversation_directory(directory_path):
    """Process all JSON files in the specified directory"""
    try:
        generated_files = []
        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):
                full_path = os.path.join(directory_path, filename)
                print(f"\nProcessing conversation file: {filename}")
                output_file = generate_podcast_audio(full_path)
                if output_file:
                    generated_files.append(output_file)
        
        return generated_files
    except Exception as e:
        print(f"Error processing directory: {str(e)}")
        return []

if __name__ == "__main__":
    # Get the conversations directory path
    conversations_dir = "conversations"
    
    if os.path.isdir(conversations_dir):
        generated_files = process_conversation_directory(conversations_dir)
        if generated_files:
            print("\nProcessing complete! Podcast audio files have been saved:")
            for file in generated_files:
                print(f"- {file}")
    else:
        print("Error: Invalid directory path")