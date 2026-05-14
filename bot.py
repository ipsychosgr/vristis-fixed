import discord
import google.generativeai as genai
import random
import os

# Μεταβλητές Railway
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Ρύθμιση Gemini - ΕΔΩ ΕΙΝΑΙ Η ΑΛΛΑΓΗ
genai.configure(api_key=GEMINI_API_KEY)

# Ορίζουμε το μοντέλο με την πλήρη διαδρομή και χωρίς beta
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
    
    print(f"Είδα μήνυμα από {message.author}: {message.content}")

    # Επιλέγουμε το μοντέλο μέσα στην on_message για να είμαστε σίγουροι
    model = genai.GenerativeModel('gemini-1.5-flash')

    pool = random.sample(vrisies, 4)
    prompt = f"Είσαι ένας αγροίκος και εριστικός τύπος από το χωριό. Απάντα σύντομα και εριστικά σε αυτό: '{message.content}'. Χρησιμοποίησε οπωσδήποτε μερικές από αυτές τις λέξεις: {', '.join(pool)}. Μην χρησιμοποιείς bold."

    try:
        # Αναγκάζουμε το αίτημα να πάει στην έκδοση v1
        response = model.generate_content(prompt)
        if response.text:
            await message.channel.send(response.text)
    except Exception as e:
        print(f"Σφάλμα στο Gemini: {e}")

client.run(DISCORD_TOKEN)
