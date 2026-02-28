# 🐾 Musya AI / Муся ИИ

## [RU] Инструкция пользователя

**Musya AI** — это консольный чат-бот для работы с Groq API.

### 🔑 Настройка API ключа (ВАЖНО)
Чтобы программа работала, ей нужен доступ к API. 
1. В папке со скриптом создайте папку `dbai`.
2. Внутри папки `dbai` создайте текстовый файл `key.txt`.
3. Зайдите на https://console.groq.com/keys (если не заходит зарегистрируйтесь потом зайдите в Api Keys), потом создайте API ключ
4. Вставьте ваш API ключ Groq в этот файл.

> **Примечание:** Если вы не создадите файл вручную, программа сама спросит ключ при первом запуске и создаст папку и файл за вас.

### 🚀 Запуск
1. Установите библиотеки: `pip install requests rich prompt_toolkit`
2. Запустите: `python musya_ai.py`

### 🐾 Команды
- `/help` — список всех команд.
- `/models` — принт нейросетей.
- `/model #` — выбрать нейросеть(посмотрите /models)
- `/clear` — очистка памяти чата.
# Тестировано на арч линуксе

---

## [EN] User Manual

**Musya AI** is a CLI chat client for Groq API.

### 🔑 API Key Setup (IMPORTANT)
The application requires an API key to function.
1. Create a folder named dbai in the same directory as the script.
2. Inside the dbai folder, create a text file named key.txt.
3. Go to https://console.groq.com/keys (sign up if you haven't already, then navigate to API Keys) and create a new API key.
4. Paste your Groq API key into the key.txt file.

> **Note:** If you don't do this manually, the app will prompt you for the key on the first run and create the necessary files automatically.

### 🚀 How to Run
1. Install dependencies: `pip install requests rich prompt_toolkit`
2. Run the script: `python musya_ai.py`

### 🐾 Commands
- `/help` — show all available commands.
- `/models` — show models.
- `/model #` — set model(see /models)
- `/clear` — clear chat memory
# Tested on Arch Linux!!
### Only russian, english soon

   - `/models` — switch between LLMs (Llama, Mixtral, etc.).
- `/clear` — clear chat context.
