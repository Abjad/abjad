import pytest

import abjad


# tell pytest about Abjad
@pytest.fixture(autouse=True)
def add_libraries(doctest_namespace):
    doctest_namespace["abjad"] = abjad
