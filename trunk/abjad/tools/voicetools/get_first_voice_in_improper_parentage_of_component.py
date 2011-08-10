from abjad.tools.voicetools.Voice import Voice
from abjad.tools import componenttools


def get_first_voice_in_improper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first voice in improper parentage of `component`::

        abjad> voice = Voice("c'8 d'8 e'8 f'8")
        abjad> staff = Staff([voice])

    ::

        abjad> f(staff)
        \new Staff {
            \new Voice {
                c'8
                d'8
                e'8
                f'8
            }
        }

    ::

        abjad> voicetools.get_first_voice_in_improper_parentage_of_component(staff.leaves[0])
        Voice{4}

    Return voice or none.
    '''

    return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        component, Voice)
