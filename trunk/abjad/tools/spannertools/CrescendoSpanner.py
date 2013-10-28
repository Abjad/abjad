# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(HairpinSpanner):
    r'''A crescendo spanner that includes rests.

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

        >>> crescendo = spannertools.CrescendoSpanner(include_rests=True)
        >>> crescendo.attach(staff[:])
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4 \<
            c'8
            d'8
            e'8
            f'8
            r4 \!
        }

    Abjad crescendo spanner that does not include rests:

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

        >>> crescendo = spannertools.CrescendoSpanner(include_rests=False)
        >>> crescendo.attach(staff[:])
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> f(staff)
        \new Staff {
            r4
            c'8 \<
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
        HairpinSpanner.__init__(
            self, components=components, 
            descriptor='<', 
            include_rests=include_rests,
            direction=direction,
            overrides=overrides,
            )
