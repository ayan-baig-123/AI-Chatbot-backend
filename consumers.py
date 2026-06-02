import json
import os
from channels.generic.websocket import AsyncWebsocketConsumer
# Stable aur guaranteed library use karein
import google.generativeai as genai

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        print("✅ Gemini AI Bot Connected!")
        
        # Bot welcome message
        await self.send(text_data=json.dumps({
            'message': "🤖 AI Bot: Assalam-o-Alaikum! I am your AI assistant. What's on your mind today?"
        }))

    async def disconnect(self, close_code):
        print("❌ AI Bot Disconnected")

    async def receive(self, text_data):
        data = json.loads(text_data)
        user_message = data.get('message', '')

        # 1. User ka message pehle screen par bhejein
        await self.send(text_data=json.dumps({
            'message': f"👤 Aap: {user_message}"
        }))

        try:
            # 🔥 STEP 1: Key ko directly environment se khichein
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                raise ValueError("Gemini key is not found on render!")

            # 🔥 STEP 2: Configure karein stable tarike se
            genai.configure(api_key=api_key)

            # 🔥 STEP 3: System Instruction set karein stable package ke mutabiq
            model = genai.GenerativeModel(
                model_name='models/gemini-1.5-flash',  # <--- Yahan 'models/' lagana zaroori hai
                system_instruction="You are a helpful, witty, and friendly AI chat assistant. Respond in Roman Urdu mixed with English (Hinglish), keeping answers concise and natural for a chat app."
            )

            # 🔥 STEP 4: Response generate karein
            # Isko safe chalane ke liye sync_to_async ki zaroorat nahi, direct response chalega
            response = model.generate_content(
                user_message,
                generation_config={"temperature": 0.7}
            )
            
            ai_reply = f"🤖 AI: {response.text}"

        except Exception as e:
            print(f"❌ Gemini Error: {e}")
            # Hum screen par asli error dikhayenge taake pata chale exact masla kya hai
            ai_reply = f"🤖 AI: Sorry bhai, backend par yeh error aaya hai: {str(e)}"

        # 4. AI ka generated jawab frontend ko bhejien
        await self.send(text_data=json.dumps({
            'message': ai_reply
        }))
        print("📤 AI response sent to frontend")
