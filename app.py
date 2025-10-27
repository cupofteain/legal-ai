# app.py
import os
import json
from datetime import datetime
from openai import OpenAI
import gradio as gr

# --- Настройка OpenAI client ---
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Локальная FAQ база (опционально) ---
FAQ_DB = {}
FAQ_FOLDER = "faq_db"
if os.path.isdir(FAQ_FOLDER):
    for fn in os.listdir(FAQ_FOLDER):
        if fn.endswith(".txt"):
            try:
                with open(os.path.join(FAQ_FOLDER, fn), "r", encoding="utf-8") as f:
                    for line in f:
                        if ":" in line:
                            q, a = line.strip().split(":", 1)
                            FAQ_DB[q.strip().lower()] = a.strip()
            except Exception:
                pass

# --- Системный промпт: юридический ассистент ---
SYSTEM_PROMPT = (
    "Ты — AI юридический ассистент, специализирующийся на правах граждан и вопросах военной службы "
    "в Казахстане. Отвечай ясно, уважительно и по существу. "
    "Если вопрос требует конкретной юридической консультации, укажи, что это общая информация и порекомендуй обратиться к юристу."
)

# --- Утилиты ---
def append_history(history, user_text, bot_text):
    history = history or []
    history.append((user_text, bot_text))
    return history

def save_transcript(history):
    filename = f"transcript_{datetime.utcnow().strftime('%Y%m%dT%H%M%SZ')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"created_at": datetime.utcnow().isoformat(), "history": history}, f, ensure_ascii=False, indent=2)

def find_faq_answer(query):
    q = query.strip().lower()
    if q in FAQ_DB:
        return FAQ_DB[q]
    for k, v in FAQ_DB.items():
        if k in q or q in k:
            return v
    return None

# --- Вызов OpenAI ---
def ask_openai_chat(messages, model="gpt-4o-mini", max_tokens=512, temperature=0.25):
    resp = client.chat.completions.create(
        model=model, messages=messages, max_tokens=max_tokens, temperature=temperature
    )
    try:
        return resp.choices[0].message.content
    except Exception:
        return str(resp)

# --- Основная функция обработки ---
def respond(user_message, history):
    history = history or []

    # Проверка FAQ
    faq_ans = find_faq_answer(user_message)
    if faq_ans:
        history = append_history(history, user_message, faq_ans)
        return history, history

    # Формируем контекст для OpenAI
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    max_context = 6
    for user_text, bot_text in history[-max_context:]:
        messages.append({"role": "user", "content": user_text})
        messages.append({"role": "assistant", "content": bot_text})
    messages.append({"role": "user", "content": user_message})

    try:
        answer = ask_openai_chat(messages)
    except Exception as e:
        answer = f"Ошибка при обращении к OpenAI: {e}"

    history = append_history(history, user_message, answer)
    try:
        save_transcript(history)
    except Exception:
        pass

    return history, history

# --- Интерфейс Gradio ---
with gr.Blocks(css=".gradio-container { max-width: 900px; margin: auto; }") as demo:
    gr.Markdown("## ⚖️ AI Legal Chatbot — юридическая поддержка по вопросам армии и прав граждан")
    chat = gr.Chatbot(label="Чат")
    state = gr.State([])
    txt = gr.Textbox(placeholder="Задай вопрос...", show_label=False)
    submit = gr.Button("Отправить")

    def _submit(message, history_state):
        history, _ = respond(message, history_state)
        return history, ""

    submit.click(_submit, [txt, state], [chat, txt])
    txt.submit(_submit, [txt, state], [chat, txt])
    clear = gr.Button("Очистить")
    clear.click(lambda: ([], ""), None, [chat, txt])

# --- Локальный запуск без логина ---
if __name__ == "__main__":
    demo.launch(share=False, auth=None)
