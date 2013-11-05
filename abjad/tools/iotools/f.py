# -*- encoding: utf-8 -*-


def f(expr):
    r'''Formats `expr` and prints to standard out.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Returns none.
    '''

    print format(expr, 'lilypond')
