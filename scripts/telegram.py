import os
import json
import urllib.request
import urllib.parse

TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()


def send_telegram_message(text):
    if not TOKEN or not CHAT_ID:
        print("[TELEGRAM] Secretos TELEGRAM_TOKEN / TELEGRAM_CHAT_ID no configurados. Omitiendo envío.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = urllib.parse.urlencode({
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": "false"
    }).encode("utf-8")
    req = urllib.request.Request(url, data=data)
    with urllib.request.urlopen(req, timeout=15) as resp:
        print("[TELEGRAM OK]", resp.status)


def main():
    try:
        with open("data/blog_posts.json", "r", encoding="utf-8") as f:
            blog = json.load(f)
        with open("data/marketing_showcase.json", "r", encoding="utf-8") as f:
            showcase = json.load(f)
    except Exception as e:
        print("[TELEGRAM] No se pudieron leer los JSON:", e)
        return

    top_post = blog["posts"][0]
    msg = (
        f"🏆 <b>DAZ PREMIUM FIT PERFORMANCE • INFORME DIARIO</b>\n\n"
        f"📌 <b>{top_post['category']}</b>\n"
        f"<b>{top_post['title']}</b>\n\n"
        f"{top_post['summary']}\n\n"
        f"🔥 <b>Escaparate Oficial:</b> {showcase['headline']}\n"
        f"👉 <a href='https://dazpremiumfit.com'>Visitar Tienda DAZ Premium Fit</a>"
    )
    send_telegram_message(msg)


if __name__ == "__main__":
    main()
