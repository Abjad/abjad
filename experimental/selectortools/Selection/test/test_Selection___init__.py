from experimental import specificationtools


def test_Selection___init___01():

    selection = selectortools.Selection()
    assert isinstance(selection, selectortools.Selection)
