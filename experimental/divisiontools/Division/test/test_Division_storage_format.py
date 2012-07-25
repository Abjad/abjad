from experimental import divisiontools


def test_Division_storage_format_01():

    division_1 = divisiontools.Division('[5, 8)')
    division_2 = eval(division_1.storage_format)

    r'''
    divisiontools.Division('(2, 8]')
    '''

    assert isinstance(division_1, divisiontools.Division)
    assert isinstance(division_2, divisiontools.Division)
    assert division_1 is not division_2
    assert division_1 == division_2
