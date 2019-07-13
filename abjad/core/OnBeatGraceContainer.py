import typing
from abjad.top.inspect import inspect as abjad_inspect
from .Container import Container


class OnBeatGraceContainer(Container):
    r"""
    On-beat grace container.

    ..  container:: example

        On-beat grace containers implement custom formatting not available in
        LilyPond:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.OnBeatGraceContainer("a'8 as' b' c'' cs''")
        >>> abjad.slur(container[:])
        >>> abjad.attach(abjad.Articulation(">"), container[0])
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                <<
                    {
                        \set fontSize = #-2
                        \once \override NoteColumn.force-hshift = 0.2
                        \slash
                        <a' \tweak Accidental.stencil ##f d'>8 * 2/5
                        - \accent
                        (
                        as'8 * 2/5
                        b'8 * 2/5
                        c''8 * 2/5
                        cs''8 * 2/5
                        )
                    }
                \\
                    d'4
                >>
                e'4
                f'4
            }

        Custom formatting engraves music at a reduced size.

        Custom formatting positions on-beat grace music starting at the same
        horizontal location as a "main note" which follows.

    ..  container:: example

        Detach on-beat grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.OnBeatGraceContainer("a'8 as' b' c'' cs''")
        >>> abjad.slur(container[:])
        >>> abjad.attach(abjad.Articulation(">"), container[0])
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                <<
                    {
                        \set fontSize = #-2
                        \once \override NoteColumn.force-hshift = 0.2
                        \slash
                        <a' \tweak Accidental.stencil ##f d'>8 * 2/5
                        - \accent
                        (
                        as'8 * 2/5
                        b'8 * 2/5
                        c''8 * 2/5
                        cs''8 * 2/5
                        )
                    }
                \\
                    d'4
                >>
                e'4
                f'4
            }

        >>> abjad.detach(abjad.OnBeatGraceContainer, voice[1])
        (OnBeatGraceContainer("<a'>8 as'8 b'8 c''8 cs''8"),)

        >>> abjad.detach(abjad.OnBeatGraceContainer, voice[1])
        ()

        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                d'4
                e'4
                f'4
            }

    ..  container:: example

        Move on-beat grace containers like this:

        >>> voice = abjad.Voice("c'4 d'4 e'4 f'4")
        >>> container = abjad.OnBeatGraceContainer("a'8 as' b' c'' cs''")
        >>> abjad.slur(container[:])
        >>> abjad.attach(abjad.Articulation(">"), container[0])
        >>> abjad.attach(container, voice[1])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                <<
                    {
                        \set fontSize = #-2
                        \once \override NoteColumn.force-hshift = 0.2
                        \slash
                        <a' \tweak Accidental.stencil ##f d'>8 * 2/5
                        - \accent
                        (
                        as'8 * 2/5
                        b'8 * 2/5
                        c''8 * 2/5
                        cs''8 * 2/5
                        )
                    }
                \\
                    d'4
                >>
                e'4
                f'4
            }

        >>> result = abjad.detach(abjad.OnBeatGraceContainer, voice[1])
        >>> container = result[0]
        >>> abjad.attach(container, voice[3])
        >>> abjad.show(voice) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(voice)
            \new Voice
            {
                c'4
                d'4
                e'4
                <<
                    {
                        \set fontSize = #-2
                        \once \override NoteColumn.force-hshift = 0.2
                        \slash
                        <a' \tweak Accidental.stencil ##f f'>8 * 2/5
                        - \accent
                        (
                        as'8 * 2/5
                        b'8 * 2/5
                        c''8 * 2/5
                        cs''8 * 2/5
                        )
                    }
                \\
                    f'4
                >>
            }

    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Containers"

    __slots__ = "_main_leaf"

    ### INITIALIZER ###

    def __init__(self, components=None, tag: str = None) -> None:
        # _main_leaf slot must be initialized before container initialization
        self._main_leaf = None
        Container.__init__(self, components, tag=tag)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        """
        Gets new after grace container arguments.

        Returns tuple of single empty list.
        """
        return ([],)

    ### PRIVATE METHODS ###

    def _attach(self, leaf):
        import abjad

        if not isinstance(leaf, abjad.Leaf):
            raise TypeError(f"must attach to leaf (not {leaf!r}).")
        leaf._on_beat_grace_container = self
        self._main_leaf = leaf

    def _detach(self):
        if self._main_leaf is not None:
            main_leaf = self._main_leaf
            main_leaf._on_beat_grace_container = None
            self._main_leaf = None
        return self

    def _format_opening_slot(self, bundle):
        result = []
        result.append(("comments", bundle.opening.comments))
        result.append(("commands", bundle.opening.commands))
        strings = [
            r"\set fontSize = #-2",
            r"\once \override NoteColumn.force-hshift = 0.2",
            r"\slash",
        ]
        result.append(("custom", strings))
        return self._format_slot_contributions_with_indent(result)

    def _leaf_multiplier(self):
        if self._main_leaf is None:
            return None
        main_duration = self._main_leaf.written_duration
        my_duration = abjad_inspect(self).duration()
        multiplier = main_duration / my_duration
        return multiplier
