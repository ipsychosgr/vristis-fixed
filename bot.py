import discord
import requests
import random
import os

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

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

    pool = random.sample(vrisies, 4)
    prompt = f"Είσαι ένας αγροίκος και εριστικός τύπος από το χωριό. Απάντα σύντομα και εριστικά σε αυτό: '{message.content}'. Χρησιμοποίησε οπωσδήποτε μερικές από αυτές τις λέξεις: {', '.join(pool)}. Μην χρησιμοποιείς bold."

    # Χρησιμοποιούμε το v1beta αλλά με το ΝΕΟ κλειδί
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(url, headers=headers, json=data)
        result = response.json()
        if 'candidates' in result:
            bot_response = result['candidates'][0]['content']['parts'][0]['text']
            await message.channel.send(bot_response)
        else:
            print(f"API Error: {result}")
    except Exception as e:
        print(f"Error: {e}")

client.run(DISCORD_TOKEN)
