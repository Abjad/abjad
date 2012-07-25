from experimental import interpretationtools


def test_Division_storage_format_01():

    division_1 = interpretationtools.Division('[5, 8)')
    division_2 = eval(division_1.storage_format)

    r'''
    interpretationtools.Division('(2, 8]')
    '''

    assert isinstance(division_1, interpretationtools.Division)
    assert isinstance(division_2, interpretationtools.Division)
    assert division_1 is not division_2
    assert division_1 == division_2
