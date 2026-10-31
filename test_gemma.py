from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Charger la clé depuis le fichier .env
load_dotenv()

# 2. Créer le client (il lit GEMINI_API_KEY tout seul)
client = genai.Client()

CONSIGNE = "Tu es un assistant qui répond en français simple, en une phrase."

try:
    reponse = client.models.generate_content(
        model="gemma-4-26b-a4b-it",
        contents="Dis bonjour et explique en une phrase ce qu'est une arnaque par SMS.",
        config=types.GenerateContentConfig(system_instruction=CONSIGNE),
    )
    print("RÉPONSE DE GEMMA :")
    print(reponse.text)
except Exception as e:
    print("ERREUR :", e)
