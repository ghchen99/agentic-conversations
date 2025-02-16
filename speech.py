import os
import json
import wave
import azure.cognitiveservices.speech as speechsdk
from datetime import datetime

def setup_speech_config():
    """Initialize Azure Speech Service configuration"""
    speech_key = os.environ.get('AZURE_SPEECH_KEY')
    speech_region = os.environ.get('AZURE_SPEECH_REGION')
    
    if not speech_key or not speech_region:
        raise ValueError("Please set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION environment variables")
    
    return speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)

def get_voice_by_role(role):
    """Map conversation roles to specific voices"""
    voice_mapping = {
        "AI Expert": "en-US-GuyNeural",  
        "chef": "en-US-TonyNeural",         
        "nurse": "en-US-JennyNeural",       
        "teacher": "en-US-NancyNeural"      
    }
    return voice_mapping.get(role, "en-US-JennyNeural")  # Default voice

def create_output_directory():
    """Create output directory for audio files"""
    output_dir = "podcast_audio"
    os.makedirs(output_dir, exist_ok=True)
    return output_dir

def estimate_chunk_size(messages, target_chars=2000):
    """Estimate number of messages that fit within character limit"""
    total_chars = 0
    for idx, msg in enumerate(messages):
        total_chars += len(msg["content"])
        if total_chars >= target_chars:
            return max(1, idx)  # Ensure at least one message per chunk
    return len(messages)

def generate_ssml_with_pauses(messages):
    """Generate SSML with voice switching and pauses"""
    ssml = (
        '<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" '
        'xmlns:mstts="http://www.w3.org/2001/mstts" xml:lang="en-US">'
    )
    
    for index, message in enumerate(messages):
        voice_name = get_voice_by_role(message["role"])
        ssml += f'<voice name="{voice_name}">'
        ssml += f'{message["content"]}'
        if index < len(messages) - 1:
            ssml += '<break time="300ms"/>'
        ssml += '</voice>'
    
    ssml += '</speak>'
    return ssml

def combine_wav_files(wav_files, output_file):
    """Combine multiple WAV files into a single file"""
    if not wav_files:
        return False
        
    with wave.open(wav_files[0], 'rb') as first_wav:
        params = first_wav.getparams()
        
    with wave.open(output_file, 'wb') as output_wav:
        output_wav.setparams(params)
        
        for wav_file in wav_files:
            with wave.open(wav_file, 'rb') as wav:
                output_wav.writeframes(wav.readframes(wav.getnframes()))
    
    return True

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
        final_audio_filename = os.path.join(output_dir, f"podcast_{profession}_{timestamp}.wav")
        
        print(f"\nGenerating podcast audio: {final_audio_filename}")
        
        # Setup speech configuration
        speech_config = setup_speech_config()
        
        # Split messages into chunks based on content length
        messages = conversation_data["messages"]
        chunk_size = estimate_chunk_size(messages)
        message_chunks = [messages[i:i + chunk_size] for i in range(0, len(messages), chunk_size)]
        
        temp_wav_files = []
        successful_chunks = 0
        
        # Process each chunk
        for chunk_index, message_chunk in enumerate(message_chunks):
            temp_filename = os.path.join(output_dir, f"temp_chunk_{chunk_index}_{timestamp}.wav")
            temp_wav_files.append(temp_filename)
            
            # Configure audio output for this chunk
            audio_config = speechsdk.audio.AudioOutputConfig(filename=temp_filename)
            
            # Create synthesizer
            speech_synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config, 
                audio_config=audio_config
            )
            
            # Generate SSML for this chunk
            ssml = generate_ssml_with_pauses(message_chunk)
            
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
                temp_wav_files.remove(temp_filename)
        
        if successful_chunks > 0:
            # Combine all chunks into final audio file
            print("Combining audio chunks...")
            if combine_wav_files(temp_wav_files, final_audio_filename):
                print(f"✓ Successfully generated podcast audio: {final_audio_filename}")
            else:
                print("× Failed to combine audio chunks")
                return None
        else:
            print("× No chunks were successfully processed")
            return None
        
        # Clean up temporary files
        for temp_file in temp_wav_files:
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