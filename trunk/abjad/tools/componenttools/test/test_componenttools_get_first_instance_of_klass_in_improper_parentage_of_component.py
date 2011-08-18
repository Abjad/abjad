from abjad import *


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_01():

    t = Staff("c'8 d'8 e'8 f'8")

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Note) is t[0]
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Staff) is t
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Score) is None

def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_02():
    '''Return first explicit Abjad ``Staff`` in parentage of client.
        Otherwise ``None``.'''

    t = Score([Staff("c'8 d'8 e'8 f'8")])

    r'''
    \new Score <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t.leaves[0], Staff) is t[0]
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Staff) is t[0]
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Staff) is None


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_03():
    '''Return first explicit Abjad staff in parentage of client.
    '''

    t = Note("c'4")

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Staff) is None


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_04():
    '''Get first instance of score in improper parentage.
    '''

    t = Score([Staff("c'8 d'8 e'8 f'8")])
    t.name = 'foo'

    r'''
    \context Score = "foo" <<
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }
    >>
    '''

    #assert t.leaves[0].score.explicit is t
    #assert t[0].score.explicit is t
    #assert t.score.explicit is t

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t.leaves[0], Score) is t
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Score) is t
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Score) is t


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_05():
    '''First explicit Abjad ``Score`` in parentage of client.
        If no explicit ``Score`` in parentage, return ``None``.'''

    t = Staff("c'8 d'8 e'8 f'8")
    t.name = 'foo'

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''

    #assert t[0].score.explicit is None
    #assert t.score.explicit is None

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Score) is None
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Score) is None


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_06():
    '''Get first instance of voice in improper parentage of component.
    '''

    t = Score([Staff([Voice("c'8 d'8 e'8 f'8")])])
    voice = t[0][0]

    r'''
    \new Score <<
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
        }
    >>
    '''

#   assert t.leaves[0].voice.explicit is voice
#   assert t[0][0].voice.explicit is voice
#   assert t[0].voice.explicit is None
#   assert t.voice.explicit is None

    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t.leaves[0], Voice) is voice
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0][0], Voice) is voice
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t[0], Voice) is None
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Voice) is None


def test_componenttools_get_first_instance_of_klass_in_improper_parentage_of_component_07():
    '''Return first explicit Abjad ``Voice`` in parentage of client.
    Otherwise ``None``.
    '''

    t = Note("c'4")

    #assert t.voice.explicit is None
    assert componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        t, Voice) is None
