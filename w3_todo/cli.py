"""W3 命令行入口：todo 增/删/查/完成。

用法：
    python -m w3_todo.cli add "买牛奶"
    python -m w3_todo.cli list
    python -m w3_todo.cli done 1
    python -m w3_todo.cli delete 1

配置（环境变量，可用 .env + pydantic-settings 进一步管理）：
    TODO_STORE     存储文件路径，默认 todo.json
    TODO_LOG_LEVEL 日志级别，默认 INFO
    TODO_LOG_FILE  日志文件路径，默认输出到屏幕
"""

from __future__ import annotations

import argparse
import logging
import os
import sys

from w3_todo.todo import TodoApp


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="命令行 todo 小程序")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("add").add_argument("title", help="任务内容")
    sub.add_parser("list")
    done = sub.add_parser("done")
    done.add_argument("index", type=int, help="任务编号（从 1 开始）")
    delete = sub.add_parser("delete")
    delete.add_argument("index", type=int, help="任务编号（从 1 开始）")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    # 把"会变的设置"从代码里抽到环境变量：换机器/换环境不用改代码
    storage = os.environ.get("TODO_STORE", "todo.json")
    logging.basicConfig(
        level=os.environ.get("TODO_LOG_LEVEL", "INFO"),
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
        filename=os.environ.get("TODO_LOG_FILE"),   # 没设就打到屏幕
    )

    app = TodoApp(storage)

    if args.command == "add":
        app.add(args.title)
    elif args.command == "list":
        for i, task in enumerate(app.list_all(), start=1):
            print(f"{i}. {task}")
    elif args.command == "done":
        task = app.mark_done(args.index - 1)   # 用户数 1 开头，内部索引 0 开头
        print(f"已完成: {task.title}")
    elif args.command == "delete":
        task = app.delete(args.index - 1)
        print(f"已删除: {task.title}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
