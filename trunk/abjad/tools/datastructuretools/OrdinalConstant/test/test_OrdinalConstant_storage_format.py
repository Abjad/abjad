from abjad.tools import *


def test_OrdinalConstant_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    vector_constant_1 = datastructuretools.OrdinalConstant('x', -1, 'Left')
    storage_format = vector_constant_1.storage_format

    assert storage_format == 'Left'
    vector_constant_2 = eval(storage_format)

    assert isinstance(vector_constant_1, datastructuretools.OrdinalConstant)
    assert isinstance(vector_constant_2, datastructuretools.OrdinalConstant)
    assert not vector_constant_1 is vector_constant_2 
    assert vector_constant_1 == vector_constant_2
