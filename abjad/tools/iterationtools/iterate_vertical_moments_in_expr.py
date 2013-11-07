# -*- encoding: utf-8 -*-
from abjad.tools.functiontools import iterate


# TODO: optimize without multiple full-component traversal.
def iterate_vertical_moments_in_expr(expr, reverse=False):
    r'''Iterate vertical moments forward in `expr`:

    ::

        >>> score = Score([])
        >>> staff = Staff(r"\times 4/3 { d''8 c''8 b'8 }")
        >>> score.append(staff)

    ::

        >>> piano_staff = scoretools.PianoStaff([])
        >>> piano_staff.append(Staff("a'4 g'4"))
        >>> piano_staff.append(Staff(r"""\clef "bass" f'8 e'8 d'8 c'8"""))
        >>> score.append(piano_staff)

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new Staff {
                \tweak #'text #tuplet-number::calc-fraction-text
                \times 4/3 {
                    d''8
                    c''8
                    b'8
                }
            }
            \new PianoStaff <<
                \new Staff {
                    a'4
                    g'4
                }
                \new Staff {
                    \clef "bass"
                    f'8
                    e'8
                    d'8
                    c'8
                }
            >>
        >>

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(score):
        ...     x.leaves
        ...
        (Note("d''8"), Note("a'4"), Note("f'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("b'8"), Note("g'4"), Note("c'8"))

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     piano_staff):
        ...     x.leaves
        ...
        (Note("a'4"), Note("f'8"))
        (Note("a'4"), Note("e'8"))
        (Note("g'4"), Note("d'8"))
        (Note("g'4"), Note("c'8"))

    Iterate vertical moments backward in `expr`:

    ::

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     score, reverse=True):
        ...     x.leaves
        ...
        (Note("b'8"), Note("g'4"), Note("c'8"))
        (Note("b'8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("g'4"), Note("d'8"))
        (Note("c''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("e'8"))
        (Note("d''8"), Note("a'4"), Note("f'8"))

    ::

        >>> for x in iterationtools.iterate_vertical_moments_in_expr(
        ...     piano_staff, reverse=True):
        ...     x.leaves
        ...
        (Note("g'4"), Note("c'8"))
        (Note("g'4"), Note("d'8"))
        (Note("a'4"), Note("e'8"))
        (Note("a'4"), Note("f'8"))

    Returns generator.
    '''
    return iterate(expr).by_vertical_moment(reverse=reverse)
