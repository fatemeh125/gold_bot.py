import requests
import time
from datetime import datetime
import os

TELEGRAM_TOKEN = os.environ.get("8975743731:AAHeOpfE6Zqq3wp3ccfHv_6DK2xeb-CAsik", "")
CHAT_ID = os.environ.get("7933664620", "")

PRICE_ALERT = 161_000_000
PRICE_BUY   = 154_000_000
CHECK_INTERVAL = 60

def send_telegram(message):
    for base_url in ["https://api.telegram.org", "https://tg.i-c-a.su"]:
        try:
            url = f"{base_url}/bot{TELEGRAM_TOKEN}/sendMessage"
            resp = requests.post(url, data={
                "chat_id": CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }, timeout=15)
            if resp.status_code == 200:
                print("پیام ارسال شد!")
                return
        except Exception as e:
            print(f"خطا: {e}")

def get_gold_price():
    sources = [
        ("https://call4.tgju.org/ajax.json", "tgju"),
        ("https://api.wallex.ir/v1/markets", "wallex"),
    ]
    for url, source in sources:
        try:
            headers = {"User-Agent": "Mozilla/5.0", "Referer": "https://www.tgju.org/"}
            resp = requests.get(url, headers=headers, timeout=10)
            data = resp.json()
            if source == "tgju":
                price = int(str(data["current"]["geram18"]["p"]).replace(",",""))
                return price
        except Exception as e:
            print(f"خطا {source}: {e}")
    return None

def main():
    print("ربات شروع کرد...")
    send_telegram("✅ <b>ربات طلا فعال شد!</b>")
    last_alert = None

    while True:
        now = datetime.now().strftime("%H:%M:%S")
        price = get_gold_price()

        if price is None:
            print(f"[{now}] خطا در قیمت")
            time.sleep(CHECK_INTERVAL)
            continue

        print(f"[{now}] قیمت: {price:,} ریال")

        if price <= PRICE_BUY:
            if last_alert != "buy":
                send_telegram(
                    f"🟢🟢 <b>سیگنال خرید!</b>\n💰 {price:,} ریال\n"
                    f"⏰ {now}\n👉 <b>همین الان بخر!</b>"
                )
                last_alert = "buy"
        elif price <= PRICE_ALERT:
            if last_alert != "alert":
                send_telegram(
                    f"🔔 <b>آلارم قیمت!</b>\n💰 {price:,} ریال\n"
                    f"⏰ {now}\n👀 <b>آماده باش!</b>"
                )
                last_alert = "alert"
        else:
            last_alert = None

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
