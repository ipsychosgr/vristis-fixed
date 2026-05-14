import discord
import requests
import random
import os
import json

# Φόρτωση ρυθμίσεων από το Railway
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Η λίστα με τα "γαλλικά" του Αντώνη
vrisies = ["ΠΑΛΙΟΤΑΓΑΡΙ", "ΜΠΑΣΤΟΥΝΟΒΛΑΧΕ", "ΤΣΟΠΑΝΗ", "ΓΙΔΟΒΟΣΚΕ", "ΤΣΟΓΛΑΝΙ", "ΤΕΝΕΚΕ ΞΕΓΑΝΩΤΕ", "ΚΑΤΣΑΠΛΙΑ", "ΜΠΟΥΧΕΣΑ", "ΖΑΓΑΡΙ", "ΒΛΑΧΟΔΗΜΑΡΧΕ", "ΣΦΟΥΓΓΑΡΟΚΩΛΑΡΙΕ", "ΚΟΥΡΑΔΟΚΟΦΤΗ", "ΛΙΝΑΤΣΑ", "ΧΑΪΒΑΝΙ", "ΞΥΛΟΓΙΑΝΝΗ", "ΠΑΡΤΑΛΙ", "ΛΕΧΡΙΤΗ", "ΜΠΑΤΑΛΗ", "ΚΟΠΡΟσκυλο", "ΣΤΟΥΡΝΑΡΙ", "ΧΑΧΟΛΟ", "ΚΑΡΑΓΚΙΟΖΗ", "ΜΠΕΧΛΙΒΑΝΗ", "ΤΣΑΠΑΤΣΟΥΛΗ"]

# Ρύθμιση Intents για να μπορεί να διαβάζει μηνύματα
intents = discord.Intents.default()
intents.message_content = True 
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Ο {client.user} είναι έτοιμος για δράση!')

@client.event
async def on_message(message):
    # Το bot δεν πρέπει να απαντάει στον εαυτό του
    if message.author == client.user:
        return
    
    # Log στο Railway για να ξέρουμε ότι έλαβε το μήνυμα
    print(f"Είδα μήνυμα από {message.author}: {message.content}")

    # Τυχαία επιλογή βρισιών για το prompt
    pool = random.sample(vrisies, 4)
    prompt = f"Είσαι ένας αγροίκος και εριστικός τύπος από το χωριό. Απάντα σύντομα και εριστικά σε αυτό: '{message.content}'. Χρησιμοποίησε οπωσδήποτε μερικές από αυτές τις λέξεις: {', '.join(pool)}. Μην χρησιμοποιείς bold."

    # Απευθείας κλήση στο Google API (v1beta)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        
        # Έλεγχος αν η Google έστειλε έγκυρη απάντηση
        if 'candidates' in result and len(result['candidates']) > 0:
            bot_response = result['candidates'][0]['content']['parts'][0]['text']
            await message.channel.send(bot_response)
        else:
            # Αν δεις αυτό στα logs, φταίει το API Key ή το Project ID
            print(f"API Error Response: {json.dumps(result)}")
    except Exception as e:
        print(f"Γενικό σφάλμα: {e}")

client.run(DISCORD_TOKEN)
