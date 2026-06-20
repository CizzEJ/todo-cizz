import json
import sys
from pathlib import Path

DATA_FILE = Path(__file__).parent / "todos.json"


def load():
    if DATA_FILE.exists():
        return json.loads(DATA_FILE.read_text())
    return []


def save(todos):
    DATA_FILE.write_text(json.dumps(todos, indent=2))


def add(text):
    todos = load()
    todos.append({"text": text, "done": False})
    save(todos)
    print(f"Added: {text}")


def list_todos():
    todos = load()
    if not todos:
        print("No todos yet.")
        return
    for i, todo in enumerate(todos, 1):
        status = "x" if todo["done"] else " "
        print(f"[{status}] {i}. {todo['text']}")


def done(index):
    todos = load()
    if index < 1 or index > len(todos):
        print(f"No todo at index {index}.")
        return
    todos[index - 1]["done"] = True
    save(todos)
    print(f"Marked done: {todos[index - 1]['text']}")


def remove(index):
    todos = load()
    if index < 1 or index > len(todos):
        print(f"No todo at index {index}.")
        return
    removed = todos.pop(index - 1)
    save(todos)
    print(f"Removed: {removed['text']}")


COMMANDS = {"add": add, "list": list_todos, "done": done, "remove": remove}


def main():
    args = sys.argv[1:]
    if not args or args[0] not in COMMANDS:
        print("Usage: python todo.py <add|list|done|remove> [args]")
        sys.exit(1)

    cmd = args[0]
    if cmd == "list":
        list_todos()
    elif cmd in ("done", "remove"):
        if len(args) < 2:
            print(f"Usage: python todo.py {cmd} <index>")
            sys.exit(1)
        COMMANDS[cmd](int(args[1]))
    elif cmd == "add":
        if len(args) < 2:
            print("Usage: python todo.py add <text>")
            sys.exit(1)
        add(" ".join(args[1:]))


if __name__ == "__main__":
    main()
