"""W2 冒烟测试：验证核心流程能跑通（pytest 基础：fixture / assert / raises）。"""

import pytest

from w2_library.library import (
    Book,
    BookNotFoundError,
    DigitalBook,
    DuplicateBookError,
    Library,
)


@pytest.fixture
def lib() -> Library:
    """fixture：每个测试开跑前先布置好一个有 2 本书的图书馆。"""
    library = Library()
    library.add_book(Book("三体", "刘慈欣", "978-7-536-69293-0"))
    library.add_book(Book("小王子", "圣埃克苏佩里", "978-7-544-24186-5"))
    return library


def test_add_and_count(lib: Library) -> None:
    assert lib.count() == 2


def test_add_duplicate_raises(lib: Library) -> None:
    with pytest.raises(DuplicateBookError):
        lib.add_book(Book("三体2", "刘慈欣", "978-7-536-69293-0"))


def test_remove_and_not_found(lib: Library) -> None:
    removed = lib.remove_book("978-7-536-69293-0")
    assert removed.title == "三体"
    with pytest.raises(BookNotFoundError):
        lib.remove_book("978-7-536-69293-0")


def test_find_by_author(lib: Library) -> None:
    result = lib.find("刘慈欣")
    assert len(result) == 1
    assert result[0].title == "三体"


def test_find_by_isbn_none_when_missing(lib: Library) -> None:
    assert lib.find_by_isbn("000-000") is None


def test_find_if_with_callable(lib: Library) -> None:
    # “三体”2 字、“小王子”3 字，所以 >= 2 的有 2 本
    long_titles = lib.find_if(lambda b: len(b.title) >= 2)
    assert len(long_titles) == 2


def test_inheritance_and_polymorphism() -> None:
    """DigitalBook 继承 Book：describe 行为不同 = 多态。"""
    paper = Book("三体", "刘慈欣", "978-7-536-69293-0")
    ebook = DigitalBook("三体", "刘慈欣", "978-7-536-69293-1", file_format="epub")

    assert "电子版: epub" in ebook.describe()
    assert "电子版" not in paper.describe()
    # 继承链：DigitalBook 是 Book 的子类
    assert isinstance(ebook, Book)
