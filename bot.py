import discord
import google.generativeai as genai
import random
import os

# Φόρτωση μεταβλητών από το Railway
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Ρύθμιση Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Η λίστα με τα "γαλλικά"
vrisies = ["ΠΑΛΙΟΤΑΓΑΡΙ", "ΜΠΑΣΤΟΥΝΟΒΛΑΧΕ", "ΤΣΟΠΑΝΗ", "ΓΙΔΟΒΟΣΚΕ", "ΤΣΟΓΛΑΝΙ", "ΤΕΝΕΚΕ ΞΕΓΑΝΩΤΕ", "ΚΑΤΣΑΠΛΙΑ", "ΜΠΟΥΧΕΣΑ", "ΖΑΓΑΡΙ", "ΒΛΑΧΟΔΗΜΑΡΧΕ", "ΣΦΟΥΓΓΑΡΟΚΩΛΑΡΙΕ", "ΚΟΥΡΑΔΟΚΟΦΤΗ", "ΛΙΝΑΤΣΑ", "ΧΑΪΒΑΝΙ", "ΞΥΛΟΓΙΑΝΝΗ", "ΠΑΡΤΑΛΙ", "ΛΕΧΡΙΤΗ", "ΜΠΑΤΑΛΗ", "ΚΟΠΡΟσκυλο", "ΣΤΟΥΡΝΑΡΙ", "ΧΑΧΟΛΟ", "ΚΑΡΑΓΚΙΟΖΗ", "ΜΠΕΧΛΙΒΑΝΗ", "ΤΣΑΠΑΤΣΟΥΛΗ"]

# Ρύθμιση Intents - Ζητάμε ΜΟΝΟ τα απαραίτητα για να μη βαράει το Discord
intents = discord.Intents.default()
intents.message_content = True 

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Ο {client.user} είναι έτοιμος για δράση!')

@client.event
async def on_message(message):
    # Log για να βλέπουμε στο Railway αν ακούει
    print(f"Είδα μήνυμα από {message.author}: {message.content}")

    # Μην απαντάς στον εαυτό σου
    if message.author == client.user:
        return
    
    # Διαλέγουμε 4 τυχαίες βρισιές για το prompt
    pool = random.sample(vrisies, 4)
    prompt = f"Είσαι ένας αγροίκος και εριστικός τύπος από το χωριό. Απάντα σύντομα και εριστικά σε αυτό: '{message.content}'. Χρησιμοποίησε οπωσδήποτε μερικές από αυτές τις λέξεις: {', '.join(pool)}. Μην χρησιμοποιείς bold."

    try:
        response = model.generate_content(prompt)
        if response.text:
            await message.channel.send(response.text)
    except Exception as e:
        print(f"Σφάλμα στο Gemini: {e}")

client.run(DISCORD_TOKEN)
