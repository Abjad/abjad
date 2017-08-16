import abjad


def test_datastructuretools_TypedOrderedDict___eq___01():

    dictionary_1 = abjad.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = abjad.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_3 = abjad.TypedOrderedDict([
        ('flavor', 'chocolate'), ('count', 2),
        ])

    assert dictionary_1 == dictionary_1
    assert dictionary_1 == dictionary_2
    assert not dictionary_1 == dictionary_3
    assert dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
    assert not dictionary_2 == dictionary_3
    assert not dictionary_3 == dictionary_1
    assert not dictionary_3 == dictionary_2
    assert dictionary_3 == dictionary_3


def test_datastructuretools_TypedOrderedDict___eq___02():

    dictionary_1 = abjad.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2),
        ])
    dictionary_2 = abjad.TypedOrderedDict([
        ('flavor', 'cherry'), ('count', 2), ('color', 'red'),
        ])

    assert dictionary_1 == dictionary_1
    assert not dictionary_1 == dictionary_2
    assert not dictionary_2 == dictionary_1
    assert dictionary_2 == dictionary_2
