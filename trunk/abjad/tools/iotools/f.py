def f(expr):
    r'''Format `expr` and print to standard out::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return none.
    '''

    print expr.lilypond_format
