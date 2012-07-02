from experimental import selectortools
from experimental import specificationtools


def test_BackgroundElementSelector_storage_format_01():

    selector = selectortools.BackgroundElementSelector(klass=specificationtools.Segment, index='red')

    r'''
    selectortools.BackgroundElementSelector(
        klass=specificationtools.Segment,
        index='red'
        )
    '''

    assert selector.storage_format == "selectortools.BackgroundElementSelector(\n\tklass=specificationtools.Segment,\n\tindex='red'\n\t)"

    new_selector = eval(selector.storage_format)

    assert new_selector == selector
