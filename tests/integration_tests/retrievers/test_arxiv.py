"""Integration test for Arxiv API Wrapper."""
from typing import List

import pytest

from langchain.document_loaders import ArxivLoader
from langchain.schema import Document


@pytest.fixture
def retriever() -> ArxivLoader:
    return ArxivLoader(query=None)


def assert_docs(docs: List[Document], all_meta: bool = False) -> None:
    for doc in docs:
        assert doc.page_content
        assert doc.metadata
        main_meta = {"Published", "Title", "Authors", "Summary"}
        assert set(doc.metadata).issuperset(main_meta)
        if all_meta:
            assert len(set(doc.metadata)) > len(main_meta)
        else:
            assert len(set(doc.metadata)) == len(main_meta)


def test_load_success(retriever: ArxivLoader) -> None:
    docs = retriever.get_relevant_documents(query="1605.08386")
    assert len(docs) == 1
    assert_docs(docs, all_meta=False)


def test_load_success_all_meta(retriever: ArxivLoader) -> None:
    retriever.load_all_available_meta = True
    retriever.load_max_docs = 2
    docs = retriever.get_relevant_documents(query="ChatGPT")
    assert len(docs) > 1
    assert_docs(docs, all_meta=True)


def test_load_success_init_args() -> None:
    retriever = ArxivLoader(load_max_docs=1, load_all_available_meta=True)
    docs = retriever.get_relevant_documents(query="ChatGPT")
    assert len(docs) == 1
    assert_docs(docs, all_meta=True)


def test_load_no_result(retriever: ArxivLoader) -> None:
    docs = retriever.get_relevant_documents("1605.08386WWW")
    assert not docs