from experimental import specificationtools
import copy


def test_OrdinalConstant___copy___01():

    constant_1 = specificationtools.OrdinalConstant('x', -1, 'left')
    constant_2 = copy.deepcopy(constant_1)

    assert isinstance(constant_1, specificationtools.OrdinalConstant)
    assert isinstance(constant_2, specificationtools.OrdinalConstant)
    assert not constant_1 is constant_2
    assert constant_1 == constant_2
