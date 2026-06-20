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


PRIORITIES = {"high": 0, "medium": 1, "low": 2}
PRIORITY_MARKER = {"high": "!", "medium": "~", "low": " "}


def add(text, due=None, priority=None):
    if priority and priority not in PRIORITIES:
        print(f"Invalid priority '{priority}'. Choose: high, medium, low.")
        return
    todos = load()
    todos.append({"text": text, "done": False, "due": due, "priority": priority})
    save(todos)
    msg = f"Added: {text}"
    if priority:
        msg += f" [{priority}]"
    if due:
        msg += f" (due {due})"
    print(msg)


def list_todos():
    todos = load()
    if not todos:
        print("No todos yet.")
        return
    ranked = sorted(
        enumerate(todos, 1),
        key=lambda x: PRIORITIES.get(x[1].get("priority"), 1),
    )
    for i, todo in ranked:
        status = "x" if todo["done"] else PRIORITY_MARKER.get(todo.get("priority"), " ")
        due = f" (due {todo['due']})" if todo.get("due") else ""
        priority = f" [{todo['priority']}]" if todo.get("priority") else ""
        print(f"[{status}] {i}. {todo['text']}{priority}{due}")


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


def clear():
    save([])
    print("All todos cleared.")


COMMANDS = {"add": add, "list": list_todos, "done": done, "remove": remove, "clear": clear}


def main():
    args = sys.argv[1:]
    if not args or args[0] not in COMMANDS:
        print("Usage: python todo.py <add|list|done|remove> [args]")
        sys.exit(1)

    cmd = args[0]
    if cmd in ("list", "clear"):
        COMMANDS[cmd]()
    elif cmd in ("done", "remove"):
        if len(args) < 2:
            print(f"Usage: python todo.py {cmd} <index>")
            sys.exit(1)
        COMMANDS[cmd](int(args[1]))
    elif cmd == "add":
        if len(args) < 2:
            print("Usage: python todo.py add <text> [--due YYYY-MM-DD]")
            sys.exit(1)
        due = None
        priority = None
        rest = args[1:]
        for flag in ("--due", "--priority"):
            if flag in rest:
                idx = rest.index(flag)
                if idx + 1 >= len(rest):
                    print(f"Usage: python todo.py add <text> [--due YYYY-MM-DD] [--priority high|medium|low]")
                    sys.exit(1)
                if flag == "--due":
                    due = rest[idx + 1]
                else:
                    priority = rest[idx + 1]
                rest = rest[:idx] + rest[idx + 2:]
        add(" ".join(rest), due=due, priority=priority)


if __name__ == "__main__":
    main()
