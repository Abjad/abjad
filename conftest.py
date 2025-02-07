import pytest

import abjad


@pytest.fixture(autouse=True)
def inject_abjad_into_doctest_namespace(doctest_namespace):
    """
    Inject Abjad into doctest namespace.
    """
    doctest_namespace["abjad"] = abjad
