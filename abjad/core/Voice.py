import typing

from abjad.system.Tag import Tag

from .Context import Context


class Voice(Context):
    r"""
    Voice.

    ..  container:: example

        >>> voice = abjad.Voice("c'8 d'8 e'8 f'8")
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'8
                d'8
                e'8
                f'8
            }

    Voice-contexted indicators like dynamics work with nested voices.

    ..  container:: example

        Forte affects all red notes:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).note_head.color = 'red'
        >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
        >>> abjad.attach(literal, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
        >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
        >>> abjad.attach(literal, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('f')
        >>> abjad.attach(dynamic, outer_red_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(outer_red_voice)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                \f
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate(outer_red_voice).leaves():
        ...     dynamic = abjad.inspect(leaf).effective(abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        e''8 Dynamic('f')
        d''8 Dynamic('f')
        c''4 Dynamic('f')
        b'4 Dynamic('f')
        c''8 Dynamic('f')
        e'4 None
        f'4 None
        e'8 None
        d''8 Dynamic('f')

    ..  container:: example

        Piano affects all blue notes:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).note_head.color = 'red'
        >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
        >>> abjad.attach(literal, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
        >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
        >>> abjad.attach(literal, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('p')
        >>> abjad.attach(dynamic, inner_blue_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(outer_red_voice)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        \p
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate(outer_red_voice).leaves():
        ...     dynamic = abjad.inspect(leaf).effective(abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        e''8 None
        d''8 None
        c''4 None
        b'4 None
        c''8 None
        e'4 Dynamic('p')
        f'4 Dynamic('p')
        e'8 Dynamic('p')
        d''8 None

    ..  container:: example

        Mezzoforte affects red notes from C4 forward:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).note_head.color = 'red'
        >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
        >>> abjad.attach(literal, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
        >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
        >>> abjad.attach(literal, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('mf')
        >>> abjad.attach(dynamic, inner_red_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(outer_red_voice)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        \mf
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate(outer_red_voice).leaves():
        ...     dynamic = abjad.inspect(leaf).effective(abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        e''8 None
        d''8 None
        c''4 Dynamic('mf')
        b'4 Dynamic('mf')
        c''8 Dynamic('mf')
        e'4 None
        f'4 None
        e'8 None
        d''8 Dynamic('mf')

    ..  container:: example

        Mezzoforte and piano set at the same time:

        >>> outer_red_voice = abjad.Voice("e''8 d''", name='Red_Voice')
        >>> inner_red_voice = abjad.Voice("c''4 b' c''8", name='Red_Voice')
        >>> inner_blue_voice = abjad.Voice("e'4 f' e'8", name='Blue_Voice')
        >>> container = abjad.Container(
        ...     [inner_red_voice, inner_blue_voice],
        ...     simultaneous=True,
        ...     )
        >>> outer_red_voice.append(container)
        >>> outer_red_voice.extend("d''8")
        >>> abjad.override(outer_red_voice).note_head.color = 'red'
        >>> literal = abjad.LilyPondLiteral(r'\voiceOne')
        >>> abjad.attach(literal, outer_red_voice[0])
        >>> abjad.override(inner_blue_voice).note_head.color = 'blue'
        >>> literal = abjad.LilyPondLiteral(r'\voiceTwo')
        >>> abjad.attach(literal, inner_blue_voice[0])
        >>> dynamic = abjad.Dynamic('mf')
        >>> abjad.attach(dynamic, inner_red_voice[0])
        >>> dynamic = abjad.Dynamic('p')
        >>> abjad.attach(dynamic, inner_blue_voice[0])
        >>> abjad.show(outer_red_voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(outer_red_voice)
            \context Voice = "Red_Voice"
            \with
            {
                \override NoteHead.color = #red
            }
            {
                \voiceOne
                e''8
                d''8
                <<
                    \context Voice = "Red_Voice"
                    {
                        c''4
                        \mf
                        b'4
                        c''8
                    }
                    \context Voice = "Blue_Voice"
                    \with
                    {
                        \override NoteHead.color = #blue
                    }
                    {
                        \voiceTwo
                        e'4
                        \p
                        f'4
                        e'8
                    }
                >>
                d''8
            }

        >>> for leaf in abjad.iterate(outer_red_voice).leaves():
        ...     dynamic = abjad.inspect(leaf).effective(abjad.Dynamic)
        ...     print(leaf, dynamic)
        ...
        e''8 None
        d''8 None
        c''4 Dynamic('mf')
        b'4 Dynamic('mf')
        c''8 Dynamic('mf')
        e'4 Dynamic('p')
        f'4 Dynamic('p')
        e'8 Dynamic('p')
        d''8 Dynamic('mf')

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Contexts"

    __slots__ = ()

    _default_lilypond_type = "Voice"

    ### INITIALIZER ###

    def __init__(
        self,
        components=None,
        lilypond_type: str = "Voice",
        simultaneous: bool = None,
        name: str = None,
        tag: Tag = None,
    ) -> None:
        Context.__init__(
            self,
            components=components,
            lilypond_type=lilypond_type,
            simultaneous=simultaneous,
            name=name,
            tag=tag,
        )

    ### PUBLIC PROPERTIES ###

    @property
    def tag(self) -> typing.Optional[Tag]:
        r"""
        Gets tag.

        ..  container:: example

            >>> voice = abjad.Voice("c'4 d' e' f'", tag=abjad.Tag('RED'))
            >>> abjad.show(voice) # doctest: +SKIP

            >>> abjad.f(voice, strict=20)
            \new Voice          %! RED
            {                   %! RED
                c'4
                d'4
                e'4
                f'4
            }                   %! RED

        """
        return super().tag
