from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class DecrescendoSpanner(HairpinSpanner):
    r'''Abjad decrescendo spanner that includes rests::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

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

        >>> spannertools.DecrescendoSpanner(staff[:], include_rests=True)
        DecrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        >>> f(staff)
        \new Staff {
            r4 \>
            c'8
            d'8
            e'8
            f'8
            r4 \!
        }

    Abjad decrescendo spanner that does not include rests::

        >>> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

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

        >>> spannertools.DecrescendoSpanner(staff[:], include_rests=False)
        DecrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        >>> f(staff)
        \new Staff {
            r4
            c'8 \>
            d'8
            e'8
            f'8 \!
            r4
        }

    Return decrescendo spanner.
    '''

    def __init__(self, components=None, include_rests=True, direction=None):
        HairpinSpanner.__init__(
            self, components=components, descriptor='>', include_rests=include_rests,
            direction=direction)
