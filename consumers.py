import json
from channels.generic.websocket import AsyncWebsocketConsumer
from google import genai
from google.genai import types

# Gemini Client Initialize karein (Apni API key yahan dalein)
client = genai.Client(api_key="AIzaSyAd7WnJiXQHrdwAhtjWARnzwn9ICc41Wa8")

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ OpenAI/Gemini AI Bot Connected!")
        
        # Bot welcome message
        await self.send(text_data=json.dumps({
            'message': "🤖 AI Bot: Assalam-o-Alaikum! I am your AI assisstant . what's on your mind today"
        }))

    async def disconnect(self, close_code):
        print("❌ AI Bot Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get('message', '')

        # 1. Pehle user ka message screen par show karein
        await self.send(text_data=json.dumps({
            'message': f"👤 Aap: {user_message}"
        }))

        try:
            # 2. AI ko system instruction dena taake wo short aur chat-friendly jawab de
            config = types.GenerateContentConfig(
                system_instruction="You are a helpful, witty, and friendly AI chat assistant. Respond in Roman Urdu mixed with English (Hinglish), keeping answers concise and natural for a chat app.",
                temperature=0.7,
            )

            # 3. Gemini API se Real-time Jawab mangwāna (Hum modern gemini-2.5-flash use kar rahe hain)
            response = client.models.generate_content(
                model='gemini-2.5-flash',
                contents=user_message,
                config=config,
            )
            
            ai_reply = f"🤖 AI: {response.text}"

        except Exception as e:
            print(f"Error calling AI API: {e}")
            ai_reply = "🤖 AI: Sorry bhai, lagta hai API key sahi nahi hai ya internet ka masla hai."

        # 4. AI ka generated jawab frontend ko bhejien
        await self.send(text_data=json.dumps({
            'message': ai_reply
        }))
        print("📤 AI response sent to frontend")