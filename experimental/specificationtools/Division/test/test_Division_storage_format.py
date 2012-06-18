from experimental import specificationtools


def test_Division_storage_format_01():

    division_1 = specificationtools.Division('[5, 8)')
    division_2 = eval(division_1.storage_format)

    r'''
    specificationtools.Division('(2, 8]')
    '''

    assert isinstance(division_1, specificationtools.Division)
    assert isinstance(division_2, specificationtools.Division)
    assert division_1 is not division_2
    assert division_1 == division_2
