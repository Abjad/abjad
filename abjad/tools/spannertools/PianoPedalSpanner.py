# -*- coding: utf-8 -*-
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import override


class PianoPedalSpanner(Spanner):
    r'''Piano pedal spanner.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> pedal = spannertools.PianoPedalSpanner()
            >>> attach(pedal, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> f(staff)
            \new Staff {
                \set Staff.pedalSustainStyle = #'mixed
                c'8 \sustainOn
                d'8
                e'8
                f'8 \sustainOff
            }

    Formats LilyPond ``\sustainOn``, ``\sosenutoOn`` or ``\unaCora`` on first
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
        kind='sustain',
        overrides=None,
        style='mixed',
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        if not kind in list(self._kinds.keys()):
            message = 'kind must be in {!r}.'
            message = message.format(list(self._kinds.keys()))
            raise ValueError(message)
        self._kind = kind
        if not style in self._styles:
            message = 'style must be in {!r}.'
            message = message.format(self._styles)
            raise ValueError(message)
        self._style = style

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._kind = self.kind
        new._style = self.style

    def _get_lilypond_format_bundle(self, leaf):
        from abjad.tools import lilypondnametools
        from abjad.tools import schemetools
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        if self._is_my_only_leaf(leaf):
            style = schemetools.SchemeSymbol(self.style)
            context_setting = lilypondnametools.LilyPondContextSetting(
                context_name='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            lilypond_format_bundle.update(context_setting)
            string = self._kinds[self.kind][0]
            lilypond_format_bundle.right.spanner_starts.append(string)
            string = self._kinds[self.kind][1]
            lilypond_format_bundle.right.spanner_starts.append(string)
        elif self._is_my_first_leaf(leaf):
            style = schemetools.SchemeSymbol(self.style)
            context_setting = lilypondnametools.LilyPondContextSetting(
                context_name='Staff',
                context_property='pedalSustainStyle',
                value=style,
                )
            lilypond_format_bundle.update(context_setting)
            string = self._kinds[self.kind][0]
            lilypond_format_bundle.right.spanner_starts.append(string)
        elif self._is_my_last_leaf(leaf):
            string = self._kinds[self.kind][1]
            lilypond_format_bundle.right.spanner_stops.append(string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def kind(self):
        r'''Gets kind of piano pedal spanner.

        ..  container:: example

            Sustain pedal:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(kind='sustain')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8 \sustainOn
                    d'8
                    e'8
                    f'8 \sustainOff
                }

            ::

                >>> spanner.kind
                'sustain'

        ..  container:: example

            Sostenuto pedal:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(kind='sostenuto')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8 \sostenutoOn
                    d'8
                    e'8
                    f'8 \sostenutoOff
                }

            ::

                >>> spanner.kind
                'sostenuto'

        ..  container:: example

            Una corda / tre corde pedal:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(kind='corda')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8 \unaCorda
                    d'8
                    e'8
                    f'8 \treCorde
                }

            ::

                >>> spanner.kind
                'corda'

        Returns ``'sustain'``, ``'sostenuto'`` or ``'corda'``.
        '''
        return self._kind

    @property
    def style(self):
        r'''Gets style of piano pedal spanner.

        ..  container:: example

            Mixed style:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(style='mixed')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'mixed
                    c'8 \sustainOn
                    d'8
                    e'8
                    f'8 \sustainOff
                }

            ::

                >>> spanner.style
                'mixed'

        ..  container:: example

            Bracket style:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(style='bracket')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'bracket
                    c'8 \sustainOn
                    d'8
                    e'8
                    f'8 \sustainOff
                }

            ::

                >>> spanner.style
                'bracket'

        ..  container:: example

            Text style:

            ::

                >>> staff = Staff("c'8 d'8 e'8 f'8")
                >>> spanner = spannertools.PianoPedalSpanner(style='text')
                >>> attach(spanner, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

                >>> print(format(staff))
                \new Staff {
                    \set Staff.pedalSustainStyle = #'text
                    c'8 \sustainOn
                    d'8
                    e'8
                    f'8 \sustainOff
                }

            ::

                >>> spanner.style
                'text'

        Returns ``'mixed'``, ``'bracket'`` or ``'text'``.
        '''
        return self._style