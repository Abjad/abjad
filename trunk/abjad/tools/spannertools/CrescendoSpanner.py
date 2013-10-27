# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(HairpinSpanner):
    r'''A crescendo spanner that includes rests.

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

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

        >>> spannertools.CrescendoSpanner(staff[:], include_rests=True)
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

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

    ::

        >>> show(staff) # doctest: +SKIP

    Abjad crescendo spanner that does not include rests:

    ::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

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

        >>> spannertools.CrescendoSpanner(staff[:], include_rests=False)
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

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

    ::

        >>> show(staff) # doctest: +SKIP

    Returns crescendo spanner.
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
