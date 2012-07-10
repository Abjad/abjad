from experimental import selectortools


def test_MultipleContextTimespanSelector___init___01():

    selection = selectortools.MultipleContextTimespanSelector()
    assert isinstance(selection, selectortools.MultipleContextTimespanSelector)
