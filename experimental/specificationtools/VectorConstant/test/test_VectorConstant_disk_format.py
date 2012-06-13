from experimental import specificationtools
from experimental.specificationtools.VectorConstant import VectorConstant


def test_VectorConstant_disk_format_01():
    '''Disk format exists and is evaluable.
    '''

    vector_constant_1 = VectorConstant('x', -1, 'left')
    disk_format = vector_constant_1._disk_format

    r'''
    specificationtools.VectorConstant(
        'x',
        -1,
        'left'
        )
    '''
    
    vector_constant_2 = eval(disk_format)

    assert isinstance(vector_constant_1, VectorConstant)
    assert isinstance(vector_constant_2, VectorConstant)
    assert not vector_constant_1 is vector_constant_2 
    assert vector_constant_1 == vector_constant_2
