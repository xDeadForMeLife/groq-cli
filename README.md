# 🐾 Groq CLI

## [RU] Инструкция пользователя

**Groq CLI** — это продвинутый консольный чат-клиент для работы с моделями Groq API.

### 🔑 Настройка API ключа (ВАЖНО)
Чтобы программа работала, ей нужен доступ к API. 
1. В папке со скриптом создайте папку `dbai`.
2. Внутри папки `dbai` создайте текстовый файл `key.txt`.
3. Зайдите на [console.groq.com/keys](https://console.groq.com/keys), создайте ключ и вставьте его в этот файл.

> **Примечание:** Если вы не создадите файл вручную, программа сама спросит ключ при первом запуске и создаст нужные файлы за вас.

### 🚀 Запуск
1. Установите библиотеки: `pip install requests rich prompt_toolkit`
2. Запустите: `python groq-cli.py`

### 🐾 Команды
- `/help` — показать список всех команд.
- `/models` — выбор нейросети (Llama, Mixtral и др.).
- `/lang <ru|en>` — смена языка интерфейса.
- `/clear` — очистка памяти чата.
- `/exit` — выход.

---

## [EN] User Manual

**Groq CLI** is a powerful terminal-based chat client for Groq API.

### 🔑 API Key Setup (IMPORTANT)
The application requires an API key to function.
1. Create a folder named `dbai` in the project directory.
2. Inside `dbai`, create a file named `key.txt`.
3. Go to [console.groq.com/keys](https://console.groq.com/keys), generate a key, and paste it into this file.

> **Note:** If the file is missing, the app will prompt you for the key on the first run and create the necessary files automatically.

### 🚀 How to Run
1. Install dependencies: `pip install requests rich prompt_toolkit`
2. Run the script: `python groq-cli.py`

### 🐾 Commands
- `/help` — show all available commands.
- `/models` — switch between LLMs (Llama, Mixtral, etc.).
- `/lang <ru|en>` — switch interface language.
- `/clear` — clear chat context.
- `/exit` — exit application.
