from experimental import selectortools
from experimental import specificationtools


def test_BackgroundElementSelector_storage_format_01():

    selector = selectortools.BackgroundElementSelector(specificationtools.Segment, 'red')

    r'''
    selectortools.BackgroundElementSelector(
        specificationtools.Segment,
        'red'
        )
    '''

    assert selector.storage_format == "selectortools.BackgroundElementSelector(\n\tspecificationtools.Segment,\n\t'red'\n\t)"

    new_selector = eval(selector.storage_format)

    assert new_selector == selector
