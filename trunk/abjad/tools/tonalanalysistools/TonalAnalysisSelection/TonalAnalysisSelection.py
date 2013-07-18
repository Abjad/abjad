from abjad.tools.selectiontools.Selection import Selection


class TonalAnalysisSelection(Selection):
    r'''Tonal analysis selection.

    ::

        >>> staff = Staff("c'4 d' e' f'")

    .. doctest::

        >>> f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
        }

    ::

        >>> show(staff) # doctest: +SKIP

    '''

    pass
