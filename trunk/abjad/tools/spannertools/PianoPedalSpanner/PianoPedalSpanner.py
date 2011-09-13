from abjad.tools.spannertools.PianoPedalSpanner._PianoPedalSpannerFormatInterface import _PianoPedalSpannerFormatInterface
from abjad.tools.spannertools.Spanner import Spanner


class PianoPedalSpanner(Spanner):
    r'''Abjad piano pedal spanner::

            abjad> staff = Staff("c'8 d'8 e'8 f'8")

    ::

            abjad> spannertools.PianoPedalSpanner(staff[:])
            PianoPedalSpanner(c'8, d'8, e'8, f'8)

    ::

            abjad> f(staff)
            \new Staff {
                \set Staff.pedalSustainStyle = #'mixed
                c'8 \sustainOn
                d'8
                e'8
                f'8 \sustainOff
            }

    Return piano pedal spanner.
    '''

    def __init__(self, components = None):
        Spanner.__init__(self, components)
        self._format = _PianoPedalSpannerFormatInterface(self)
        self.kind = 'sustain'
        self.style = 'mixed'

    ### PRIVATE ATTRIBUTES ###

    _styles = ['text', 'bracket', 'mixed']

    _kinds = {'sustain': (r'\sustainOn', r'\sustainOff'),
            'sostenuto':(r'\sostenutoOn', r'\sostenutoOff'),
            'corda': (r'\unaCorda', r'\treCorde')}

    ### PUBLIC ATTRIBUTES ###

    @apply
    def kind():
        def fget(self):
            r'''Get piano pedal spanner kind::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.PianoPedalSpanner(staff[:])
                abjad> spanner.kind
                'sustain'

            Set piano pedal spanner kind::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.PianoPedalSpanner(staff[:])
                abjad> spanner.kind = 'sostenuto'
                abjad> spanner.kind
                'sostenuto'

            Acceptable values ``'sustain'``, ``'sostenuto'``, ``'corda'``.
            '''
            return self._kind
        def fset(self, arg):
            if not arg in self._kinds.keys():
                raise ValueError("Type must be in %s" % self._kinds.keys())
            self._kind = arg
        return property(**locals())

    @apply
    def style():
        def fget(self):
            r'''Get piano pedal spanner style::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.PianoPedalSpanner(staff[:])
                abjad> spanner.style
                'mixed'

            Set piano pedal spanner style::

                abjad> staff = Staff("c'8 d'8 e'8 f'8")
                abjad> spanner = spannertools.PianoPedalSpanner(staff[:])
                abjad> spanner.style = 'bracket'
                abjad> spanner.style
                'bracket'

            Acceptable values ``'mixed'``, ``'bracket'``, ``'text'``.
            '''
            return self._style
        def fset(self, arg):
            if not arg in self._styles:
                raise ValueError("Style must be in %s" % self._styles)
            self._style = arg
        return property(**locals())
