from abjad.tools import componenttools


def iterate_contexts_forward_in_expr(expr, start=0, stop=None):
    r'''.. versionadded:: 2.0

    Iterate contexts forward in `expr`::

        >>> staff = Staff([Voice("c'8 d'8"), Voice("e'8 f'8 g'8")])
        >>> Tuplet(Fraction(2, 3), staff[1][:])
        Tuplet(2/3, [e'8, f'8, g'8])
        >>> staff.is_parallel = True

    ::

        >>> f(staff)
        \new Staff <<
            \new Voice {
                c'8
                d'8
            }
            \new Voice {
                \times 2/3 {
                    e'8
                    f'8
                    g'8
                }
            }
        >>

    ::

        >>> for x in contexttools.iterate_contexts_forward_in_expr(staff):
        ...   x
        Staff<<2>>
        Voice{2}
        Voice{1}

    Ignore threads.

    Return generator.
    '''
    from abjad.tools import contexttools

    return componenttools.iterate_components_forward_in_expr(expr, contexttools.Context, start=start, stop=stop)
