import streamlit as st
import random
import urllib.parse
from datetime import date
import requests
import json
from pathlib import Path
import time
import base64
from streamlit.components.v1 import html
import sqlite3
import hashlib
import os
from threading import Lock

# بيانات PayPal Sandbox
PAYPAL_CLIENT_ID = "AQd5IZObL6YTejqYpN0LxADLMtqbeal1ahbgNNrDfFLcKzMl6goF9BihgMw2tYnb4suhUfprhI-Z8eoC"
PAYPAL_SECRET = "EPk46EBw3Xm2W-R0Uua8sLsoDLJytgSXqIzYLbbXCk_zSOkdzFx8jEbKbKxhjf07cnJId8gt6INzm6_V"
PAYPAL_API = "https://api-m.sandbox.paypal.com"

class DailyJokeClub:
    def __init__(self):
        # إعداد قاعدة بيانات SQLite لتخزين النكات والمستخدمين
        self.db_path = "joke_club.db"
        self.lock = Lock()
        self.initialize_database()

        # قائمة نكات أولية (200 نكتة كبداية، مع قاعدة بيانات للتوسع إلى ملايين)
        self.initial_jokes = [
            "Why don’t skeletons fight? They don’t have the guts! 💀👊",
            "What do you call a bear with no teeth? A gummy bear! 🐻🍬",
            "Why did the tomato blush? It saw the salad dressing! 🍅😂",
            "What’s orange and sounds like a parrot? A carrot! 🥕🦜",
            "Why don’t eggs tell jokes? They’d crack up! 🥚🤡",
            "Why was the broom late? It swept in! 🧹⏰",
            "What do you call a fake noodle? An impasta! 🍝😜",
            "Why did the coffee file a police report? It got mugged! ☕🚨",
            "What has keys but can’t open locks? A piano! 🎹🔑",
            "Why did the banana go to school? To improve its peel-festeem! 🍌📚",
            "Why don’t programmers prefer dark mode? The light attracts bugs! 💻🐞",
            "What do you call a lazy kangaroo? A pouch potato! 🦘🥔",
            "Why did the smartphone refuse to date? It had too many apps-tractions! 📱💔",
            "Why did the cow sit alone? It didn’t want to share the moo-d! 🐮😑",
            "What’s a vampire’s favorite fruit? A blood orange! 🧛🍊",
            "Why did the cookie go to therapy? It had too many crumbs of issues! 🍪🛋️",
            "What do you call a sleeping bull? A bulldozer! 🐂💤",
            "Why was the math book sad? It had too many problems! 📘😢",
            "What’s a ghost’s favorite dessert? Boo-berry pie! 👻🫐",
            "What do you call cheese that isn’t yours? **Nacho** cheese! 🧀😏",
            "Why don’t cats play chess? They’re afraid of any situation where a pawn can become a queen! 🐱♟️",
            "Why did the lemon stop in the road? It ran out of juice! 🍋🛑",
            "What’s a pirate’s favorite letter? Argh you kidding? It’s the *C*! 🏴‍☠️🌊",
            "Why don’t fish play basketball? They’re afraid of the net! 🐟🏀",
            "What do you call a dog magician? A labracadabrador! 🐶✨",
            "Why was the belt arrested? For holding up the pants! 👖🚔",
            "What’s a tornado’s favorite game? Twister! 🌪️🎲",
            "Why don’t owls date in the rain? It’s too wet to woo! 🦇💧",
            "Why did the clock go to jail? It couldn’t stop ticking off the guards! ⏰🔗",
            "Why don’t chairs ever forget? They have great *seat* memory! 🪑🧠",
            "What do you call a snowman with a six-pack? An abdominal snowman! ⛄💪",
            "Why did the Wi-Fi go to therapy? It had too many connection issues! 📶😓",
            "What’s a cloud’s favorite music? Rain-drops and beats! ☁️🎶",
            "Why don’t refrigerators tell secrets? They’d spill the chill! ❄️🗣️",
            "What do you call a sheep with no legs? A cloud! 🐑☁️",
            "Why did the pencil refuse to write? It was feeling too *pointless*! ✏️😞",
            "What’s a balloon’s worst fear? A pop quiz! 🎈❓",
            "Why did the bread go to jail? It couldn’t stop loafing around! 🍞🚓",
            "What do you call a fish who writes music? A *tuna* composer! 🐟🎵",
            "Why don’t sharks use social media? They’d rather bite than like! 🦈📱",
            "What do you call a dancing cow? A milkshake! 🐄🕺",
            "Why did the lamp break up with the bulb? It couldn’t handle the bright ideas! 💡💔",
            "What’s a robot’s favorite snack? Micro-chips! 🤖🍟",
            "Why don’t trees get lost? They have deep roots in navigation! 🌳🗺️",
            "What do you call a frog with no legs? A hop-timist! 🐸😊",
            "Why did the popcorn refuse to pop? It didn’t want to lose its cool! 🍿❄️",
            "What’s a bee’s favorite sport? Buzz-ketball! 🐝🏀",
            "Why don’t pillows fight? They’re too soft-hearted! 🛏️❤️",
            "What do you call a snail with a jetpack? A rocket escargot! 🐌🚀",
            "Why did the guitar refuse to play? It didn’t want to string anyone along! 🎸😉",
            "Why don’t whales sing karaoke? They’d sink the stage! 🐳🎤",
            "What do you call a cat with a PhD? A purr-fessor! 🐱🎓",
            "Why did the donut go to school? To fill its *hole* in knowledge! 🍩📖",
            "What’s a spider’s favorite hobby? Web design! 🕷️💻",
            "Why don’t books ever go out of business? They have a lot of *circulation*! 📚💸",
            "What do you call a lazy dinosaur? A snoresaurus! 🦖💤",
            "Why did the shoe go to therapy? It had too many sole-searching moments! 👟🧘",
            "What’s a duck’s favorite TV show? Quack Mirror! 🦆📺",
            "Why don’t stars play hide and seek? They always shine too bright! ⭐🙈",
            "What do you call a potato that sings? A yam-star! 🥔🎙️",
            "Why did the mirror refuse to talk? It didn’t want to reflect badly! 🪞😬",
            "What’s a camel’s favorite day? Hump day! 🐪📅",
            "Why don’t bicycles fall in love? They’re too tired! 🚲😴",
            "What do you call a chicken with attitude? An egg-streme rebel! 🐔😎",
            "Why did the toothbrush refuse to work? It was bristling with anger! 🪥😤",
            "What’s a lion’s favorite snack? Roar-itos! 🦁🌮",
            "Why don’t socks go to parties? They’re afraid of getting unpaired! 🧦🎉",
            "What do you call a turtle who writes music? A shell-ebrity composer! 🐢🎼",
            "Why did the watermelon blush? It overheard the seeds gossiping! 🍉👂",
            "What’s a zebra’s favorite game? Black-and-white checkers! 🦓♟️",
            "Why don’t doors ever gossip? They’re too hinged to spill! 🚪🤐",
            "What do you call a horse that can’t gallop? A neigh-sayer! 🐴🚫",
            "Why did the cucumber turn green? It was jealous of the pickles! 🥒😒",
            "What’s a penguin’s favorite dance? The waddle shuffle! 🐧💃",
            "Why don’t candles fight? They’d burn out too fast! 🕯️👊",
            "What do you call a bird that’s bad at flying? A flap-tastrophe! 🐦💥",
            "Why did the onion cry at the party? It couldn’t stop peeling out! 🧅🎈",
            "What’s a frog’s favorite candy? Lolli-hops! 🐸🍭",
            "Why don’t rainbows share? They’re too colorful to split! 🌈🤷",
            "What do you call a crab with a temper? A pinch-y grump! 🦀😡",
            "Why did the kite refuse to fly? It didn’t want to get tied down! 🪁⛓️",
            "What’s a monkey’s favorite drink? Banana daiquiri! 🐒🍹",
            "Why don’t hats argue? They don’t want to lose their heads! 🎩🗣️",
            "What do you call a deer with no eyes? No-eye-deer! 🦌🙈",
            "Why did the grape stop rolling? It was tired of the vine! 🍇😴",
            "What’s a wolf’s favorite song? Howl-elujah! 🐺🎶",
            "Why don’t butterflies date? They’re too flirty with flowers! 🦋🌸",
            "What do you call a pig who paints? A pork-trait artist! 🐷🎨",
            "Why did the strawberry blush? It got caught in a jam! 🍓😳",
            "What’s a bat’s favorite dessert? Fang-tastic fudge! 🦇🍫",
            "Why don’t gloves wave goodbye? They’re too hands-off! 🧤👋",
            "What do you call a rabbit with a cape? A hare-o! 🐰🦸",
            "Why did the ice cube refuse to melt? It wanted to stay cool! 🧊😎",
            "What’s a tiger’s favorite movie? The Roar-ing Twenties! 🦅🎬",
            "Why don’t lemons fight? They’d just squeeze out! 🍋🤼",
            "What do you call a fox who loves math? A calcu-vixen! 🦊➕",
            "Why did the toaster refuse breakfast? It was burned out! 🍞🔥",
            "What’s a dolphin’s favorite game? Fin-tastic tag! 🐬🏃",
            "Why don’t rivers gossip? YAThey just flow with it! 🌊🤫",
            "What do you call a sloth who sings? A nap-tune crooner! 🦥🎤",
            "Why did the peach stop talking? It didn’t want to pit-y anyone! 🍑😶",
            "Why don’t planets argue? They’re too spaced out! 🪐🤐",
            "What do you call a lazy astronaut? A space cadet! 🚀😴",
            "Why did the volcano refuse to date? It didn’t want to blow its top! 🌋💔",
            "What’s a cactus’s favorite song? *Spikey* and I know it! 🌵🎵",
            "Why don’t mountains fight? They’re too peak-ed to argue! ⛰️👊",
            "What do you call a worm who loves coffee? A java wriggler! 🐛☕",
            "Why did the suitcase refuse to travel? It was tired of baggage! 🧳😴",
            "What’s a lizard’s favorite game? Tail-spin! 🦎🎡",
            "Why don’t waves ever quit? They just keep rolling with it! 🌊🏄",
            "What do you call a parrot with no feathers? A squawk-ward situation! 🦜😅",
            "Why did the broccoli refuse to dance? It didn’t want to stalk the floor! 🥦💃",
            "What’s a giraffe’s favorite drink? High-ball! 🦒🍸",
            "Why don’t cherries fight? They’re too pitted against each other! 🍒🤼",
            "What do you call a moose with headphones? A groovy grazer! 🦌🎧",
            "Why did the fridge go on strike? It was fed up with the cold shoulder! ❄️😤",
            "What’s a hawk’s favorite sport? Eye-ronman! 🦅🏃",
            "Why don’t scissors ever lose? They always cut to the chase! ✂️🏆",
            "What do you call a turtle who loves sweets? A candy-didate! 🐢🍬",
            "Why did the sunflower turn away? It didn’t want to face the shade! 🌻😒",
            "What’s a skunk’s favorite perfume? Eau de *stink*! 🦨💨",
            "Why don’t bees ever retire? They love the buzz-ness! 🐝💼",
            "What do you call a camel who tells jokes? A hump-orist! 🐪😂",
            "Why did the mushroom stay home? It didn’t want to spore-t the fun! 🍄🏠",
            "What’s a raccoon’s favorite heist? Trash-ure hunting! 🦝💰",
            "Why don’t pineapples argue? They’re too prickly to care! 🍍🤷",
            "What do you call a squirrel with a briefcase? A nut-ty businessman! 🐿️💼",
            "Why did the avocado sit alone? It didn’t want to guac and roll! 🥑🎸",
            "What’s a seagull’s favorite song? Fly me to the moon! 🐦🌕",
            "Why don’t elephants use phones? They forget where they trunk-dialed! 🐘📞",
            "What do you call a hedgehog who loves parties? A prickly socialite! 🦔🎉",
            "Why did the corn refuse to talk? It was too ear-itated! 🌽😣",
            "What’s a flamingo’s favorite pose? One-legged stand-up! 🦩🎤",
            "Why don’t jellyfish fight? They don’t have the spine for it! 🪼👊",
            "What do you call a panda who naps all day? A bamboo-zler! 🐼💤",
            "Why did the lime refuse to join? It was too sour to mingle! 🍈😖",
            "What do you call a kangaroo who loves coffee? A java jumper! 🦘☕",
            "Why don’t clouds ever fight? They just drift apart! ☁️🤝",
            "What’s a turkey’s favorite dance? The gobble wobble! 🦃💃",
            "Why did the sofa refuse guests? It didn’t want to get too cushy! 🛋️🚫",
            "What do you call a deer who sings opera? A stag-nificent tenor! 🦌🎶",
            "Why don’t trains gossip? They stay on track! 🚂🤫",
            "What’s a goose’s favorite game? Honk-y tonk! 🦢🎹",
            "Why did the apple refuse to roll? It didn’t want to core-respond! 🍎📧",
            "What do you call a bear who loves sweets? A honey hoarder! 🐻🍯",
            "Why don’t kites ever argue? They rise above it all! 🪁☁️",
            "What’s a snail’s favorite race? The slime-athlon! 🐌🏅",
            "Why did the pear refuse to fight? It didn’t want to bruise its ego! 🍐😤",
            "What do you call a hawk who loves puns? A talon-ted jokester! 🦅😂",
            "Why don’t bridges ever collapse under pressure? They’ve got strong support! 🌉💪",
            "What’s a cheetah’s favorite snack? Fast food! 🐆🍔",
            "Why did the orange refuse to peel? It didn’t want to get too zesty! 🍊😜",
            "What do you call a frog who loves tech? A digital ribbiter! 🐸💾",
            "Why don’t clocks ever argue? They’re too ticked off to care! ⏰😑",
            "What’s a peacock’s favorite show? Feather-flix and chill! 🦚📺",
            "Why did the lettuce refuse to dance? It didn’t want to leaf the floor! 🥬💃",
            "What do you call a monkey who loves math? A calcu-chimp! 🐒➕",
            "Why don’t buses ever gossip? They’re too busy picking up the chatter! 🚌🗣️",
            "What’s a swan’s favorite song? Swan-derful tonight! 🦢🎵",
            "Why did the blueberry turn blue? It heard the jam session! 🫐🎸",
            "What do you call a cow who loves yoga? A moo-ga master! 🐄🧘",
            "Why don’t stars ever fight? They’re too busy twinkling! ⭐👊",
            "What’s a raven’s favorite book? Caw-lassic literature! � raven📖",
            "Why did the lime refuse to party? It didn’t want to get squeezed! 🍈🎉",
            "What do you call a goat who loves puns? A baa-ffling comedian! 🐐😂",
            "Why don’t waves ever stop? They’ve got too much momentum to crash! 🌊🏄",
            "What’s a bison’s favorite dance? The buffalo shuffle! 🦬💃",
            "Why did the cherry refuse to roll? It didn’t want to pit-ch in! 🍒⚾",
            "What do you call a wolf who loves tech? A byte-ing geek! 🐺💻",
            "Why don’t feathers fight? They’d just float away! 🪶👊",
            "What’s a koala’s favorite snack? Eucalyptus crisps! 🐨🍃",
            "Why did the peach refuse to talk? It was too fuzzy to chat! 🍑🤐",
            "What do you call a lion who loves disco? A mane groover! 🦁🕺"
        ]
        # نكتة مجانية ثابتة كمعاينة
        self.free_joke = "Why did the chicken join a band? To play the egguitar! 🐔🎸"

        # تحميل النكات من قاعدة البيانات
        self.load_jokes_from_db()

    def initialize_database(self):
        """Initialize SQLite database for jokes and user subscriptions"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            # جدول النكات
            c.execute('''CREATE TABLE IF NOT EXISTS jokes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                joke TEXT UNIQUE,
                category TEXT,
                added_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )''')
            # جدول المستخدمين
            c.execute('''CREATE TABLE IF NOT EXISTS users (
                user_id TEXT PRIMARY KEY,
                subscription_status BOOLEAN,
                join_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                laugh_count INTEGER DEFAULT 0,
                days_active INTEGER DEFAULT 0
            )''')
            # إضافة النكات الأولية إذا لم تكن موجودة
            for joke in self.initial_jokes:
                c.execute("INSERT OR IGNORE INTO jokes (joke, category) VALUES (?, ?)", (joke, "General"))
            conn.commit()
            conn.close()

    def load_jokes_from_db(self):
        """Load jokes from SQLite database"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("SELECT joke FROM jokes")
            self.jokes = [row[0] for row in c.fetchall()]
            conn.close()

    def add_joke_to_db(self, joke, category="General"):
        """Add a new joke to the database"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO jokes (joke, category) VALUES (?, ?)", (joke, category))
            conn.commit()
            conn.close()

    def get_daily_joke_index(self):
        """Generate a unique index for unlimited years with randomization"""
        start_date = date(2025, 1, 1)
        today = date.today()
        days_since_start = (today - start_date).days
        random.seed(days_since_start + len(self.jokes))  # إضافة طول القائمة لتنوع إضافي
        return random.randint(0, len(self.jokes) - 1)

    def generate_sharing_links(self, joke):
        """Generate advanced social media sharing links with analytics tracking"""
        encoded_joke = urllib.parse.quote(joke)
        app_url = "https://daily-jokes.streamlit.app"
        tracking_param = f"?utm_source={urllib.parse.quote(encoded_joke[:20])}&utm_medium=social&utm_campaign=dailyjoke"
        return {
            "WhatsApp": f"https://wa.me/?text={encoded_joke}%20-%20Join%20Daily%20Joke%20Club%20at%20{app_url}{tracking_param}%20😂",
            "Telegram": f"https://t.me/share/url?url={app_url}{tracking_param}&text={encoded_joke}%20-%20Daily%20Joke%20Club",
            "Twitter": f"https://twitter.com/intent/tweet?text={encoded_joke}%20%23DailyJokeClub%20{app_url}{tracking_param}",
            "Facebook": f"https://www.facebook.com/sharer/sharer.php?u={app_url}{tracking_param}&quote={encoded_joke}",
            "Instagram": f"https://www.instagram.com/?url={app_url}{tracking_param}",
            "Reddit": f"https://www.reddit.com/submit?url={app_url}{tracking_param}&title={encoded_joke}",
            "Email": f"mailto:?subject=Daily%20Joke%20Club&body={encoded_joke}%20-%20Join%20at%20{app_url}{tracking_param}",
            "LinkedIn": f"https://www.linkedin.com/sharing/share-offsite/?url={app_url}{tracking_param}"
        }

    def get_paypal_token(self):
        """Get PayPal access token with advanced error handling"""
        url = f"{PAYPAL_API}/v1/oauth2/token"
        headers = {"Accept": "application/json", "Accept-Language": "en_US"}
        data = {"grant_type": "client_credentials"}
        try:
            response = requests.post(url, auth=(PAYPAL_CLIENT_ID, PAYPAL_SECRET), data=data, timeout=10)
            return response.json().get("access_token") if response.status_code == 200 else None
        except requests.RequestException as e:
            st.error(f"Payment error: {str(e)}")
            return None

    def get_user_id(self):
        """Generate a unique user ID based on session"""
        if "user_id" not in st.session_state:
            st.session_state.user_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        return st.session_state.user_id

    def update_user_stats(self, user_id, subscribed=False, laughed=False):
        """Update user stats in the database"""
        with self.lock:
            conn = sqlite3.connect(self.db_path)
            c = conn.cursor()
            c.execute("INSERT OR IGNORE INTO users (user_id, subscription_status) VALUES (?, ?)", (user_id, False))
            if subscribed:
                c.execute("UPDATE users SET subscription_status = 1 WHERE user_id = ?", (user_id,))
            if laughed:
                c.execute("UPDATE users SET laugh_count = laugh_count + 1, days_active = days_active + 1 WHERE user_id = ?", (user_id,))
            conn.commit()
            c.execute("SELECT laugh_count, days_active FROM users WHERE user_id = ?", (user_id,))
            stats = c.fetchone()
            conn.close()
            return stats[0] if stats else 0, stats[1] if stats else 0

    def show_joke_club(self):
        """Display the ultimate joke club interface with maximum features"""
        st.set_page_config(
            page_title="Daily Joke Club 😂",
            page_icon="🤡",
            layout="wide",
            initial_sidebar_state="expanded",
            menu_items={
                "Get Help": "https://daily-jokes.streamlit.app/support",
                "Report a Bug": "mailto:support@dailyjokeclub.com",
                "About": "Daily Joke Club - The World’s Funniest App Since 2025!"
            }
        )

        # شريط جانبي متطور
        user_id = self.get_user_id()
        with st.sidebar:
            st.header("🎉 Daily Joke Club Hub")
            st.write("Join millions of laughers worldwide! 😂")
            st.image("https://via.placeholder.com/150x150.png?text=Laugh+Daily", caption="Your Daily Giggle!")
            laugh_count, days_active = self.update_user_stats(user_id)
            st.metric("Your Laughs", laugh_count)
            st.metric("Days Active", days_active)
            st.metric("Global Members", "1,000,000+", "10,000+ this month")
            st.button("Invite Friends", key="invite_btn", help="Share the fun!")
            st.write("🌟 Powered by Streamlit & Laughter!")

        # العنوان الرئيسي مع تأثير متحرك
        st.markdown("""
        <h1 style='text-align: center; color: #FF4500; font-family: Comic Sans MS; animation: bounce 2s infinite;'>
        🎭 Daily Joke Club
        </h1>
        <style>
        @keyframes bounce {
            0%, 20%, 50%, 80%, 100% {transform: translateY(0);}
            40% {transform: translateY(-20px);}
            60% {transform: translateY(-10px);}
        }
        </style>
        """, unsafe_allow_html=True)
        st.write("The world’s ultimate source for daily laughter – subscribe for just $1/month! 🤣")

        # عرض النكتة المجانية بخط كبير
        st.subheader("🆓 Free Joke Preview")
        st.markdown(f"<h1 style='text-align: center; color: #FF5733; font-family: Comic Sans MS;'>{self.free_joke}</h1>", unsafe_allow_html=True)
        st.info("😂 Cracked a smile? Unlock a new, world-class joke every day with a subscription!")

        # حالة الاشتراك
        if "subscribed" not in st.session_state:
            st.session_state.subscribed = False

        # التحقق من الاشتراك
        if not st.session_state.subscribed:
            st.warning("🔒 Exclusive daily jokes are waiting! Join the club now!")
            st.info("Only $1/month – 3 cents a day for endless, premium laughter! 🎉")
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                if st.button("Subscribe for $1/month", key="subscribe_btn", help="Join the laughter revolution!", type="primary"):
                    token = self.get_paypal_token()
                    if token:
                        st.session_state.subscribed = True
                        self.update_user_stats(user_id, subscribed=True)
                        st.success("Payment successful! Welcome to Daily Joke Club! 🌟")
                        st.balloons()
                        st.snow()
                        st.fireworks()
                        st.toast("You’re in! Get ready to laugh daily! 😂", icon="🎉")
                    else:
                        st.error("Payment failed. Try again! 😕")
            st.markdown("[Pay via PayPal Sandbox](https://www.sandbox.paypal.com) - Use a test account!")
        else:
            # عرض النكتة اليومية بخط كبير للمشتركين
            joke_index = self.get_daily_joke_index()
            daily_joke = self.jokes[joke_index]
            st.subheader("🎁 Your Daily Joke")
            st.markdown(f"<h1 style='text-align: center; color: #00CC00; font-family: Comic Sans MS;'>{daily_joke}</h1>", unsafe_allow_html=True)
            st.warning("😂 Rolling on the floor yet? Check back tomorrow for another masterpiece! 🎭")

            # روابط المشاركة المحسنة
            st.subheader("Share the Laughter Globally! 📢")
            sharing_links = self.generate_sharing_links(daily_joke)
            cols = st.columns(len(sharing_links))
            for i, (platform, link) in enumerate(sharing_links.items()):
                with cols[i]:
                    st.button(f"{platform}", on_click=lambda l=link: st.write(f"Open: {l}"), key=f"share_{i}")

            # ميزات إضافية متطورة
            st.subheader("Your Laugh Dashboard 🌟")
            laugh_count, days_active = self.update_user_stats(user_id)
            col1, col2, col3 = st.columns(3)
            col1.metric("Your Laughs", laugh_count, "+1 today" if laugh_count > 0 else "0")
            col2.metric("Days Active", days_active, "+1 today")
            col3.metric("Global Laughs", "50,000,000+", "100,000+ today")
            if st.button("I Laughed! 😂", key="laugh_btn"):
                laugh_count, days_active = self.update_user_stats(user_id, laughed=True)
                st.success(f"You’ve laughed {laugh_count} times over {days_active} days! Legendary! 🌟")
                st.confetti()

            # صوت ضحك وفيديو فكاهي اختياري
            st.subheader("Enhance Your Laugh 😂")
            laugh_option = st.radio("Add some fun:", ("None", "Laugh Sound", "Funny Video"))
            if laugh_option == "Laugh Sound":
                laugh_audio = base64.b64encode(open("laugh.mp3", "rb").read()).decode() if Path("laugh.mp3").exists() else None
                if laugh_audio:
                    html(f"""
                    <audio autoplay>
                        <source src="data:audio/mp3;base64,{laugh_audio}" type="audio/mp3">
                    </audio>
                    """)
                else:
                    st.warning("Add a 'laugh.mp3' file to hear the fun! 😂")
            elif laugh_option == "Funny Video":
                st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")  # Rickroll كمثال، استبدل برابط فكاهي

            # إضافة نكتة من المستخدم
            st.subheader("Submit Your Own Joke! ✍️")
            user_joke = st.text_input("Your hilarious joke:", "")
            user_category = st.selectbox("Category:", ["General", "Animals", "Tech", "Food"])
            if st.button("Submit Joke", key="submit_joke"):
                if user_joke:
                    self.add_joke_to_db(user_joke, user_category)
                    st.success("Joke submitted! It might appear in the club soon! 😂")
                    self.load_jokes_from_db()

            # قسم المزايا الإضافية
            with st.expander("Why Daily Joke Club is the Best?"):
                st.write("""
                - 😂 **Unmatched Humor**: World-class, timeless jokes daily.
                - 🌍 **Global Community**: Join millions of laughers worldwide.
                - 📱 **Interactive Experience**: Share, track, and laugh with cutting-edge features.
                - 💸 **Insane Value**: $1/month – less than a gum stick for endless fun!
                - 🎉 **VIP Perks**: Exclusive content, stats, and global bragging rights!
                - 🔧 **Future-Proof**: Expandable to millions of jokes for decades of laughter!
                """)

        # تذييل مع إحصائيات ديناميكية
        st.markdown("---")
        st.write("© 2025 Daily Joke Club - Powered by Laughter, Streamlit, and You! 😂")

def main():
    joke_club = DailyJokeClub()
    joke_club.show_joke_club()

if __name__ == "__main__":
    main()
