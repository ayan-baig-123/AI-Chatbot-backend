import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Naya Google GenAI SDK import karein
from google import genai
from google.genai import types

# AI Response generate karne ke liye ek pure synchronous function banayein
def generate_ai_response(user_message, api_key):
    try:
        # Bilkul naya client initialize karein jo 2026 ke sabhi naye models ko support karta hai
        client = genai.Client(api_key=api_key)
        
        config = types.GenerateContentConfig(
            system_instruction="You are a helpful, witty, and friendly AI chat assistant. Respond in English but if user says to talk in other language so you talk in that language, keeping answers concise and natural for a chat app.",
            temperature=0.7,
        )
        
        # Naya aur tez tareen gemini-2.5-flash model
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_message,
            config=config,
        )
        return f"🤖 AI: {response.text}"
    except Exception as e:
        return f"❌ AI API Error: {str(e)}"

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ New Cyber Bot Connected!")
        
        await self.send(text_data=json.dumps({
            'message': "🤖 AI Bot: Assalam-o-Alaikum! I am your AI assistant. What's on your mind today?"
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

        # 2. Render ke dashboard se key uthein
        api_key = os.environ.get("GEMINI_API_KEY")
        
        if not api_key:
            ai_reply = "🤖 AI: Sorry bhai, Render dashboard par GEMINI_API_KEY nahi mili."
        else:
            try:
                # 🔥 Channels ke async tree mein sync function ko safely run karein
                ai_reply = await sync_to_async(generate_ai_response)(user_message, api_key)
            except Exception as e:
                ai_reply = f"🤖 AI: Sorry bhai, execution mein error aaya: {str(e)}"

        # 3. AI ka generated jawab frontend ko bhejien
        await self.send(text_data=json.dumps({
            'message': ai_reply
        }))
        print("📤 AI response sent to frontend")
