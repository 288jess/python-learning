"""W3 动手任务：命令行 todo 的核心逻辑。

增删查 + JSON 文件存储（重启不丢）+ logging 记录操作。
"""

from __future__ import annotations

import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional

# 模块级 logger：每个文件用自己名字，日志里能看出是"谁"写的
logger = logging.getLogger(__name__)


class Task:
    """一条待办：标题 + 完成状态 + 创建时间。"""

    def __init__(self, title: str, done: bool = False, created_at: Optional[str] = None) -> None:
        self.title = title
        self.done = done
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")

    def to_dict(self) -> dict:
        """转成字典，方便 JSON 序列化。"""
        return {"title": self.title, "done": self.done, "created_at": self.created_at}

    @classmethod
    def from_dict(cls, data: dict) -> "Task":
        """从字典还原（配合 to_dict 使用，读写对称）。"""
        return cls(data["title"], data.get("done", False), data.get("created_at"))

    def __repr__(self) -> str:
        mark = "[x]" if self.done else "[ ]"
        return f"{mark} {self.title}（{self.created_at}）"


class TodoApp:
    """待办应用：所有操作都会 save 到磁盘，保证数据不丢。"""

    def __init__(self, storage_path: str | Path) -> None:
        self.storage_path = Path(storage_path)
        self._tasks: list[Task] = []
        self.load()

    # ---------- 存储 ----------

    def load(self) -> None:
        """启动时读盘；文件不存在说明是第一次用。"""
        if not self.storage_path.exists():
            self._tasks = []
            return
        with open(self.storage_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        self._tasks = [Task.from_dict(item) for item in data]
        logger.info("已从 %s 加载 %d 条任务", self.storage_path, len(self._tasks))

    def save(self) -> None:
        """任何修改后都落盘（with 保证写入异常也自动关文件）。"""
        with open(self.storage_path, "w", encoding="utf-8") as f:
            json.dump([t.to_dict() for t in self._tasks], f, ensure_ascii=False, indent=2)
        logger.info("已保存 %d 条任务到 %s", len(self._tasks), self.storage_path)

    # ---------- 增删查 ----------

    def add(self, title: str) -> Task:
        task = Task(title)
        self._tasks.append(task)
        self.save()
        logger.info("新增任务: %s", title)
        return task

    def list_all(self) -> list[Task]:
        return list(self._tasks)

    def mark_done(self, index: int) -> Task:
        task = self._tasks[index]
        task.done = True
        self.save()
        logger.info("完成任务: %s", task.title)
        return task

    def delete(self, index: int) -> Task:
        task = self._tasks.pop(index)
        self.save()
        logger.info("删除任务: %s", task.title)
        return task
