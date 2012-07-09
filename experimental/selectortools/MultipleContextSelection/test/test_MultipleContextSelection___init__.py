from experimental import selectortools


def test_MultipleContextSelection___init___01():

    selection = selectortools.MultipleContextSelection()
    assert isinstance(selection, selectortools.MultipleContextSelection)
