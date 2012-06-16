from experimental import specificationtools


def test_Selection___init___01():

    selection = specificationtools.Selection()
    assert isinstance(selection, specificationtools.Selection)
