import os
import keyboards as kb 
from request_gpt import ai_generator

from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command


from database import create_database, save_message, communication_style, clear_chat_history

from pydub import AudioSegment
import speech_recognition as sr

# Конвертер голосового в текст
r = sr.Recognizer()

router = Router()

# Обработчик команды /start
@router.message(CommandStart())
async def start(message: Message):
    create_database()
    text = f"""🙋‍♂️<b>Привет, {message.from_user.first_name}!</b>
        Я умный бот. Со мной можно поговорить на любые темы.
        <b>Доступные команды:</b>
        /start - Начать общение
        /help - Показать справку
        /reset - Сбросить контекст
        /about - Информация о боте
        /mode - Выборр стиля общения
        👀 Также можно отправить мне голосовое сообщение и получить его текстовую версию
        """

    await message.answer(text=text, parse_mode="html")


# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):

    await message.answer(text = "<a href = 'https://core.telegram.org/'>Тут какая то полезная информация</a>", parse_mode='html')


# Обработчик команды /reset
@router.message(Command("reset"))
async def reset_handler(message: Message):
    user_id = message.from_user.id
    clear_chat_history(user_id)
    await message.answer("✅ История диалога полностью очищена! <s>Теперь дядя майор ничего не узнает</s>", parse_mode='html')
 
    

# Обработчик команды /about
@router.message(Command("about"))
async def cmd_about(message: Message):
    about_text = """
<pre>О боте:
Версия: 1.0
Используется: OpenAI GPT-3.5-turbo
Разработчик:🤷‍♂️</pre> 
    """

    await message.answer(text = about_text, parse_mode='html')


# Обработчик команды /mode
@router.message(Command("mode"))
async def cmd_mode(message: Message):
    await message.answer('<b>Выберите стиль общения</b>', reply_markup=kb.mode_keyboards, parse_mode='html')

# Выбор стиля
@router.callback_query(F.data.in_(["friendly", "Business", "ironic"]))
async def mode(callback: CallbackQuery):
    user_id = callback.from_user.id
    style = callback.data

    style_names = {
        "friendly": "Дружеский",
        "Business": "Деловой",
        "ironic": "Ироничный"
    }

    # Сохраняем стиль 
    communication_style(user_id, style_names.get(style, 'Дружеский'))
    
    
    
    await callback.message.edit_text(
        f"✅ Стиль изменен на: {style_names.get(style, 'Дружеский')}"
    )
    await callback.answer()

# Оюраюотчик сообщений
@router.message(F.text)
async def handle_text(message: Message):
    await message.bot.send_chat_action(message.chat.id, 'typing')

    # Сохраняем текст пользователя в бд и швыряем его в нейронку
    save_message(message.from_user.id, message.text, is_user_message=True)
    response = await ai_generator(message.text, message.from_user.id)  
    # Сохраняем ответ железного
    save_message(message.from_user.id, response, is_user_message=False)

    await message.answer(response)




@router.message(F.voice)
async def converter_voice(message: Message):
    await message.answer('<b>Обрабатываю сообщение</b>', parse_mode='html')
    await message.bot.send_chat_action(message.chat.id, "record_audio")

    # Скачивание и конвертация голосового сообщения
    file_info = await message.bot.get_file(message.voice.file_id)
    temp_dir = "temp_voice"
    os.makedirs(temp_dir, exist_ok=True)
    ogg_path = os.path.join(temp_dir, f"{message.message_id}.ogg")
    wav_path = os.path.join(temp_dir, f"{message.message_id}.wav")

    await message.bot.download_file(file_info.file_path, ogg_path)
    sound = AudioSegment.from_ogg(ogg_path)

    sound.export(wav_path, format="wav")

    # Распознавание текста
    with sr.AudioFile(wav_path) as source:
        audio = r.record(source)
        text = r.recognize_google(audio, language="ru-RU")
    await message.answer(text = f'<b>Текстовый вариант сообщения:</b>\n{text}', parse_mode='html')




