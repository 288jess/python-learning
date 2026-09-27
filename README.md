# Python Learning — Three Hands-on Projects

This repo is the hands-on part of a three-week Python learning path.
Each week turns a checklist item into a real, runnable program.

## Project Structure

```
python-learning/
├── pyproject.toml          # Project config: name, deps, pytest settings
├── data/
│   └── sample.txt          # Sample text for the wordcount demo
├── w1_wordcount/           # Week 1: read a file, count lines & word frequency
│   └── counter.py          #   CLI: python -m w1_wordcount.counter data/sample.txt
├── w2_library/             # Week 2: OOP — Book / Library, custom exceptions,
│   ├── library.py          #   type hints, inheritance & polymorphism
│   └── tests/
│       └── test_library.py #   pytest smoke tests (fixture, raises)
└── w3_todo/                # Week 3: command-line todo app
    ├── todo.py             #   Core: add / list / done / delete + JSON storage
    ├── cli.py              #   CLI entry: python -m w3_todo.cli ...
    └── tests/
        └── test_todo.py    #   pytest covering core functions (tmp_path, parametrize)
```

## How to Run

```bash
# Week 1 — wordcount
python -m w1_wordcount.counter data/sample.txt --top 5

# Week 2 — tests only
python -m pytest w2_library/tests

# Week 3 — todo app
python -m w3_todo.cli add "buy milk"
python -m w3_todo.cli list
python -m w3_todo.cli done 1
python -m w3_todo.cli delete 1
```

Environment variables (optional): `TODO_STORE`, `TODO_LOG_LEVEL`, `TODO_LOG_FILE`.

## Why It Is Built This Way

- **`with` statements** guarantee files are closed even when an error is raised.
- **Type hints** act as documentation and let the IDE catch mistakes early.
- **Custom exceptions** turn confusing errors into meaningful messages.
- **JSON storage** keeps data after the program exits.
- **logging** records what the program did, with timestamps, for debugging later.
- **pytest** protects you from breaking code you wrote days ago.

## Tests

```bash
python -m pytest        # runs w2_library/tests and w3_todo/tests, expects all green
```
