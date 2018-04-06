import abjad
import copy


def test_datastructuretools_OrderedDict___copy___01():

    dictionary_1 = abjad.OrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = copy.copy(dictionary_1)

    assert dictionary_1 == dictionary_2
    assert repr(dictionary_1) == repr(dictionary_2)
