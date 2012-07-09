from experimental import selectortools


def test_MulticontextSelection___init___01():

    selection = selectortools.MulticontextSelection()
    assert isinstance(selection, selectortools.MulticontextSelection)
