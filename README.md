# AI Podcast Generator

## Overview

This project automates the creation of 20-minute podcast episodes featuring dynamic conversations between an AI expert and various professionals (chefs, teachers, nurses) about AI's impact on their work. Using Azure OpenAI for dialogue generation and Azure Speech Services for voice synthesis, it produces natural-sounding podcast episodes complete with distinct voices for each speaker and professional audio quality. Each episode explores how AI is transforming specific industries through authentic discussions between the host and industry practitioners.

[Check out the `podcast_audio` folder for sample results 🔊](podcast_audio/podcast_nurse_20250210_145400.mp3)

## Features

* **Automated Conversation Generation**
  * Creates realistic multi-turn dialogues between an AI expert and professionals
  * Supports multiple professions (chef, teacher, nurse)
  * Ensures natural conversation flow with proper turn-taking

* **Audio Production**
  * Converts text conversations to audio using Azure Speech Services
  * Generates professional-quality podcast audio
  * Uses different voices for each speaker
  * Outputs high-quality MP3 files

* **Robust Infrastructure**
  * Comprehensive logging system
  * Error handling and recovery
  * Conversation storage in JSON format
  * Modular and extensible design

## Setup

### Prerequisites

* Python 3.7 or higher
* Azure OpenAI API access
* Azure Speech Services subscription

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Environment Configuration

Set the following environment variables:

```bash
# Azure OpenAI Configuration
AZURE_ENDPOINT="your_azure_openai_endpoint"
AZURE_API_KEY="your_azure_openai_api_key"
AZURE_API_VERSION="your_azure_openai_api_version"
AZURE_DEPLOYMENT="your_azure_openai_deployment"

# Azure Speech Services Configuration
AZURE_SPEECH_KEY="your_azure_speech_key"
AZURE_SPEECH_REGION="your_azure_speech_region"
```

## Project Structure

```
.
├── conversation_generator.py    # Main conversation generation script
├── audio_generator.py          # Text-to-speech conversion script
├── conversations/             # Stored conversation JSON files
├── podcast_audio/            # Generated MP3 files
├── conversation_logs.log     # System logs
└── requirements.txt          # Project dependencies
```

## Usage

### Generating Conversations

Run the conversation generator:

```bash
python conversation_generator.py
```

This creates JSON files in the `conversations` directory for each profession.

### Creating Podcast Audio

Generate audio from the conversations:

```bash
python audio_generator.py
```

This processes all JSON files in `conversations` and creates MP3 files in `podcast_audio`.

## Technical Details

### Conversation System

* **Structure**
  * AI Expert (George) leads discussions about workplace AI
  * Professional provides field-specific insights
  * 15 complete exchanges (30 messages total)
  * Context-aware responses maintain natural flow

* **Turn Management**
  * Strict alternating turns
  * Validation of speaker order
  * Conversation context tracking
  * Natural transition handling

### Audio Generation

* **Features**
  * Neural voice selection per speaker
  * Intelligent pause insertion
  * Chunk-based processing for large files
  * High-quality audio output (16kHz, 32kbps mono MP3)

* **Processing**
  * SSML generation with voice switching
  * Chunk size optimisation
  * Temporary file management
  * MP3 concatenation and cleanup

## Error Handling

The system includes comprehensive error management:

* Detailed logging of all operations
* Graceful API failure handling
* Automatic temporary file cleanup
* Conversation validation
* Environment variable verification

## Customisation

The project can be customised by:

* Adding new professions to `profession_examples`
* Adjusting conversation length via `num_chunks`
* Modifying voice selection in `get_voice_by_role`
* Configuring audio output settings
* Customizing conversation prompts and style

## License

This project is licensed under the terms of the license found in the LICENSE file in the root directory of this project.

## Contributing

I welcome contributions to improve the AI Podcast Generator! Here's how you can help:

### Reporting Issues
* Use the GitHub issue tracker to report bugs
* Include as much detail as possible: steps to reproduce, error messages, logs
* Describe what you expected to happen

### Pull Requests
1. Fork the repository
2. Create a new branch (`git checkout -b feature/your-feature`)
3. Make your changes
4. Run tests if available
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/your-feature`)

