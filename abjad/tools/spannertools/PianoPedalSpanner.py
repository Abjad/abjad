# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner


class PianoPedalSpanner(Spanner):
    r'''A piano pedal spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")
        >>> pedal = spannertools.PianoPedalSpanner()
        >>> attach(pedal, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set Staff.pedalSustainStyle = #'mixed
            c'8 \sustainOn
            d'8
            e'8
            f'8 \sustainOff
        }

    '''

    ### CLASS VARIABLES ###

    _kinds = {
        'sustain': (r'\sustainOn', r'\sustainOff'),
        'sostenuto':(r'\sostenutoOn', r'\sostenutoOff'),
        'corda': (r'\unaCorda', r'\treCorde'),
        }

    _styles = [
        'text',
        'bracket',
        'mixed',
        ]

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None,
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            components,
            overrides=overrides,
            )
        self.kind = 'sustain'
        self.style = 'mixed'

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.kind = self.kind
        new.style = self.style

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(r"\set Staff.pedalSustainStyle = #'%s" % self.style)
        return result

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            result.append(self._kinds[self.kind][0])
        if self._is_my_last_leaf(leaf):
            result.append(self._kinds[self.kind][1])
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Get piano pedal spanner kind:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.PianoPedalSpanner()
            >>> attach(spanner, staff[:])
            >>> spanner.kind
            'sustain'

        Set piano pedal spanner kind:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.PianoPedalSpanner()
            >>> attach(spanner, staff[:])
            >>> spanner.kind = 'sostenuto'
            >>> spanner.kind
            'sostenuto'

        Acceptable values ``'sustain'``, ``'sostenuto'``, ``'corda'``.
        '''
        return self._kind

    @kind.setter
    def kind(self, arg):
        if not arg in self._kinds.keys():
            raise ValueError("Type must be in %s" % self._kinds.keys())
        self._kind = arg

    @property
    def style(self):
        r'''Get piano pedal spanner style:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.PianoPedalSpanner()
            >>> attach(spanner, staff[:])
            >>> spanner.style
            'mixed'

        Set piano pedal spanner style:

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> spanner = spannertools.PianoPedalSpanner()
            >>> attach(spanner, staff[:])
            >>> spanner.style = 'bracket'
            >>> spanner.style
            'bracket'

        Acceptable values ``'mixed'``, ``'bracket'``, ``'text'``.
        '''
        return self._style

    @style.setter
    def style(self, arg):
        if not arg in self._styles:
            raise ValueError("Style must be in %s" % self._styles)
        self._style = arg
