import streamlit as st
import random
import urllib.parse
from datetime import date

class DailyJokeClub:
    def __init__(self):
        # Expanded Joke Collection
        self.jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my wife she was drawing her eyebrows too high. She looked surprised.",
            "Why don't scientists trust atoms? Because they make up everything!",
            "I'm afraid for the calendar. Its days are numbered.",
            "Why did the math book look sad? Because it had too many problems.",
            "What do you call a fake noodle? An impasta!",
            "Why did the coffee file a police report? Because it got mugged.",
            "I used to be a baker, but I didn't make enough dough.",
            "Why don't eggs tell jokes? They'd crack each other up!"
        ]

    def generate_sharing_links(self, joke):
        """Generate social media sharing links"""
        encoded_joke = urllib.parse.quote(joke)
        
        return {
            "WhatsApp": f"https://wa.me/?text={encoded_joke}",
            "Telegram": f"https://t.me/share/url?url=Daily%20Joke%20Club&text={encoded_joke}",
            "X (Twitter)": f"https://twitter.com/intent/tweet?text={encoded_joke}%20%23DailyJokeClub",
            "Facebook": f"https://www.facebook.com/sharer/sharer.php?u=https://dailyjokeclub.com&quote={encoded_joke}"
        }

    def show_free_joke(self):
        """Display free joke with social sharing options"""
        st.set_page_config(
            page_title="Daily Joke Club 😂", 
            page_icon="🤣", 
            layout="centered"
        )

        st.title("🎭 Daily Joke Club")
        st.subheader("Your Daily Dose of Laughter! 🤣")

        # Display Free Joke
        free_joke = random.choice(self.jokes)
        st.markdown(f"### 🃏 Today's Free Joke:\n\n*{free_joke}*")

        # Social Sharing Section
        st.markdown("---")
        st.subheader("Share This Joke! 📢")

        # Create columns for sharing buttons
        cols = st.columns(len(self.generate_sharing_links(free_joke)))
        
        for i, (platform, link) in enumerate(self.generate_sharing_links(free_joke).items()):
            with cols[i]:
                st.markdown(f"[Share on {platform}]({link})", unsafe_allow_html=True)

        # Subscription Teaser
        st.markdown("---")
        st.markdown("## Want More Laughs? 🌟")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Premium Features:")
            st.write("""
            - 📆 Daily Fresh Jokes
            - 🌍 Diverse Humor
            - 🤣 Unlimited Laughter
            - 📱 Easy Sharing
            """)
        
        with col2:
            if st.button("🎉 Subscribe for $1/Month!", key="subscribe_btn"):
                st.balloons()
                st.success("Thanks for your interest in Daily Joke Club!")
                # Here you can add actual payment integration

def main():
    joke_club = DailyJokeClub()
    joke_club.show_free_joke()

if __name__ == "__main__":
    main()
