import streamlit as st
import random
from datetime import date
import requests
import os

# Enhanced Joke Collection with More Variety
jokes = [
    # English Jokes
    "Why did the tomato turn red? It saw the salad dressing!",
    "What do you call a bear with no teeth? A gummy bear!",
    "Why was the broom late? It swept in!",
    "What's orange and sounds like a parrot? A carrot!",
    "Why don't eggs tell jokes? They'd crack up!",
    
    # Arabic Jokes
    "لماذا لا يستطيع الكتاب أن يخبر نكتة؟ لأنه سيتمزق من الضحك!",
    "ما هو شيء يدخل أخضر ويخرج أحمر؟ البطيخ في سباق!",
    "لماذا لم يذهب الكمبيوتر إلى الحفلة؟ لأنه كان محمولاً!",
    
    # Multilingual Fun
    "Why did the math book look sad? Because it had too many problems!",
    "كيف يضحك المهندس؟ بالهندسة!"
]

class JokeClub:
    def __init__(self):
        # Enhanced Security: Use Environment Variables
        self.PAYPAL_CLIENT_ID = os.getenv('PAYPAL_CLIENT_ID', 'default_client_id')
        self.PAYPAL_SECRET = os.getenv('PAYPAL_SECRET', 'default_secret')
        self.PAYPAL_API = "https://api-m.sandbox.paypal.com"

    def get_paypal_token(self):
        """Enhanced PayPal Token Retrieval with Error Handling"""
        try:
            url = f"{self.PAYPAL_API}/v1/oauth2/token"
            headers = {
                "Accept": "application/json", 
                "Accept-Language": "en_US"
            }
            data = {"grant_type": "client_credentials"}
            
            response = requests.post(
                url, 
                auth=(self.PAYPAL_CLIENT_ID, self.PAYPAL_SECRET), 
                data=data, 
                timeout=10
            )
            
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json().get("access_token")
        
        except requests.exceptions.RequestException as e:
            st.error(f"Payment Gateway Error: {e}")
            return None

    def render_joke_app(self):
        """Main Application Rendering"""
        st.set_page_config(
            page_title="Daily Joke Club 😂", 
            page_icon="🤣", 
            initial_sidebar_state="expanded"
        )

        # Multilingual Title
        st.title("🎭 Daily Joke Club | نادي النكات اليومية")
        
        # Sidebar for Additional Information
        st.sidebar.header("App Features 🌟")
        st.sidebar.info("""
        - Daily Fresh Jokes 🃏
        - Multilingual Support 🌍
        - Easy Subscription 💳
        - Share Laughter 😄
        """)

        # Subscription Management
        if "subscribed" not in st.session_state:
            st.session_state.subscribed = False

        if not st.session_state.subscribed:
            self.render_subscription_section()
        else:
            self.render_joke_section()

    def render_subscription_section(self):
        """Subscription UI with Enhanced Engagement"""
        st.info("🌈 Join the Laughter League! Just $1/month")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Why Subscribe? 🤔")
            st.write("""
            - Daily Fresh Jokes
            - Multilingual Content
            - Share & Spread Joy
            - Support Comedy!
            """)
        
        with col2:
            if st.button("🎉 Subscribe Now!", key="subscribe_btn"):
                token = self.get_paypal_token()
                if token:
                    st.session_state.subscribed = True
                    st.success("🎊 Welcome to the Joke Club!")
                    st.balloons()
                else:
                    st.error("Payment Failed. Please try again later.")

    def render_joke_section(self):
        """Enhanced Joke Delivery Section"""
        # Deterministic Joke Selection
        today = date.today().day
        joke_index = today % len(jokes)
        daily_joke = jokes[joke_index]

        st.success(f"🃏 Today's Joke: {daily_joke}")
        
        # Social Sharing with Enhanced Links
        st.subheader("Share the Laughter! 🤣")
        
        sharing_links = {
            "WhatsApp": f"https://wa.me/?text={daily_joke}",
            "Telegram": f"https://t.me/share/url?text={daily_joke}",
            "Twitter": f"https://twitter.com/intent/tweet?text={daily_joke}"
        }
        
        cols = st.columns(len(sharing_links))
        for i, (platform, link) in enumerate(sharing_links.items()):
            with cols[i]:
                st.markdown(f"[{platform}]({link})")

def main():
    joke_club = JokeClub()
    joke_club.render_joke_app()

if __name__ == "__main__":
    main()
