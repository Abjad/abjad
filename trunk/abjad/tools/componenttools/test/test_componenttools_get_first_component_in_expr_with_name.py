from abjad import *
import py.test


def test_componenttools_get_first_component_in_expr_with_name_01():
    '''Find by name.'''

    v1 = Voice([Note(i, (1, 4)) for i in range(2)])
    v2 = Voice([Note(i, (1, 4)) for i in range(2, 4)])
    v1.name = 'voiceOne'
    t = Staff([v1, v2])

    assert componenttools.get_first_component_in_expr_with_name(t, name = 'voiceOne') == v1


def test_componenttools_get_first_component_in_expr_with_name_02():
    '''Raise missing component error on no match.'''

    v = Voice("c'8 d'8 e'8 f'8")
    v.context = 'MyStrangeVoice'
    v.name = 'voice_1'
    t = Staff([v])

    assert py.test.raises(
        MissingComponentError,
        "componenttools.get_first_component_in_expr_with_name(t, name = 'voice_200')")


def test_componenttools_get_first_component_in_expr_with_name_03():
    '''Full test.'''

    vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
    vl1.name = 'low'
    vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    vl2.name = 'low'
    vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
    vh1.name = 'high'
    vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
    vh2.name = 'high'

    s1 = Staff([vh1, vl1])
    s1.name = 'mystaff'
    s1.is_parallel = True
    s2 = Staff([vh2, vl2])
    s2.name = 'mystaff'
    s2.is_parallel = True

    fn = vl1[0]

    seq = Container([s1, s2])

    assert componenttools.get_first_component_in_expr_with_name(seq, 'mystaff') == s1
    assert componenttools.get_first_component_in_expr_with_name(seq, 'low') == vl1
    assert componenttools.get_first_component_in_expr_with_name(seq, 'high') == vh1
    assert py.test.raises(MissingComponentError,
        "componenttools.get_first_component_in_expr_with_name(seq, 'nonexistent')")
