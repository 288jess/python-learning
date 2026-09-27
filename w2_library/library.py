"""W2 动手任务：用 OOP 设计 Book 与 Library，加自定义异常与类型提示。

覆盖知识点：class/__init__/self、继承与 super()、方法重写、多态、
封装约定（下划线前缀）、自定义异常类、类型提示（Optional/Callable）。
"""

from __future__ import annotations

from typing import Callable, Optional


class Book:
    """一本书：数据（title/author/isbn）+ 行为（describe）绑在一起。"""

    def __init__(self, title: str, author: str, isbn: str) -> None:
        self.title = title
        self.author = author
        self.isbn = isbn

    def describe(self) -> str:
        return f"《{self.title}》 by {self.author} (ISBN: {self.isbn})"


class DigitalBook(Book):
    """电子书：继承 Book，重写 describe 展示继承 + 多态。"""

    def __init__(self, title: str, author: str, isbn: str, file_format: str = "pdf") -> None:
        super().__init__(title, author, isbn)   # 调用父类初始化，不重复造轮子
        self.file_format = file_format

    def describe(self) -> str:
        base = super().describe()               # 复用父类描述
        return f"{base} [电子版: {self.file_format}]"


class LibraryError(Exception):
    """图书馆业务异常的基类（所有自定义异常的爸爸）。"""


class DuplicateBookError(LibraryError):
    """同一 ISBN 的书重复上架。"""


class BookNotFoundError(LibraryError):
    """要借/要删的书不在馆内。"""


class Library:
    """图书馆：内部用 dict 以 ISBN 为 key 管理藏书（封装约定：_ 前缀表示私有）。"""

    def __init__(self) -> None:
        self._books: dict[str, Book] = {}

    def add_book(self, book: Book) -> None:
        if book.isbn in self._books:
            raise DuplicateBookError(f"ISBN {book.isbn} 已在馆内")
        self._books[book.isbn] = book

    def remove_book(self, isbn: str) -> Book:
        if isbn not in self._books:
            raise BookNotFoundError(f"馆内没有 ISBN {isbn} 的书")
        return self._books.pop(isbn)

    def find(self, keyword: str) -> list[Book]:
        """按标题/作者模糊查找。"""
        kw = keyword.lower()
        return [
            b for b in self._books.values()
            if kw in b.title.lower() or kw in b.author.lower()
        ]

    def find_by_isbn(self, isbn: str) -> Optional[Book]:
        """按 ISBN 精确查找；找不到返回 None（Optional 的典型用法）。"""
        return self._books.get(isbn)

    def find_if(self, predicate: Callable[[Book], bool]) -> list[Book]:
        """按任意条件筛选（Callable 的典型用法：函数也能当参数传）。"""
        return [b for b in self._books.values() if predicate(b)]

    def count(self) -> int:
        return len(self._books)
