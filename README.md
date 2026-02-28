# 🐾 Musya AI / Муся ИИ

## [RU] Инструкция пользователя

**Musya AI** — это консольный чат-бот для работы с Groq API.

### 🔑 Настройка API ключа (ВАЖНО)
Чтобы программа работала, ей нужен доступ к API. 
1. В папке со скриптом создайте папку `dbai`.
2. Внутри папки `dbai` создайте текстовый файл `key.txt`.
3. Вставьте ваш API ключ Groq в этот файл.

> **Примечание:** Если вы не создадите файл вручную, программа сама спросит ключ при первом запуске и создаст папку и файл за вас.

### 🚀 Запуск
1. Установите библиотеки: `pip install requests rich prompt_toolkit`
2. Запустите: `python musya_ai.py`

### 🐾 Команды
- `/help` — список всех команд.
- `/models` — выбор нейросети (Llama, Mixtral и др.).
- `/clear` — очистка памяти чата.

---

## [EN] User Manual

**Musya AI** is a CLI chat client for Groq API.

### 🔑 API Key Setup (IMPORTANT)
The application requires an API key to function.
1. Create a folder named `dbai` in the project directory.
2. Inside `dbai`, create a file named `key.txt`.
3. Paste your Groq API key into this file.

> **Note:** If you don't do this manually, the app will prompt you for the key on the first run and create the necessary files automatically.

### 🚀 How to Run
1. Install dependencies: `pip install requests rich prompt_toolkit`
2. Run the script: `python musya_ai.py`

### 🐾 Commands
- `/help` — show all available commands.
- `/models` — switch between LLMs (Llama, Mixtral, etc.).
- `/clear` — clear chat context.
