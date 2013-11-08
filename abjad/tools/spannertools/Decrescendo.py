# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Hairpin import Hairpin


class Decrescendo(Hairpin):
    r'''A decrescendo spanner that includes rests.

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> decrescendo = spannertools.Decrescendo(include_rests=True)
        >>> attach(decrescendo, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4 \>
            c'8
            d'8
            e'8
            f'8
            r4 \!
        }

    Abjad decrescendo spanner that does not include rests:

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        >>> decrescendo = spannertools.Decrescendo(include_rests=False)
        >>> attach(decrescendo, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4
            c'8 \>
            d'8
            e'8
            f'8 \!
            r4
        }

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        include_rests=True, 
        direction=None,
        overrides=None,
        ):
        Hairpin.__init__(
            self, 
            components=components, 
            descriptor='>', 
            include_rests=include_rests,
            direction=direction,
            overrides=overrides,
            )
