import requests
import os
import json
from rich.console import Console
from rich.table import Table
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.styles import Style as ptStyle

# Универсальное определение путей для Linux и Windows
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "dbai")
if not os.path.exists(DB_DIR): 
    os.makedirs(DB_DIR)

KEY_FILE = os.path.join(DB_DIR, "key.txt")
MODEL_FILE = os.path.join(DB_DIR, "last_model.txt")
PROMPTS_FILE = os.path.join(DB_DIR, "prompts.json")
HISTORY_FILE = os.path.join(DB_DIR, "chat_history.txt")

BASE_URL = "https://api.groq.com/openai/v1"
DEFAULT_PROMPT = "ты аристократичная кошка муся, пиши всегда с маленькой буквы."
LAVENDER = "bold #afafff"

console = Console()
chat_context = []
cached_models = []

def get_api_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            k = f.read().strip()
            if k: return k
    console.print("[yellow]ключ не найден в dbai/key.txt[/yellow]")
    k = input("введи API KEY: ").strip()
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
    table = Table(title="🐾 список команд", border_style=LAVENDER)
    table.add_column("команда", style="cyan")
    table.add_column("описание")
    table.add_row("/help", "показать это меню")
    table.add_row("/models", "показать все доступные модели Groq")
    table.add_row("/model <№>", "переключиться на модель по номеру")
    table.add_row("/prompt $LIST", "показать список всех личностей")
    table.add_row("/prompt set <№>", "выбрать личность по номеру")
    table.add_row("/clear", "полная очистка текущего чата")
    table.add_row("/clear <№>", "удалить последние N сообщений")
    table.add_row("/exit", "завершить работу")
    console.print(table)

def print_models(api_key):
    if not cached_models: fetch_models(api_key)
    table = Table(title="🐾 доступные модели", border_style="green")
    table.add_column("№", style="yellow")
    table.add_column("ID", style="dim")
    table.add_column("NAME", style="bold white")
    table.add_column("CONTEXT", style="blue")
    for i, m in enumerate(cached_models):
        table.add_row(str(i+1), m['id'], get_friendly_name(m['id']), str(m.get('context_window', '-')))
    console.print(table)

def chat():
    global chat_context
    data = load_data()
    api_key = get_api_key()
    fetch_models(api_key)
    
    current_model = open(MODEL_FILE, 'r').read().strip() if os.path.exists(MODEL_FILE) else "llama-3.3-70b-versatile"
    session = PromptSession(history=FileHistory(HISTORY_FILE))

    console.print(f"[bold]система запущена. папка данных: {DB_DIR}[/bold]\n")

    while True:
        try:
            f_name = get_friendly_name(current_model)
            user_input = session.prompt(f"Я ≫ ", style=ptStyle.from_dict({'': '#afafff'})).strip()
            if not user_input: continue

            if user_input.startswith('/'):
                parts = user_input.split()
                cmd = parts[0]
                if cmd == '/exit': break
                elif cmd == '/help': print_help()
                elif cmd == '/models': print_models(api_key)
                elif cmd == '/clear':
                    if len(parts) > 1 and parts[1].isdigit():
                        num = int(parts[1]) * 2
                        chat_context = chat_context[:-num] if num < len(chat_context) else []
                        console.print(f"удалено из памяти: {parts[1]} пар сообщений.")
                    else:
                        chat_context = []
                        os.system('cls' if os.name == 'nt' else 'clear')
                        console.print("память полностью очищена.")
                elif cmd == '/model' and len(parts) > 1:
                    try:
                        idx = int(parts[1]) - 1
                        current_model = cached_models[idx]['id']
                        with open(MODEL_FILE, 'w') as f: f.write(current_model)
                        console.print(f"активна модель: {get_friendly_name(current_model)}")
                    except: console.print("[red]ошибка: неверный номер модели[/red]")
                elif cmd == '/prompt' and len(parts) > 1:
                    if parts[1] == "$LIST":
                        t = Table(title="🐾 личности")
                        t.add_column("№"); t.add_column("текст")
                        for i, p in enumerate(data['list']): t.add_row(str(i+1), p[:100] + "...")
                        console.print(t)
                    elif parts[1] == "set" and len(parts) > 2:
                        try:
                            idx = int(parts[2]) - 1
                            data['current'] = data['list'][idx]
                            chat_context = []
                            save_data(data)
                            console.print(f"личность №{parts[2]} выбрана. контекст сброшен.")
                        except: pass
                continue

            messages = [{"role": "system", "content": data['current']}]
            messages.extend(chat_context)
            messages.append({"role": "user", "content": user_input})
            
            with console.status(f"[italic]генерация ({f_name})...[/]"):
                r = requests.post(f"{BASE_URL}/chat/completions", 
                                 headers={"Authorization": f"Bearer {api_key}"}, 
                                 json={"model": current_model, "messages": messages})
                res = r.json()
                if 'choices' in res:
                    ans = res['choices'][0]['message']['content']
                    chat_context.extend([{"role": "user", "content": user_input}, {"role": "assistant", "content": ans}])
                    console.print(f"\n[bold #afafff]{f_name} ≫[/bold #afafff] {ans}\n")
                else:
                    console.print(f"[red]ошибка API: {res.get('error', {}).get('message', 'error')}[/red]")
        except KeyboardInterrupt: break
        except Exception as e: console.print(f"критическая ошибка: {e}")

if __name__ == "__main__":
    chat()
