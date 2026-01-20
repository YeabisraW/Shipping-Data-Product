import os
import json
import asyncio
import logging
from datetime import datetime
from pathlib import Path

from telethon import TelegramClient, errors
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.types import MessageMediaPhoto
from dotenv import load_dotenv

# ---------------------------
# Load environment variables
# ---------------------------
load_dotenv()
API_ID = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")

if not API_ID or not API_HASH:
    raise ValueError("Telegram API credentials not found in .env")

# ---------------------------
# Channels
# ---------------------------
CHANNELS = {
    "chemed": "chemed",
    "lobelia4cosmetics": "lobelia4cosmetics",
    "tikvahpharma": "tikvahpharma",
}

# ---------------------------
# Paths
# ---------------------------
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
MSG_DIR = RAW_DIR / "telegram_messages" / datetime.utcnow().strftime("%Y-%m-%d")
IMG_DIR = RAW_DIR / "images"
LOG_DIR = BASE_DIR / "logs"

MSG_DIR.mkdir(parents=True, exist_ok=True)
IMG_DIR.mkdir(parents=True, exist_ok=True)
LOG_DIR.mkdir(parents=True, exist_ok=True)

# ---------------------------
# Logging
# ---------------------------
logging.basicConfig(
    filename=LOG_DIR / "scraper.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# ---------------------------
# Telegram client
# ---------------------------
client = TelegramClient("telegram_scraper", API_ID, API_HASH)

# ---------------------------
# Scrape function
# ---------------------------
async def scrape_channel(name, username):
    print(f"\n➡ Scraping: {name}")
    records = []
    count = 0

    try:
        entity = await client.get_entity(username)

        # Join safely
        try:
            await client(JoinChannelRequest(entity))
        except errors.UserAlreadyParticipantError:
            pass
        except errors.InviteRequestSentError:
            print("⚠ Join request sent — try again later")
            return

        async for msg in client.iter_messages(entity, limit=300):
            if not msg.text and not msg.media:
                continue

            record = {
                "message_id": msg.id,
                "channel": name,
                "date": msg.date.isoformat() if msg.date else None,
                "text": msg.text,
                "views": msg.views,
                "forwards": msg.forwards,
                "has_media": bool(msg.media),
                "image_path": None
            }

            if isinstance(msg.media, MessageMediaPhoto):
                ch_img_dir = IMG_DIR / name
                ch_img_dir.mkdir(exist_ok=True)
                img_path = ch_img_dir / f"{msg.id}.jpg"
                await client.download_media(msg.media, img_path)
                record["image_path"] = str(img_path)

            records.append(record)
            count += 1

            if count % 50 == 0:
                print(f"  scraped {count} messages...")

        out_file = MSG_DIR / f"{name}.json"
        with open(out_file, "w", encoding="utf-8") as f:
            json.dump(records, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {count} messages → {out_file.name}")

    except Exception as e:
        logging.error(f"{name}: {e}")
        print(f"❌ Error scraping {name}: {e}")

# ---------------------------
# Main
# ---------------------------
async def main():
    await client.start()
    for name, username in CHANNELS.items():
        await scrape_channel(name, username)
    await client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
