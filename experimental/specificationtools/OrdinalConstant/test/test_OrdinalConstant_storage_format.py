from experimental import specificationtools
from experimental.specificationtools.OrdinalConstant import OrdinalConstant


def test_OrdinalConstant_storage_format_01():
    '''Disk format exists and is evaluable.
    '''

    vector_constant_1 = OrdinalConstant('x', -1, 'Left')
    disk_format = vector_constant_1._disk_format

    assert disk_format == 'Left'
    vector_constant_2 = eval(disk_format)

    assert isinstance(vector_constant_1, OrdinalConstant)
    assert isinstance(vector_constant_2, OrdinalConstant)
    assert not vector_constant_1 is vector_constant_2 
    assert vector_constant_1 == vector_constant_2
