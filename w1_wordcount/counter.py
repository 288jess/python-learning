"""W1 动手任务：读取文本文件，统计行数与词频的命令行脚本。

用法：
    python -m w1_wordcount.counter <文件路径> [--top N]
"""

import re
import sys
from collections import Counter


def read_text(path: str) -> str:
    """读取整个文件（with 保证无论是否报错都自动关闭）。"""
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def count_lines(text: str) -> int:
    """按换行符切分统计行数。"""
    return len(text.splitlines())


def count_words(text: str) -> Counter:
    """切词并统计词频：统一转小写，只保留字母数字。"""
    words = re.findall(r"[a-zA-Z0-9]+", text.lower())
    return Counter(words)


def main(argv: list[str] | None = None) -> int:
    """命令行入口。返回 0 表示成功，1 表示用法错误。"""
    argv = sys.argv[1:] if argv is None else argv
    if not argv:
        print("用法: python -m w1_wordcount.counter <文件路径> [--top N]", file=sys.stderr)
        return 1

    path = argv[0]
    top = 10
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])

    text = read_text(path)
    print(f"行数: {count_lines(text)}")
    for word, freq in count_words(text).most_common(top):
        print(f"  {word}: {freq}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
