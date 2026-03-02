import requests
import os
import json
from rich.console import Console
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style as ptStyle

# Универсальное определение путей
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "dbai")
if not os.path.exists(DB_DIR): 
    os.makedirs(DB_DIR)

KEY_FILE = os.path.join(DB_DIR, "key.txt")
MODEL_FILE = os.path.join(DB_DIR, "last_model.txt")
PROMPTS_FILE = os.path.join(DB_DIR, "prompts.json")
HISTORY_FILE = os.path.join(DB_DIR, "chat_history.txt")
LANG_FILE = os.path.join(DB_DIR, "lang.txt")

BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_PROMPT = "You are a helper of a person you are talking with ; Please don't use: bold text, cursive, spreadsheets, etc."
LAVENDER = "bold #afafff"

console = Console()
chat_context = []
cached_models = []

# Локализация
LOCALES = {
    "ru": {
        "help_title": "🐾 список команд",
        "models_title": "🐾 доступные модели",
        "prompts_title": "🐾 личности",
        "key_not_found": "[yellow]ключ не найден в dbai/key.txt[/yellow]",
        "enter_key": "введи API KEY: ",
        "sys_start": "[bold]система запущена. папка данных: {dir}[/bold]\n",
        "cleared": "память полностью очищена.",
        "cleared_num": "удалено из памяти: {n} пар сообщений.",
        "model_active": "активна модель: {name}",
        "prompt_set": "личность №{n} выбрана. контекст сброшен.",
        "err_model": "[red]ошибка: неверный номер модели[/red]",
        "gen": "генерация",
        "lang_set": "язык изменен на русский",
        "help_rows": [
            ("/help", "показать это меню"),
            ("/models", "показать все доступные модели Groq"),
            ("/model <№>", "переключиться на модель по номеру"),
            ("/prompt ", "показать список всех личностей"),
            ("/prompt set <№>", "выбрать личность по номеру"),
            ("/lang <ru|en>", "сменить язык интерфейса"),
            ("/clear", "полная очистка текущего чата"),
            ("/clear <№>", "удалить последние N сообщений"),
            ("/exit", "завершить работу")
        ]
    },
    "en": {
        "help_title": "🐾 command list",
        "models_title": "🐾 available models",
        "prompts_title": "🐾 personalities",
        "key_not_found": "[yellow]key not found in dbai/key.txt[/yellow]",
        "enter_key": "enter API KEY: ",
        "sys_start": "[bold]system started. data folder: {dir}[/bold]\n",
        "cleared": "memory fully cleared.",
        "cleared_num": "removed from memory: {n} message pairs.",
        "model_active": "active model: {name}",
        "prompt_set": "personality #{n} selected. context reset.",
        "err_model": "[red]error: invalid model number[/red]",
        "gen": "generating",
        "lang_set": "language changed to english",
        "help_rows": [
            ("/help", "show this menu"),
            ("/models", "show all available Groq models"),
            ("/model <#>", "switch model by number"),
            ("/prompt ", "show all personalities"),
            ("/prompt set <#>", "select personality by number"),
            ("/lang <ru|en>", "change interface language"),
            ("/clear", "full chat clear"),
            ("/clear <#>", "delete last N messages"),
            ("/exit", "exit the app")
        ]
    }
}

current_lang = "ru"
if os.path.exists(LANG_FILE):
    with open(LANG_FILE, 'r') as f:
        saved_lang = f.read().strip()
        if saved_lang in LOCALES: current_lang = saved_lang

def get_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            k = f.read().strip()
            if k: return k
    console.print(LOCALES[current_lang]["key_not_found"])
    k = input(LOCALES[current_lang]["enter_key"]).strip()
    with open(KEY_FILE, 'w') as f: f.write(k)
    return k

def load_data():
    if not os.path.exists(PROMPTS_FILE):
        d = {"current": DEFAULT_PROMPT, "list": [DEFAULT_PROMPT]}
        with open(PROMPTS_FILE, 'w') as f: json.dump(d, f, ensure_ascii=False)
        return d
    with open(PROMPTS_FILE, 'r') as f: return json.load(f)

def save_data(data):
    with open(PROMPTS_FILE, 'w') as f: json.dump(data, f, ensure_ascii=False, indent=2)

def fetch_models(api_key):
    global cached_models
    try:
        r = requests.get(f"{BASE_URL}/models", headers={"Authorization": f"Bearer {api_key}"})
        if r.status_code == 200:
            cached_models = sorted(r.json().get('data', []), key=lambda x: x['id'])
            return True
    except: pass
    return False

def get_friendly_name(model_id):
    return model_id.split('/')[-1].replace('-', ' ').capitalize()

def print_help():
    lang = LOCALES[current_lang]
    table = Table(title=lang["help_title"], border_style=LAVENDER)
    table.add_column("command", style="cyan")
    table.add_column("description")
    for row in lang["help_rows"]:
        table.add_row(*row)
    console.print(table)

def print_models(api_key):
    if not cached_models: fetch_models(api_key)
    table = Table(title=LOCALES[current_lang]["models_title"], border_style="green")
    table.add_column("№", style="yellow")
    table.add_column("ID", style="dim")
    table.add_column("NAME", style="bold white")
    table.add_column("CONTEXT", style="blue")
    for i, m in enumerate(cached_models):
        table.add_row(str(i+1), m['id'], get_friendly_name(m['id']), str(m.get('context_window', '-')))
    console.print(table)

def chat():
    global chat_context, current_lang
    data = load_data()
    api_key = get_api_key()
    fetch_models(api_key)
    
    current_model = open(MODEL_FILE, 'r').read().strip() if os.path.exists(MODEL_FILE) else "llama-3.3-70b-versatile"
    session = PromptSession(history=FileHistory(HISTORY_FILE))

    console.print(LOCALES[current_lang]["sys_start"].format(dir=DB_DIR))

    while True:
        try:
            lang = LOCALES[current_lang]
            f_name = get_friendly_name(current_model)
            user_input = session.prompt(f"Я ≫ ", style=ptStyle.from_dict({'': '#afafff'})).strip()
            if not user_input: continue

            if user_input.startswith('/'):
                parts = user_input.split()
                cmd = parts[0]
                if cmd == '/exit': break
                elif cmd == '/help': print_help()
                elif cmd == '/models': print_models(api_key)
                elif cmd == '/lang' and len(parts) > 1:
                    new_lang = parts[1].lower()
                    if new_lang in LOCALES:
                        current_lang = new_lang
                        with open(LANG_FILE, 'w') as f: f.write(current_lang)
                        console.print(LOCALES[current_lang]["lang_set"])
                elif cmd == '/clear':
                    if len(parts) > 1 and parts[1].isdigit():
                        num = int(parts[1]) * 2
                        chat_context = chat_context[:-num] if num < len(chat_context) else []
                        console.print(lang["cleared_num"].format(n=parts[1]))
                    else:
                        chat_context = []
                        os.system('cls' if os.name == 'nt' else 'clear')
                        console.print(lang["cleared"])
                elif cmd == '/model' and len(parts) > 1:
                    try:
                        idx = int(parts[1]) - 1
                        current_model = cached_models[idx]['id']
                        with open(MODEL_FILE, 'w') as f: f.write(current_model)
                        console.print(lang["model_active"].format(name=get_friendly_name(current_model)))
                    except: console.print(lang["err_model"])
                elif cmd == '/prompt' and len(parts) > 1:
                    if parts[1] == "":
                        t = Table(title=lang["prompts_title"])
                        t.add_column("№"); t.add_column("text")
                        for i, p in enumerate(data['list']): t.add_row(str(i+1), p[:100] + "...")
                        console.print(t)
                    elif parts[1] == "set" and len(parts) > 2:
                        try:
                            idx = int(parts[2]) - 1
                            data['current'] = data['list'][idx]
                            chat_context = []
                            save_data(data)
                            console.print(lang["prompt_set"].format(n=parts[2]))
                        except: pass
                continue

            messages = [{"role": "system", "content": data['current']}]
            messages.extend(chat_context)
            messages.append({"role": "user", "content": user_input})
            
            with console.status(f"[italic]{lang['gen']} ({f_name})...[/]"):
                r = requests.post(f"{BASE_URL}/chat/completions", 
                                 headers={"Authorization": f"Bearer {api_key}"}, 
                                 json={"model": current_model, "messages": messages})
                res = r.json()
                if 'choices' in res:
                    ans = res['choices'][0]['message']['content']
                    chat_context.extend([{"role": "user", "content": user_input}, {"role": "assistant", "content": ans}])
                    console.print(f"\n[bold #afafff]{f_name} ≫[/bold #afafff] {ans}\n")
                else:
                    console.print(f"[red]API Error: {res.get('error', {}).get('message', 'error')}[/red]")
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"Error: {e}")

if __name__ == "__main__":
    chat()
