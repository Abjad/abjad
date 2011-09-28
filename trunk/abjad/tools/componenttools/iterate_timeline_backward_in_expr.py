from abjad.tools.componenttools.component_to_score_index import component_to_score_index
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def iterate_timeline_backward_in_expr(expr, klass=None):
    r'''.. versionadded:: 2.0

    Iterate timeline backward in `expr`::

        abjad> score = Score([])
        abjad> score.append(Staff(notetools.make_repeated_notes(4, Duration(1, 4))))
        abjad> score.append(Staff(notetools.make_repeated_notes(4)))
        abjad> pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(score)
        abjad> f(score)
        \new Score <<
            \new Staff {
                c'4
                d'4
                e'4
                f'4
            }
            \new Staff {
                g'8
                a'8
                b'8
                c''8
            }
        >>
        abjad> for leaf in componenttools.iterate_timeline_backward_in_expr(score):
        ...     leaf
        ...
        Note("f'4")
        Note("e'4")
        Note("d'4")
        Note("c''8")
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Iterate leaves when `klass` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf

    if klass is None:
        klass = _Leaf

    component_generator = iterate_components_forward_in_expr(expr, klass = klass)
    components = list(component_generator)

    def _sort_helper(component_1, component_2):
        result = cmp(component_1._offset.stop,
            component_2._offset.stop)
        if result == 0:
            return cmp(
                component_to_score_index(component_1),
                component_to_score_index(component_2))
        else:
            # note negative result of cmp() is returned
            # for backward time sort
            return -result

    components.sort(_sort_helper)

    for component in components:
        yield component
