import json
import pytest
from pathlib import Path
from unittest.mock import patch
import todo


@pytest.fixture(autouse=True)
def tmp_data_file(tmp_path, monkeypatch):
    data_file = tmp_path / "todos.json"
    monkeypatch.setattr(todo, "DATA_FILE", data_file)


def test_add_creates_todo():
    todo.add("Buy milk")
    todos = todo.load()
    assert len(todos) == 1
    assert todos[0]["text"] == "Buy milk"
    assert todos[0]["done"] is False
    assert todos[0]["due"] is None


def test_add_with_due_date(capsys):
    todo.add("Submit report", due="2026-06-25")
    todos = todo.load()
    assert todos[0]["due"] == "2026-06-25"
    assert "due 2026-06-25" in capsys.readouterr().out


def test_list_shows_due_date(capsys):
    todo.add("Submit report", due="2026-06-25")
    todo.list_todos()
    assert "due 2026-06-25" in capsys.readouterr().out


def test_list_no_due_date(capsys):
    todo.add("No deadline")
    todo.list_todos()
    assert "due" not in capsys.readouterr().out


def test_list_empty(capsys):
    todo.list_todos()
    assert "No todos yet." in capsys.readouterr().out


def test_list_shows_todos(capsys):
    todo.add("Task one")
    todo.list_todos()
    assert "Task one" in capsys.readouterr().out


def test_done_marks_todo(capsys):
    todo.add("Finish report")
    todo.done(1)
    assert todo.load()[0]["done"] is True


def test_done_invalid_index(capsys):
    todo.done(99)
    assert "No todo at index" in capsys.readouterr().out


def test_remove_deletes_todo():
    todo.add("Delete me")
    todo.remove(1)
    assert todo.load() == []


def test_remove_invalid_index(capsys):
    todo.remove(99)
    assert "No todo at index" in capsys.readouterr().out


def test_clear_removes_all(capsys):
    todo.add("One")
    todo.add("Two")
    todo.clear()
    assert todo.load() == []
    assert "All todos cleared." in capsys.readouterr().out


def test_add_with_priority(capsys):
    todo.add("Fix bug", priority="high")
    todos = todo.load()
    assert todos[0]["priority"] == "high"
    assert "[high]" in capsys.readouterr().out


def test_add_invalid_priority(capsys):
    todo.add("Fix bug", priority="urgent")
    assert todo.load() == []
    assert "Invalid priority" in capsys.readouterr().out


def test_list_sorted_by_priority(capsys):
    todo.add("Low task", priority="low")
    todo.add("High task", priority="high")
    todo.add("Normal task")
    capsys.readouterr()  # discard add() output
    todo.list_todos()
    output = capsys.readouterr().out
    high_pos = output.index("High task")
    normal_pos = output.index("Normal task")
    low_pos = output.index("Low task")
    assert high_pos < normal_pos < low_pos


def test_list_shows_priority_marker(capsys):
    todo.add("Urgent", priority="high")
    todo.list_todos()
    assert "[!]" in capsys.readouterr().out
