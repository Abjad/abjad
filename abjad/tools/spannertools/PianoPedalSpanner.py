from .Spanner import Spanner
from abjad.tools.lilypondnametools.LilyPondContextSetting import \
    LilyPondContextSetting
from abjad.tools.schemetools.SchemeSymbol import SchemeSymbol


class PianoPedalSpanner(Spanner):
    r'''
    Piano pedal spanner.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> spanner = abjad.PianoPedalSpanner()
        >>> abjad.attach(spanner, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                \set Staff.pedalSustainStyle = #'mixed
                c'8
                \sustainOn
                d'8
                e'8
                f'8
                \sustainOff
            }

    Formats LilyPond ``\sustainOn``, ``\sosenutoOn`` or ``\unaCorda`` on first
    leaf in spanner.

    Formats LilyPond ``\sustainOff``, ``\sostenutoOff`` or ``\treCorde`` on
    last leaf in spanner.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_kind',
        '_style',
        )

    _kinds = {
        'sustain': (r'\sustainOn', r'\sustainOff'),
        'sostenuto': (r'\sostenutoOn', r'\sostenutoOff'),
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
        kind: str = 'sustain',
        style: str = 'mixed',
        ) -> None:
        Spanner.__init__(self)
        if kind not in list(self._kinds.keys()):
            raise ValueError(f'kind must be in {list(self._kinds.keys())!r}.')
        self._kind = kind
        if style not in self._styles:
            raise ValueError(f'style must be in {self._styles!r}.')
        self._style = style

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._kind = self.kind
        new._style = self.style

    def _get_lilypond_format_bundle(self, leaf):
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only_leaf(leaf):
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            string = self._kinds[self.kind][0]
            bundle.right.spanner_starts.append(string)
            string = self._kinds[self.kind][1]
            bundle.right.spanner_starts.append(string)
        elif leaf is self[0]:
            style = SchemeSymbol(self.style)
            context_setting = LilyPondContextSetting(
                lilypond_type='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            bundle.update(context_setting)
            string = self._kinds[self.kind][0]
            bundle.right.spanner_starts.append(string)
        elif leaf is self[-1]:
            string = self._kinds[self.kind][1]
            bundle.right.spanner_stops.append(string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self) -> str:
        r'''
        Gets kind of piano pedal spanner.

        ..  container:: example

            Sustain pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sustain')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

            >>> spanner.kind
            'sustain'

        ..  container:: example

            Sostenuto pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='sostenuto')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \sostenutoOn
                    d'8
                    e'8
                    f'8
                    \sostenutoOff
                }

            >>> spanner.kind
            'sostenuto'

        ..  container:: example

            Una corda / tre corde pedal:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(kind='corda')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \unaCorda
                    d'8
                    e'8
                    f'8
                    \treCorde
                }

            >>> spanner.kind
            'corda'

        Returns ``'sustain'``, ``'sostenuto'`` or ``'corda'``.
        '''
        return self._kind

    @property
    def style(self) -> str:
        r'''
        Gets style of piano pedal spanner.

        ..  container:: example

            Mixed style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='mixed')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

            >>> spanner.style
            'mixed'

        ..  container:: example

            Bracket style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='bracket')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'bracket
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

            >>> spanner.style
            'bracket'

        ..  container:: example

            Text style:

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> spanner = abjad.PianoPedalSpanner(style='text')
            >>> abjad.attach(spanner, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \set Staff.pedalSustainStyle = #'text
                    c'8
                    \sustainOn
                    d'8
                    e'8
                    f'8
                    \sustainOff
                }

            >>> spanner.style
            'text'

        Returns ``'mixed'``, ``'bracket'`` or ``'text'``.
        '''
        return self._style
