from abjad.tools.componenttools.iterate_components_backward_in_expr import iterate_components_backward_in_expr
from abjad.tools.componenttools.iterate_components_forward_in_expr import iterate_components_forward_in_expr


def get_nth_component_in_expr(expr, klasses, n=0):
    r'''.. versionadded:: 1.1

    Get component `n` in the `klasses` of `expr`::

        abjad> staff = Staff([])
        abjad> durations = [Duration(n, 16) for n in range(1, 5)]
        abjad> notes = notetools.make_notes([0, 2, 4, 5], durations)
        abjad> rests = resttools.make_rests(durations)
        abjad> from abjad.tools import sequencetools
        abjad> leaves = sequencetools.interlace_sequences(notes, rests)
        abjad> staff.extend(leaves)

    ::

        abjad> print staff.format
        \new Staff {
            c'16
            r16
            d'8
            r8
            e'8.
            r8.
            f'4
            r4
        }

    ::

        abjad> for n in range(4):
        ...        componenttools.get_nth_component_in_expr(staff, Note, n)
        ...
        Note("c'16")
        Note("d'8")
        Note("e'8.")
        Note("f'4")

    ::

        abjad> for n in range(4):
        ...        componenttools.get_nth_component_in_expr(staff, Rest, n)
        ...
        Rest('r16')
        Rest('r8')
        Rest('r8.')
        Rest('r4')

    ::

        abjad> componenttools.get_nth_component_in_expr(staff, Staff)
        Staff{8}

    Read right-to-left for negative values of `n`::

        abjad> for n in range(3, -1, -1):
        ...        componenttools.get_nth_component_in_expr(staff, Rest, n)
        ...
        Rest('r4')
        Rest('r8.')
        Rest('r8')
        Rest('r16')

    Return component or none.

    .. versionchanged:: 2.0
        renamed ``iterate.get_nth()`` to
        ``componenttools.get_nth_component_in_expr()``.
    '''

    if not isinstance(n, (int, long)):
        raise ValueError

    if 0 <= n:
        for i, x in enumerate(iterate_components_forward_in_expr(expr, klasses)):
            if i == n:
                return x
    else:
        for i, x in enumerate(iterate_components_backward_in_expr(expr, klasses)):
            if i == abs(n) - 1:
                return x
