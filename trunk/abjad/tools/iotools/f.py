def f(expr):
    r'''Format `expr` and print to standard out::

        abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        abjad> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
        }

    Return none.
    '''

    print expr.format
