import streamlit as st
import random
from datetime import date
import requests

# بيانات PayPal Sandbox
PAYPAL_CLIENT_ID = "AQd5IZObL6YTejqYpN0LxADLMtqbeal1ahbgNNrDfFLcKzMl6goF9BihgMw2tYnb4suhUfprhI-Z8eoC"
PAYPAL_SECRET = "EPk46EBw3Xm2W-R0Uua8sLsoDLJytgSXqIzYLbbXCk_zSOkdzFx8jEbKbKxhjf07cnJId8gt6INzm6_V"
PAYPAL_API = "https://api-m.sandbox.paypal.com"

# قائمة نكات بسيطة ومضحكة جدًا
jokes = [
    "Why did the tomato turn red? It saw the salad dressing!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why was the broom late? It swept in!",
    "What’s orange and sounds like a parrot? A carrot!",
    "Why don’t eggs tell jokes? They’d crack up!",
    "What do you call a lazy kangaroo? A pouch potato!",
    "Why did the banana go to school? It wanted to improve its peel-festeem!"
]

# واجهة جذابة باللغة الإنجليزية
st.title("Daily Joke Club")
st.write("Subscribe for just $1/month and enjoy a fresh, hilarious joke every day!")

# الحصول على رمز الوصول من PayPal Sandbox
def get_paypal_token():
    url = f"{PAYPAL_API}/v1/oauth2/token"
    headers = {"Accept": "application/json", "Accept-Language": "en_US"}
    data = {"grant_type": "client_credentials"}
    response = requests.post(url, auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET), data=data)
    return response.json().get("access_token") if response.status_code == 200 else None

# حالة الاشتراك
if "subscribed" not in st.session_state:
    st.session_state.subscribed = False

if not st.session_state.subscribed:
    st.info("Join the club for only 3 cents a day and laugh non-stop!")
    if st.button("Subscribe Now for $1/month"):
        token = get_paypal_token()
        if token:
            st.session_state.subscribed = True
            st.success("Payment successful! Welcome to the Daily Joke Club!")
            st.balloons()  # تأثير احتفالي
        else:
            st.error("Payment failed. Please try again!")
    st.markdown("[Pay $1/month via PayPal Sandbox](https://www.sandbox.paypal.com) - Use a test account to subscribe!")
else:
    # عرض النكتة اليومية
    today = date.today().day
    joke_index = today % len(jokes)
    daily_joke = jokes[joke_index]
    st.success(f"Your Daily Joke: {daily_joke}")
    st.warning("😂 Your daily laugh is ready! Share it and come back tomorrow!")

    # روابط المشاركة
    whatsapp_link = f"https://wa.me/?text=Check%20out%20this%20hilarious%20joke%20from%20Daily%20Joke%20Club:%20{daily_joke}"
    telegram_link = f"https://t.me/share/url?url=Daily%20Joke%20Club&text={daily_joke}"
    twitter_link = f"https://twitter.com/intent/tweet?text={daily_joke}%20-%20From%20Daily%20Joke%20Club"
    
    st.subheader("Share the Fun!")
    st.markdown(f"[Share on WhatsApp]({whatsapp_link}) | [Share on Telegram]({telegram_link}) | [Share on Twitter]({twitter_link})")
    st.info("Spread the laughter with friends and grow the club!")

# تنبيهات تحفيزية
if st.session_state.subscribed:
    st.info("🎉 You’re a VIP member! Enjoy your daily dose of fun!")
else:
    st.warning("⏰ Don’t miss out! Subscribe now for endless laughs!")
