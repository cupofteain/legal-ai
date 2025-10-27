# ⚖️ AI Legal Chatbot — Free Legal Support for Every Citizen

### 💡 Empowering people through accessible legal guidance

Millions of people face unfair treatment or simply cannot afford a lawyer when they need help the most.  
**AI Legal Chatbot** was built to change that — offering **free, AI-driven legal assistance** focused on **civil rights and military service issues in Kazakhstan** 🇰🇿.

---

## 🧭 Mission

> To make legal information accessible to everyone — regardless of income, status, or location.

This project bridges the gap between citizens and legal knowledge.  
By combining **AI technology** with **ethical design**, it helps people better understand their rights and make informed decisions.

---

## 🧠 What It Does

- 💬 Provides clear answers to basic legal questions in real time  
- 📚 Uses a local FAQ database for fast, offline responses  
- 🤖 Leverages OpenAI models for more complex, context-aware reasoning  
- 🛡️ Prioritizes user safety — never stores private data or personal identifiers  
- 💾 Saves anonymized conversation history for research and improvement  

---

## 🧩 Tech Overview

| Component | Purpose |
|------------|----------|
| **Python** | Core programming language |
| **Gradio** | Clean and intuitive chat interface |
| **OpenAI API** | Language understanding and reasoning |
| **Local JSON DB** | Stores chat transcripts securely |
| **FAQ Engine** | Predefined legal Q&A for offline access |

---

## 💻 How It Works

Users can ask questions about:
- Rights of conscripts and military deferments  
- Employment law and workplace rights  
- Civil and administrative issues  

The chatbot first checks a **local FAQ** for relevant answers.  
If none are found, it securely queries **OpenAI’s API** to provide an accurate, human-like response — always with a disclaimer that it is **informational, not legal advice**.

---

## 🧪 Example Interaction

> **User:** What are my rights if I’m called to military service while studying?  
>
> **AI Legal Chatbot:**  
> According to the Law on Military Duty and Service of the Republic of Kazakhstan, full-time students are eligible for a temporary deferment. This response is for general information — for official guidance, please contact your local enlistment office or legal advisor.

---

## 🛠️ Installation (for local testing)

```bash
git clone https://github.com/cupofteain/legal-ai.git
cd legal-ai
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key"
python app.py


An example chatbot using [Gradio](https://gradio.app), [`huggingface_hub`](https://huggingface.co/docs/huggingface_hub/v0.22.2/en/index), and the [Hugging Face Inference API](https://huggingface.co/docs/api-inference/index).
