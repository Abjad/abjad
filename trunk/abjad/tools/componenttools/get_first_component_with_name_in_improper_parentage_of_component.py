from abjad.tools.componenttools.get_improper_parentage_of_component import get_improper_parentage_of_component


def get_first_component_with_name_in_improper_parentage_of_component(component, name):
    r'''.. versionadded:: 2.0

    Get first component with `name` in improper parentage of `component`::

        abjad> score = Score([Staff("c'4 d'4 e'4 f'4")])
        abjad> score.name = 'The Score'

    ::

        abjad> f(score)
        \context Score = "The Score" <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
        >>

    ::

        abjad> leaf = score.leaves[0]

    ::

        abjad> componenttools.get_first_component_with_name_in_improper_parentage_of_component(leaf, 'The Score')
        Score-"The Score"<<1>>

    ::

        abjad> componenttools.get_first_component_with_name_in_improper_parentage_of_component(leaf, 'foo') is None
        True

    Return component or none.
    '''

    for parent in get_improper_parentage_of_component(component):
        if getattr(parent, 'name', None) == name:
            return parent
