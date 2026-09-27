"""W3 测试：覆盖核心函数（增删查、文件存储、重启恢复、参数化）。"""

import json

import pytest

from w3_todo.todo import Task, TodoApp


@pytest.fixture
def app(tmp_path) -> TodoApp:
    """tmp_path 是 pytest 内置 fixture：每个测试拿到一个临时目录，互不污染。"""
    return TodoApp(tmp_path / "todo.json")


def test_add_persists_to_file(app: TodoApp) -> None:
    app.add("写周报")
    saved = json.loads(app.storage_path.read_text(encoding="utf-8"))
    assert saved[0]["title"] == "写周报"


def test_reload_from_file(app: TodoApp) -> None:
    """模拟程序重启：数据要还在（文件存储的意义）。"""
    app.add("买牛奶")
    app2 = TodoApp(app.storage_path)
    assert [t.title for t in app2.list_all()] == ["买牛奶"]


def test_mark_done(app: TodoApp) -> None:
    app.add("学习 with 语句")
    task = app.mark_done(0)
    assert task.done is True


def test_delete(app: TodoApp) -> None:
    app.add("第一件事")
    app.add("第二件事")
    app.delete(0)
    assert len(app.list_all()) == 1
    assert app.list_all()[0].title == "第二件事"


@pytest.mark.parametrize("title", ["", "打卡", "学 Python 装饰器"])
def test_add_any_title(app: TodoApp, title: str) -> None:
    """一组参数跑多遍：参数化测试。"""
    app.add(title)
    assert app.list_all()[-1].title == title


def test_task_roundtrip() -> None:
    """Task 与字典互转：to_dict / from_dict 读写对称。"""
    task = Task("写 README", done=True)
    restored = Task.from_dict(task.to_dict())
    assert restored.title == task.title
    assert restored.done is True
