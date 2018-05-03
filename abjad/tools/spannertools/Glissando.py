import typing
from abjad.tools.datastructuretools.OrderedDict import OrderedDict
from .Spanner import Spanner


class Glissando(Spanner):
    r'''Glissando.

    ..  container:: example

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> glissando = abjad.Glissando()
        >>> abjad.attach(glissando, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                d'8
                \glissando
                e'8
                \glissando
                f'8
            }

    ..  container:: example

        Glissando avoids bend-after indicators:

        >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
        >>> bend_after = abjad.BendAfter()
        >>> abjad.attach(bend_after, staff[1])
        >>> glissando = abjad.Glissando()
        >>> abjad.attach(glissando, staff[:])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'8
                \glissando
                d'8
                - \bendAfter #'-4.0
                e'8
                \glissando
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_repeats',
        '_allow_ties',
        '_parenthesize_repeats',
        '_stems',
        '_style',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_repeats: bool = None,
        allow_ties: bool = None,
        overrides: OrderedDict = None,
        parenthesize_repeats: bool = None,
        stems: bool = None,
        style: str = None,
        ) -> None:
        Spanner.__init__(self, overrides=overrides)
        if allow_repeats is not None:
            allow_repeats = bool(allow_repeats)
        self._allow_repeats = allow_repeats
        if allow_ties is not None:
            allow_ties = bool(allow_ties)
        self._allow_ties = allow_ties
        if parenthesize_repeats is not None:
            parenthesize_repeats = bool(parenthesize_repeats)
        self._parenthesize_repeats = parenthesize_repeats
        if stems is not None:
            stems = bool(stems)
        self._stems = stems
        if style is not None:
            assert isinstance(style, str), repr(style)
        self._style = style

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._allow_repeats = self.allow_repeats
        new._allow_ties = self.allow_ties
        new._parenthesize_repeats = self.parenthesize_repeats

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (abjad.Chord, abjad.Note)
        should_attach_glissando = False
        if leaf is not self[0]:
            if self.parenthesize_repeats:
                if not self._previous_leaf_changes_current_pitch(leaf):
                    self._parenthesize_leaf(leaf)
        tag = False
        if abjad.inspect(leaf).has_indicator(abjad.BendAfter):
            pass
        elif leaf is self[-1]:
            if self._right_broken:
                should_attach_glissando = True
                tag = True
        elif not isinstance(leaf, prototype):
            pass
        elif self.allow_repeats and self.allow_ties:
            should_attach_glissando = True
        elif self.allow_repeats and not self.allow_ties:
            should_attach_glissando = self._is_last_in_tie_chain(leaf)
        elif not self.allow_repeats and self.allow_ties:
            if self._next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif (not self.allow_repeats and not self.allow_ties):
            if self._next_leaf_changes_current_pitch(leaf):
                if self._is_last_in_tie_chain(leaf):
                    should_attach_glissando = True
        if should_attach_glissando:
            strings = [r'\glissando']
            if tag:
                strings = self._tag_show(strings)
            bundle.right.spanner_starts.extend(strings)
        if self.stems:
            if leaf is self[1]:
                strings = [
                    r'\override Accidental.stencil = ##f',
                    r'\override NoteColumn.glissando-skip = ##t',
                    r'\hide NoteHead',
                    r'\override NoteHead.no-ledgers = ##t',
                    ]
                bundle.grob_overrides.extend(strings)
            if leaf is self[-1]:
                strings = [
                    r'\revert Accidental.stencil',
                    r'\revert NoteColumn.glissando-skip',
                    r'\undo \hide NoteHead',
                    r'\revert NoteHead.no-ledgers',
                    ]
                if self._right_broken:
                    strings_ = self._tag_hide(strings)
                    bundle.grob_reverts.extend(strings_)
                    strings_ = self._tag_show(strings)
                    bundle.after.commands.extend(strings_)
                else:
                    bundle.grob_reverts.extend(strings)
        if self.style:
            if leaf is self[0]:
                string = rf"\override Glissando.style = #'{self.style}"
                bundle.grob_overrides.append(string)
            if leaf is self[-1]:
                string = rf"\revert Glissando.style"
                bundle.grob_reverts.append(string)
        return bundle

    @staticmethod
    def _is_last_in_tie_chain(leaf):
        import abjad
        logical_tie = abjad.inspect(leaf).get_logical_tie()
        return leaf is logical_tie[-1]

    @staticmethod
    def _next_leaf_changes_current_pitch(leaf):
        import abjad
        next_leaf = abjad.inspect(leaf).get_leaf(n=1)
        if (isinstance(leaf, abjad.Note) and
            isinstance(next_leaf, abjad.Note) and
            leaf.written_pitch == next_leaf.written_pitch):
            return False
        elif (isinstance(leaf, abjad.Chord) and
            isinstance(next_leaf, abjad.Chord) and
            leaf.written_pitches == next_leaf.written_pitches):
            return False
        return True

    @staticmethod
    def _parenthesize_leaf(leaf):
        import abjad
        if isinstance(leaf, abjad.Note):
            leaf.note_head.is_parenthesized = True
        elif isinstance(leaf, abjad.Chord):
            for note_head in leaf.note_heads:
                note_head.is_parenthesized = True

    @staticmethod
    def _previous_leaf_changes_current_pitch(leaf):
        import abjad
        previous_leaf = abjad.inspect(leaf).get_leaf(n=-1)
        if (isinstance(leaf, abjad.Note) and
            isinstance(previous_leaf, abjad.Note) and
            leaf.written_pitch == previous_leaf.written_pitch):
            return False
        elif (isinstance(leaf, abjad.Chord) and
            isinstance(previous_leaf, abjad.Chord) and
            leaf.written_pitches == previous_leaf.written_pitches):
            return False
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeats(self) -> typing.Optional[bool]:
        r'''Is true when glissando should allow repeated pitches.
        Otherwise false.

        ..  container:: example

            Does not allow repeated pitches:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=False,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Allows repeated pitches (but not ties):

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }

        ..  container:: example

            Allows both repeated pitches and ties:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=True,
            ...     allow_ties=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    \glissando
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    \glissando
                    d'8
                }

        Ties are excluded when repeated pitches are not allowed because all
        ties comprise repeated pitches.
        '''
        return self._allow_repeats

    @property
    def allow_ties(self) -> typing.Optional[bool]:
        r'''Is true when glissando should allow ties. Otherwise false.

        ..  container:: example

            Does not allow repeated pitches (including ties):

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=False,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Allows repeated pitches (but not ties):

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }

        ..  container:: example

            Allows both repeated pitches and ties:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=True,
            ...     allow_ties=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \glissando
                    a8
                    \glissando
                    b8
                    ~
                    \glissando
                    b8
                    \glissando
                    c'8
                    \glissando
                    c'8
                    \glissando
                    d'8
                    ~
                    \glissando
                    d'8
                }

        Ties are excluded when repeated pitches are not allowed because all
        ties comprise repeated pitches.
        '''
        return self._allow_ties

    def cross_segment_examples(self):
        r'''Cross-segment examples.

        ..  container:: example

            Cross-segment example #1 (one-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_1[-1:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    e'4
                    f'4
                %@% \glissando                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 a' b' r", name='MainVoice')
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    a'4
                    b'4
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            
            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \glissando                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        a'4
                        b'4
                        r4
                    }
                }

        ..  container:: example

            Cross-segment example #2 (one-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_1[-1:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    d'4
                    e'4
                    f'4
                %@% \glissando                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 a' b' r", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_2[:3])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    \glissando
                    a'4
                    \glissando
                    b'4
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            
            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        d'4
                        e'4
                        f'4
                        \glissando                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        \glissando
                        a'4
                        \glissando
                        b'4
                        r4
                    }
                }

        ..  container:: example

            Cross-segment example #3 (many-to-one):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_1[:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \glissando
                    d'4
                    \glissando
                    e'4
                    \glissando
                    f'4
                %@% \glissando                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 a' b' r", name='MainVoice')
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    a'4
                    b'4
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            
            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \glissando
                        d'4
                        \glissando
                        e'4
                        \glissando
                        f'4
                        \glissando                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        a'4
                        b'4
                        r4
                    }
                }

        ..  container:: example

            Cross-segment example #4 (many-to-many):

            >>> segment_1 = abjad.Voice("c'4 d' e' f'", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_1[:], right_broken=True)
            >>> abjad.show(segment_1, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_1, strict=50)
                \context Voice = "MainVoice"
                {
                    c'4
                    \glissando
                    d'4
                    \glissando
                    e'4
                    \glissando
                    f'4
                %@% \glissando                                    %! SHOW_TO_JOIN_BROKEN_SPANNERS
                }

            >>> segment_2 = abjad.Voice("g'4 a' b' r", name='MainVoice')
            >>> abjad.attach(abjad.Glissando(), segment_2[:3])
            >>> abjad.show(segment_2, strict=50) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(segment_2, strict=50)
                \context Voice = "MainVoice"
                {
                    g'4
                    \glissando
                    a'4
                    \glissando
                    b'4
                    r4
                }

            >>> container = abjad.Container([segment_1, segment_2])
            >>> text = format(container, 'lilypond')
            >>> text = abjad.LilyPondFormatManager.left_shift_tags(text, 50)
            >>> job = abjad.Job.join_broken_spanners(text)
            >>> text = job()
            >>> lines = text.split('\n')
            >>> lilypond_file = abjad.LilyPondFile.new(lines)
            >>> abjad.show(lilypond_file) # doctest: +SKIP
            
            ..  docs::

                >>> print(text)
                {
                    \context Voice = "MainVoice"
                    {
                        c'4
                        \glissando
                        d'4
                        \glissando
                        e'4
                        \glissando
                        f'4
                        \glissando                                %! SHOW_TO_JOIN_BROKEN_SPANNERS %@%
                    }
                    \context Voice = "MainVoice"
                    {
                        g'4
                        \glissando
                        a'4
                        \glissando
                        b'4
                        r4
                    }
                }

        '''
        pass

    @property
    def parenthesize_repeats(self) -> typing.Optional[bool]:
        r'''Is true when glissando should parenthesize repeated pitches.
        Otherwise false.

        ..  container:: example

            Does not parenthesize repeated pitches:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando()
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    a8
                    \glissando
                    b8
                    ~
                    b8
                    \glissando
                    c'8
                    c'8
                    \glissando
                    d'8
                    ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Spans and parenthesizes repeated pitches:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     allow_repeats=True,
            ...     parenthesize_repeats=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \glissando
                    \parenthesize
                    a8
                    \glissando
                    b8
                    ~
                    \parenthesize
                    b8
                    \glissando
                    c'8
                    \glissando
                    \parenthesize
                    c'8
                    \glissando
                    d'8
                    ~
                    \parenthesize
                    d'8
                }

        ..  container:: example

            Parenthesizes (but does not span) repeated pitches:

            >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
            >>> glissando = abjad.Glissando(
            ...     parenthesize_repeats=True,
            ...     )
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    a8
                    \parenthesize
                    a8
                    \glissando
                    b8
                    ~
                    \parenthesize
                    b8
                    \glissando
                    c'8
                    \parenthesize
                    c'8
                    \glissando
                    d'8
                    ~
                    \parenthesize
                    d'8
                }

        '''
        return self._parenthesize_repeats

    @property
    def stems(self) -> typing.Optional[bool]:
        r'''Is true when glissando formats stems-only timing marks non nonedge
        leaves.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> glissando = abjad.Glissando(stems=True)
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    c'8
                    \glissando
                    \hide NoteHead
                    \override Accidental.stencil = ##f
                    \override NoteColumn.glissando-skip = ##t
                    \override NoteHead.no-ledgers = ##t
                    d'8
                    \glissando
                    e'8
                    \glissando
                    \revert Accidental.stencil
                    \revert NoteColumn.glissando-skip
                    \revert NoteHead.no-ledgers
                    \undo \hide NoteHead
                    f'8
                }

        '''
        return self._stems

    @property
    def style(self) -> typing.Optional[str]:
        r'''Gets style.

        ..  container:: example

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> glissando = abjad.Glissando(style='trill')
            >>> abjad.attach(glissando, staff[:])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \override Glissando.style = #'trill
                    c'8
                    \glissando
                    d'8
                    \glissando
                    e'8
                    \glissando
                    \revert Glissando.style
                    f'8
                }

        '''
        return self._style
