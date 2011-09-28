from abjad.tools.componenttools.component_to_score_root import component_to_score_root
from abjad.tools.componenttools.iterate_timeline_backward_in_expr import iterate_timeline_backward_in_expr


def iterate_timeline_backward_from_component(expr, klass=None):
    r'''.. versionadded:: 2.0

    Iterate timeline backward from `component`::

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
        abjad> for leaf in componenttools.iterate_timeline_backward_from_component(score[1][2]):
        ...     leaf
        ...
        Note("b'8")
        Note("c'4")
        Note("a'8")
        Note("g'8")

    Yield components sorted backward by score offset stop time.

    Iterate leaves when `klass` is none.

    .. todo:: optimize to avoid behind-the-scenes full-score traversal.
    '''
    from abjad.tools.leaftools._Leaf import _Leaf

    if klass is None:
        klass = _Leaf

    root = component_to_score_root(expr)
    component_generator = iterate_timeline_backward_in_expr(root, klass = klass)

    yielded_expr = False
    for component in component_generator:
        if yielded_expr:
            yield component
        elif component is expr:
            yield component
            yielded_expr = True
