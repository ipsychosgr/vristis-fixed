import discord
import google.generativeai as genai
import random
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

vrisies = ["ΠΑΛΙΟΤΑΓΑΡΙ", "ΜΠΑΣΤΟΥΝΟΒΛΑΧΕ", "ΤΣΟΠΑΝΗ", "ΓΙΔΟΒΟΣΚΕ", "ΤΣΟΓΛΑΝΙ", "ΤΕΝΕΚΕ ΞΕΓΑΝΩΤΕ", "ΚΑΤΣΑΠΛΙΑ", "ΜΠΟΥΧΕΣΑ", "ΖΑΓΑΡΙ", "ΒΛΑΧΟΔΗΜΑΡΧΕ", "ΣΦΟΥΓΓΑΡΟΚΩΛΑΡΙΕ", "ΚΟΥΡΑΔΟΚΟΦΤΗ", "ΛΙΝΑΤΣΑ", "ΧΑΪΒΑΝΙ", "ΞΥΛΟΓΙΑΝΝΗ", "ΠΑΡΤΑΛΙ", "ΛΕΧΡΙΤΗ", "ΜΠΑΤΑΛΗ", "ΚΟΠΡΟσκυλο", "ΣΤΟΥΡΝΑΡΙ", "ΧΑΧΟΛΟ", "ΚΑΡΑΓΚΙΟΖΗ", "ΜΠΕΧΛΙΒΑΝΗ", "ΤΣΑΠΑΤΣΟΥΛΗ"]

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Ο {client.user} είναι έτοιμος για δράση!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Το bot θα απαντάει στο 50% των μηνυμάτων για να μην γίνει σπαμ, ή σε κάθε μήνυμα αν θέλεις
    pool = random.sample(vrisies, 4)
    prompt = f"Είσαι ένας αγροίκος και εριστικός τύπος από το χωριό. Απάντα σύντομα και εριστικά σε αυτό: '{message.content}'. Χρησιμοποίησε οπωσδήποτε μερικές από αυτές τις λέξεις: {', '.join(pool)}. Μην χρησιμοποιείς bold."

    try:
        response = model.generate_content(prompt)
        await message.channel.send(response.text)
    except:
        pass

client.run(DISCORD_TOKEN)
