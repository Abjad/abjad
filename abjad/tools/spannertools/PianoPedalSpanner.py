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

    __slots__ = (
        '_kind',
        '_style',
        )

    _kinds = {
        'sustain': (r'\sustainOn', r'\sustainOff'),
        'sostenuto':(r'\sostenutoOn', r'\sostenutoOff'),
        'corda': (r'\unaCorda', r'\treCorde'),
        }

    _styles = (
        'text',
        'bracket',
        'mixed',
        )

    ### INITIALIZER ###

    def __init__(
        self, 
        kind='sustain',
        style='mixed',
        overrides=None,
        ):
        Spanner.__init__(
            self, 
            overrides=overrides,
            )
        if not kind in self._kinds.keys():
            message = 'kind must be in {!r}.'.format(self._kinds.keys())
            raise ValueError(message)
        self._kind = kind
        if not style in self._styles:
            message = 'style must be in {!r}.'.format(self._styles)
            raise ValueError(message)
        self._style = style

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new.kind = self.kind
        new.style = self.style

    def _format_before_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            string = r"\set Staff.pedalSustainStyle = #'{}".format(self.style)
            result.append(string)
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
        r'''Gets piano pedal spanner kind.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner()
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> spanner.kind
                'sustain'

        Set to ``'sustain'``, ``'sostenuto'`` or ``'corda'``.

        Returns string.
        '''
        return self._kind

    @property
    def style(self):
        r'''Gets piano pedal spanner style.

        ..  container:: example

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner()
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ::

                >>> spanner.style
                'mixed'

        Set to ``'mixed'``, ``'bracket'`` or ``'text'``.

        Returns string.
        '''
        return self._style
