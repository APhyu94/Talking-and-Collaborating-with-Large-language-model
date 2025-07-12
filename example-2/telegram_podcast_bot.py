import os
import logging
import asyncio
from typing import Optional
from pathlib import Path
import tempfile
import shutil

# Telegram Bot
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, ContextTypes, CommandHandler

# PDF Processing
import PyPDF2
import pdfplumber

# AI and Text Processing
import google.generativeai as genai
from dotenv import load_dotenv

# Audio Generation
from gtts import gTTS
import io

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('podcast_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-pro')

# Configure Gemini
genai.configure(api_key=GEMINI_API_KEY)

class PodcastBot:
    def __init__(self):
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.temp_dir = Path("temp_audio")
        self.temp_dir.mkdir(exist_ok=True)
        
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        welcome_message = """
🎙️ **PDF to Podcast Bot**

I automatically convert PDF documents into podcast audio files!

**How to use:**
1. Upload any PDF file to this chat
2. I'll extract the text and generate a podcast script
3. Convert it to audio and send it back to you

**Features:**
• Automatic PDF processing
• AI-powered script generation
• High-quality audio synthesis
• Real-time progress updates

Just upload a PDF and watch the magic happen! 🚀
        """
        
        keyboard = [
            [InlineKeyboardButton("📖 How it works", callback_data="help")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, reply_markup=reply_markup, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
📚 **How the PDF to Podcast Bot Works:**

1. **PDF Upload** 📄
   - Upload any PDF file to the chat
   - Bot automatically detects and starts processing

2. **Text Extraction** 🔍
   - Extracts all text content from the PDF
   - Handles various PDF formats and layouts

3. **Script Generation** ✍️
   - Uses Gemini AI to create engaging podcast scripts
   - Maintains key information while making it conversational

4. **Audio Synthesis** 🎵
   - Converts the script to natural-sounding speech
   - Uses gTTS for high-quality audio generation

5. **Delivery** 📤
   - Sends the audio file back to the chat
   - Provides progress updates throughout the process

**Supported Languages:** English (default)
**Max PDF Size:** 20MB
**Processing Time:** 2-5 minutes depending on PDF size

Try uploading a PDF now! 🎙️
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """Extract text from PDF using multiple methods"""
        text = ""
        
        try:
            # Method 1: Try with PyPDF2
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            
            # If PyPDF2 didn't extract much text, try pdfplumber
            if len(text.strip()) < 100:
                logger.info("PyPDF2 extracted minimal text, trying pdfplumber...")
                with pdfplumber.open(pdf_path) as pdf:
                    for page in pdf.pages:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            
        except Exception as e:
            logger.error(f"Error extracting text from PDF: {e}")
            raise
        
        if not text.strip():
            raise ValueError("No text could be extracted from the PDF")
        
        return text.strip()
    
    async def generate_podcast_script(self, text: str) -> str:
        """Generate a podcast script from the extracted text using Gemini"""
        prompt = f"""
You are a professional podcast script writer. Convert the following text into an engaging podcast script.

**Requirements:**
- Make it conversational and engaging
- Maintain all important information
- Add natural transitions and flow
- Keep it under 10 minutes when spoken (approximately 1500 words)
- Use a friendly, informative tone
- Structure it with clear sections
- Add brief pauses and emphasis markers where appropriate

**Text to convert:**
{text[:8000]}  # Limit text length for API

**Format the script as:**
[Introduction]
[Main content with clear sections]
[Conclusion/Summary]

Make it sound natural when spoken aloud.
        """
        
        try:
            response = self.model.generate_content(prompt)
            script = response.text
            
            if not script:
                raise ValueError("Failed to generate script")
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating script with Gemini: {e}")
            raise
    
    async def text_to_speech(self, script: str, output_path: Path) -> Path:
        """Convert text to speech using gTTS"""
        try:
            # Create gTTS object
            tts = gTTS(text=script, lang='en', slow=False)
            
            # Save to file
            tts.save(str(output_path))
            
            return output_path
            
        except Exception as e:
            logger.error(f"Error converting text to speech: {e}")
            raise
    
    async def send_progress_update(self, context: ContextTypes.DEFAULT_TYPE, chat_id: int, message: str):
        """Send progress update to the chat"""
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"🔄 {message}",
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error sending progress update: {e}")
    
    async def handle_pdf_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle PDF file uploads"""
        message = update.message
        chat_id = message.chat_id
        
        # Check if the uploaded file is a PDF
        if not message.document or not message.document.file_name.lower().endswith('.pdf'):
            return
        
        # Check file size (limit to 20MB)
        if message.document.file_size > 20 * 1024 * 1024:
            await message.reply_text("❌ File too large! Please upload a PDF smaller than 20MB.")
            return
        
        # Send initial confirmation
        status_message = await message.reply_text(
            "📄 **PDF Detected!**\n\nStarting podcast generation process...",
            parse_mode='Markdown'
        )
        
        try:
            # Step 1: Download the PDF
            await self.send_progress_update(context, chat_id, "📥 Downloading PDF...")
            file = await context.bot.get_file(message.document.file_id)
            
            # Create temporary file
            temp_pdf = self.temp_dir / f"input_{chat_id}_{message.document.file_name}"
            await file.download_to_drive(temp_pdf)
            
            # Step 2: Extract text
            await self.send_progress_update(context, chat_id, "🔍 Extracting text from PDF...")
            extracted_text = await self.extract_text_from_pdf(temp_pdf)
            
            if len(extracted_text) < 50:
                await message.reply_text("❌ Could not extract enough text from the PDF. Please try a different file.")
                return
            
            # Step 3: Generate podcast script
            await self.send_progress_update(context, chat_id, "✍️ Generating podcast script with AI...")
            script = await self.generate_podcast_script(extracted_text)
            
            # Step 4: Convert to speech
            await self.send_progress_update(context, chat_id, "🎵 Converting script to audio...")
            output_filename = f"podcast_{chat_id}_{message.document.file_name.replace('.pdf', '.mp3')}"
            output_path = self.temp_dir / output_filename
            
            await self.text_to_speech(script, output_path)
            
            # Step 5: Send the audio file
            await self.send_progress_update(context, chat_id, "📤 Uploading audio file...")
            
            with open(output_path, 'rb') as audio_file:
                await context.bot.send_audio(
                    chat_id=chat_id,
                    audio=audio_file,
                    title=f"Podcast: {message.document.file_name.replace('.pdf', '')}",
                    performer="AI Podcast Bot",
                    caption="🎙️ Your podcast is ready! Generated from the uploaded PDF."
                )
            
            # Send completion message
            await context.bot.send_message(
                chat_id=chat_id,
                text="✅ **Podcast Generation Complete!**\n\nYour audio file has been generated and sent above. Enjoy listening! 🎧",
                parse_mode='Markdown'
            )
            
            # Clean up temporary files
            temp_pdf.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
            
            logger.info(f"Successfully processed PDF for chat {chat_id}")
            
        except Exception as e:
            logger.error(f"Error processing PDF for chat {chat_id}: {e}")
            await message.reply_text(
                f"❌ **Error processing PDF:**\n\n{str(e)}\n\nPlease try again with a different file.",
                parse_mode='Markdown'
            )
            
            # Clean up on error
            temp_pdf.unlink(missing_ok=True)
            output_path.unlink(missing_ok=True)
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        logger.error(f"Update {update} caused error {context.error}")
        
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "❌ An error occurred while processing your request. Please try again."
            )

def main():
    """Main function to run the bot"""
    if not TELEGRAM_BOT_TOKEN:
        logger.error("TELEGRAM_BOT_TOKEN not found in environment variables")
        return
    
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY not found in environment variables")
        return
    
    # Create bot instance
    bot = PodcastBot()
    
    # Create application
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", bot.start_command))
    application.add_handler(CommandHandler("help", bot.help_command))
    application.add_handler(MessageHandler(filters.Document.ALL, bot.handle_pdf_upload))
    
    # Add error handler
    application.add_error_handler(bot.error_handler)
    
    # Start the bot
    logger.info("Starting PDF to Podcast Bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main() 