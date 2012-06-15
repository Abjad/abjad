from experimental import specificationtools
import copy


def test_VectorConstant___copy___01():

    constant_1 = specificationtools.VectorConstant('x', -1, 'left')
    constant_2 = copy.deepcopy(constant_1)

    assert isinstance(constant_1, specificationtools.VectorConstant)
    assert isinstance(constant_2, specificationtools.VectorConstant)
    assert not constant_1 is constant_2
    assert constant_1 == constant_2
