# Установка библиотек (если ещё не установлены)
# pip install transformers torch gradio fuzzywuzzy python-Levenshtein

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import gradio as gr
from fuzzywuzzy import process

# 1. Загружаем предобученную модель DialoGPT-small
model_name = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# 2. Простейшая база знаний (FAQ) - ключ: вопрос, значение: ответ
faq_db = {
    "Как подать жалобу на работодателя?": "Вы можете обратиться в трудовую инспекцию или написать официальную жалобу работодателю.",
    "Могу ли я вернуть товар без чека?": "Да, при определенных условиях можно вернуть товар, даже если чек потерян, но потребуется доказательство покупки.",
    "Какие права у работника при увольнении?": "Работник имеет право на компенсацию за неиспользованный отпуск и соблюдение трудового договора."
}

# 3. Функция поиска ответа
def chatbot_response(user_input, chat_history=[]):
    # Сначала ищем совпадение в базе знаний (поиск по ключевым словам)
    best_match, score = process.extractOne(user_input, faq_db.keys())
    if score >= 60:  # если совпадение достаточно близкое
        response = faq_db[best_match]
    else:
        # Если совпадений нет, генерируем ответ через модель
        new_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        if chat_history:
            bot_input_ids = torch.cat([torch.tensor(chat_history, dtype=torch.long), new_input_ids], dim=-1)
        else:
            bot_input_ids = new_input_ids
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id)
        response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        # Обновляем историю модели
        chat_history.append(new_input_ids.tolist()[0])
        chat_history.append(tokenizer.encode(response + tokenizer.eos_token, return_tensors='pt').tolist()[0])

    return response, chat_history

# 4. Создаем интерфейс Gradio
with gr.Blocks() as demo:
    chat_history = []
    chatbot = gr.Chatbot()
    user_input = gr.Textbox(placeholder="Напиши вопрос...")
    submit_btn = gr.Button("Отправить")

    def respond(user_message):
        response, _ = chatbot_response(user_message, chat_history)
        return [(user_message, response)]

    submit_btn.click(respond, inputs=user_input, outputs=chatbot)

# 5. Запуск локально
demo.launch()
