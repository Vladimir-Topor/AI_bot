from openai import OpenAI
from dotenv import load_dotenv
from database import clear_chat_history
import os
import sqlite3
load_dotenv()


# Инициализация
client = OpenAI(
  base_url="https://openrouter.ai/api/v1",
  api_key = os.getenv("GPT_TOKEN"),
)


async def ai_generator(text: str, user_id: int = None):
    style_instruction = ""
    if user_id:
        conn = sqlite3.connect('chat_history.db')
        cursor = conn.cursor()
        
        # Получаем стиль общения 
        cursor.execute('SELECT communication_style FROM users WHERE user_id = ?', (user_id,))
        style_result = cursor.fetchone()
        
        # Получаем историю сообщений
        cursor.execute('''
        SELECT message_text, is_user_message 
        FROM messages 
        WHERE user_id = ? 
        ORDER BY timestamp DESC 
        LIMIT 10
        ''', (user_id,))
        history = cursor.fetchall()
        conn.close()
        
        # Руководство к общению
        if style_result:
            style = style_result[0]
            style_instructions = {
                "Дружеский": "Отвечай дружелюбно, желательно использовать эмодзи",
                "Деловой": "Отвечай в деловом, формальном стиле. Будь кратким и точным.",
                "Ироничный": "Отвечай с иронией и сарказмом. Используй шутки и подколки."
            }
            style_instruction = style_instructions.get(style, "")
        
        # Передаем контекст
        messages = []
        for msg, is_user in reversed(history):
            role = "user" if is_user else "assistant"
            messages.append({"role": role, "content": msg})
    else:
        messages = [{"role": "user", "content": text}]
    
    # Системное сообщение
    if style_instruction:
        messages.insert(0, {
            "role": "system",
            "content": f"Ты общаешься с пользователем. {style_instruction}"
        })


    # Запрос
    completion = client.chat.completions.create(
        model="openai/gpt-3.5-turbo-0613",
        messages=messages
    )
    return completion.choices[0].message.content
