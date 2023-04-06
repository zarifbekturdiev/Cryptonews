from datetime import datetime
from pathlib import Path
import requests
import docx
import os
import time
import shutil

from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent.parent.parent
load_dotenv(BASE_DIR / '.env')

TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

folder_to_watch = BASE_DIR / 'data_processing/Ready_posts'
folder_to_move_processed_files = BASE_DIR / 'RussianCrypto/RussianToPost'

# Keep track of the processed files
processed_files = []

while True:
    # Get all docx files in the folder
    docx_files = [f for f in os.listdir(folder_to_watch) if f.endswith('.docx')]

    # Filter out processed files
    new_files = [f for f in docx_files if f not in processed_files]
    if new_files:
        for file in new_files:
            # Process the docx file
            doc = docx.Document(folder_to_watch / file)
            text = '\n'.join([paragraph.text for paragraph in doc.paragraphs])

            # Send the content to the Telegram bot
            url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'
            params = {'chat_id': CHAT_ID, 'text': text}
            response = requests.post(url, data=params)

            # Move the processed file to the specified folder
            shutil.move(folder_to_watch / file, folder_to_move_processed_files / file)

            # Add the file to the list of processed files
            processed_files.append(file)

            print(f'{datetime.now()} Successfully processed and sent {file} to Telegram.')

    # Wait for 1 minutes before checking for new files again
    time.sleep(60)
