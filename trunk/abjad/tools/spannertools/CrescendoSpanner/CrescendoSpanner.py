from abjad.tools.spannertools.HairpinSpanner import HairpinSpanner


class CrescendoSpanner(HairpinSpanner):
    r'''Abjad crescendo spanner that includes rests::

        abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        abjad> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        abjad> spannertools.CrescendoSpanner(staff[:], include_rests = True)
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        abjad> f(staff)
        \new Staff {
            r4 \<
            c'8
            d'8
            e'8
            f'8
            r4 \!
        }

    Abjad crescendo spanner that does not include rests::

        abjad> staff = Staff("r4 c'8 d'8 e'8 f'8 r4")

    ::

        abjad> f(staff)
        \new Staff {
            r4
            c'8
            d'8
            e'8
            f'8
            r4
        }

    ::

        abjad> spannertools.CrescendoSpanner(staff[:], include_rests = False)
        CrescendoSpanner(r4, c'8, d'8, e'8, f'8, r4)

    ::

        abjad> f(staff)
        \new Staff {
            r4
            c'8 \<
            d'8
            e'8
            f'8 \!
            r4
        }

    Return crescendo spanner.
    '''

    def __init__(self, components = None, include_rests = True):
        HairpinSpanner.__init__(
            self, components = components, descriptor = '<', include_rests = include_rests)
