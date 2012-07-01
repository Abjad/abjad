from experimental import specificationtools


def test_BackgroundElementSelector_storage_format_01():

    selector = specificationtools.BackgroundElementSelector(specificationtools.Segment, 'red')

    r'''
    specificationtools.BackgroundElementSelector(
        specificationtools.Segment,
        'red'
        )
    '''

    assert selector.storage_format == "specificationtools.BackgroundElementSelector(\n\tspecificationtools.Segment,\n\t'red'\n\t)"

    new_selector = eval(selector.storage_format)

    assert new_selector == selector
