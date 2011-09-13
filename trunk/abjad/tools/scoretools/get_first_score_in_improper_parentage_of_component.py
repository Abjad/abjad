from abjad.tools.scoretools.Score import Score
from abjad.tools import componenttools


def get_first_score_in_improper_parentage_of_component(component):
    r'''.. versionadded:: 2.0

    Get first score in improper parentage of `component`::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")
        abjad> score = Score([staff])

    ::

        abjad> f(score)
        \new Score <<
            \new Staff {
                c'8
                d'8
                e'8
                f'8
            }
        >>


    ::

        abjad> scoretools.get_first_score_in_improper_parentage_of_component(score.leaves[0])
        Score<<1>>

    Return score or none.
    '''

    return componenttools.get_first_instance_of_klass_in_improper_parentage_of_component(
        component, Score)
