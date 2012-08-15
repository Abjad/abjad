def get_first_component_with_name_in_proper_parentage_of_component(component, name):
    r'''.. versionadded:: 2.0

    Get first component with `name` in proper parentage of `component`::

        >>> score = Score([Staff("c'4 d'4 e'4 f'4")])
        >>> score.name = 'The Score'

    ::

        >>> f(score)
        \context Score = "The Score" <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
        >>

    ::

        >>> leaf = score.leaves[0]

    ::

        >>> componenttools.get_first_component_with_name_in_proper_parentage_of_component(
        ...     leaf, 'The Score')
        Score-"The Score"<<1>>

    ::

        >>> componenttools.get_first_component_with_name_in_proper_parentage_of_component(
        ...     leaf, 'foo') is None
        True

    Return component or none.
    '''
    from abjad.tools import componenttools

    for parent in componenttools.get_proper_parentage_of_component(component):
        if getattr(parent, 'name', None) == name:
            return parent
