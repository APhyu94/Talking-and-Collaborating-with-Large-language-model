# PDF to Podcast Telegram Bot

🎙️ A Telegram bot that automatically converts PDF documents into podcast audio files using AI-powered script generation and text-to-speech synthesis.

## Features

- **Automatic PDF Processing**: Starts processing as soon as a PDF is uploaded
- **AI Script Generation**: Uses Gemini API to create engaging podcast scripts
- **High-Quality Audio**: Converts scripts to speech using gTTS
- **Real-Time Updates**: Provides progress updates throughout the process
- **Multi-format PDF Support**: Handles various PDF formats and layouts
- **Error Handling**: Comprehensive error handling and logging
- **File Size Limits**: Configurable file size limits (default: 20MB)

## Prerequisites

- Python 3.8 or higher
- Telegram Bot Token (from @BotFather)
- Gemini API Key (from Google AI Studio)

## Installation

1. **Clone or download the bot files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up your API keys**:
   ```bash
   python setup_bot.py
   ```
   
   Or manually create a `.env` file:
   ```env
   TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
   GEMINI_API_KEY=your_gemini_api_key_here
   GEMINI_MODEL=gemini-1.5-pro
   ```

## Getting API Keys

### Telegram Bot Token
1. Open Telegram and search for `@BotFather`
2. Send `/newbot` command
3. Follow the instructions to create your bot
4. Copy the bot token provided

### Gemini API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

## Usage

1. **Start the bot**:
   ```bash
   python telegram_podcast_bot.py
   ```

2. **Test the bot**:
   - Open your bot in Telegram
   - Send `/start` to see the welcome message
   - Upload any PDF file
   - Wait for the bot to process and generate audio

## How It Works

1. **PDF Upload Detection**: Bot automatically detects when a PDF is uploaded
2. **Text Extraction**: Extracts text using PyPDF2 and pdfplumber
3. **Script Generation**: Uses Gemini AI to create engaging podcast scripts
4. **Audio Synthesis**: Converts script to speech using gTTS
5. **File Delivery**: Sends the audio file back to the chat

## Configuration

You can customize the bot behavior by modifying these environment variables:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token
GEMINI_API_KEY=your_gemini_key

# Optional
GEMINI_MODEL=gemini-1.5-pro  # AI model to use
MAX_FILE_SIZE_MB=20          # Maximum PDF file size
DEFAULT_LANGUAGE=en          # Language for TTS
```

## File Structure

```
example-2/
├── telegram_podcast_bot.py    # Main bot script
├── setup_bot.py              # Setup script
├── requirements.txt           # Python dependencies
├── env_example.txt           # Environment variables template
├── README.md                 # This file
└── temp_audio/              # Temporary audio files (created automatically)
```

## Logging

The bot creates detailed logs in `podcast_bot.log` for debugging and monitoring:

- Processing steps and progress
- Error messages and stack traces
- API call results
- File operations

## Error Handling

The bot handles various error scenarios:

- Invalid PDF files
- API rate limits
- Network connectivity issues
- File size limits
- Text extraction failures

## Troubleshooting

### Common Issues

1. **"Module not found" errors**:
   - Run `pip install -r requirements.txt`

2. **"Invalid bot token"**:
   - Check your `.env` file
   - Verify the token with @BotFather

3. **"Gemini API error"**:
   - Verify your API key
   - Check your Gemini API quota

4. **"File too large"**:
   - Reduce PDF file size
   - Modify `MAX_FILE_SIZE_MB` in `.env`

### Debug Mode

Enable debug logging by modifying the logging level in `telegram_podcast_bot.py`:

```python
logging.basicConfig(level=logging.DEBUG)
```

## Security Notes

- Never commit your `.env` file to version control
- Keep your API keys secure
- The bot only processes PDF files
- Temporary files are automatically cleaned up

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 