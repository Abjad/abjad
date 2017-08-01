# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner


class Glissando(Spanner):
    r'''Glissando.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> glissando = abjad.Glissando()
            >>> abjad.attach(glissando, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8 \glissando
                d'8 \glissando
                e'8 \glissando
                f'8
            }

    ..  container:: example

        Glissando avoids bend-after indicators:

        ::

            >>> staff = abjad.Staff("c'8 d'8 e'8 f'8")
            >>> bend_after = abjad.BendAfter()
            >>> abjad.attach(bend_after, staff[1])
            >>> glissando = abjad.Glissando()
            >>> abjad.attach(glissando, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  docs::

            >>> f(staff)
            \new Staff {
                c'8 \glissando
                d'8 - \bendAfter #'-4.0
                e'8 \glissando
                f'8
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_repeat_pitches',
        '_allow_ties',
        '_parenthesize_repeated_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_repeat_pitches=False,
        allow_ties=False,
        overrides=None,
        parenthesize_repeated_pitches=False,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        allow_ties = bool(allow_ties)
        allow_repeat_pitches = bool(allow_repeat_pitches)
        parenthesize_repeated_pitches = bool(parenthesize_repeated_pitches)
        self._allow_ties = allow_ties
        self._allow_repeat_pitches = allow_repeat_pitches
        self._parenthesize_repeated_pitches = parenthesize_repeated_pitches

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, argument):
        return self._at_least_two_leaves(argument)

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._allow_repeat_pitches = self.allow_repeat_pitches
        new._allow_ties = self.allow_ties
        new._parenthesize_repeated_pitches = self.parenthesize_repeated_pitches

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Chord, scoretools.Note)
        should_attach_glissando = False
        if not self._is_my_first_leaf(leaf):
            if self.parenthesize_repeated_pitches:
                if not self._previous_leaf_changes_current_pitch(leaf):
                    self._parenthesize_leaf(leaf)
        if abjad.inspect(leaf).has_indicator(abjad.BendAfter):
            pass
        elif self._is_my_last_leaf(leaf):
            pass
        elif not isinstance(leaf, prototype):
            pass
        elif self.allow_repeat_pitches and self.allow_ties:
            should_attach_glissando = True
        elif self.allow_repeat_pitches and not self.allow_ties:
            should_attach_glissando = self._is_last_in_tie_chain(leaf)
        elif not self.allow_repeat_pitches and self.allow_ties:
            if self._next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif (
            not self.allow_repeat_pitches and
            not self.allow_ties):
            if self._next_leaf_changes_current_pitch(leaf):
                if self._is_last_in_tie_chain(leaf):
                    should_attach_glissando = True
        if should_attach_glissando:
            bundle.right.spanner_starts.append('\glissando')
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
        if (isinstance(leaf, scoretools.Note) and
            isinstance(next_leaf, scoretools.Note) and
            leaf.written_pitch == next_leaf.written_pitch):
            return False
        elif (isinstance(leaf, scoretools.Chord) and
            isinstance(next_leaf, scoretools.Chord) and
            leaf.written_pitches == next_leaf.written_pitches):
            return False
        return True

    @staticmethod
    def _parenthesize_leaf(leaf):
        if isinstance(leaf, scoretools.Note):
            leaf.note_head.is_parenthesized = True
        elif isinstance(leaf, scoretools.Chord):
            for note_head in leaf.note_heads:
                note_head.is_parenthesized = True

    @staticmethod
    def _previous_leaf_changes_current_pitch(leaf):
        import abjad
        previous_leaf = abjad.inspect(leaf).get_leaf(n=-1)
        if (isinstance(leaf, scoretools.Note) and
            isinstance(previous_leaf, scoretools.Note) and
            leaf.written_pitch == previous_leaf.written_pitch):
            return False
        elif (isinstance(leaf, scoretools.Chord) and
            isinstance(previous_leaf, scoretools.Chord) and
            leaf.written_pitches == previous_leaf.written_pitches):
            return False
        return True

    ### PUBLIC PROPERTIES ###

    @property
    def allow_repeat_pitches(self):
        r'''Is true when glissando should allow repeated pitches.
        Otherwise false.

        ..  container:: example

            Does not allow repeated pitches:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=False,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8
                    a8 \glissando
                    b8 ~
                    b8 \glissando
                    c'8
                    c'8 \glissando
                    d'8 ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Allows repeated pitches (but not ties):

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8 \glissando
                    a8 \glissando
                    b8 ~
                    b8 \glissando
                    c'8 \glissando
                    c'8 \glissando
                    d'8 ~
                    d'8
                }

        ..  container:: example

            Allows both repeated pitches and ties:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=True,
                ...     allow_ties=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8 \glissando
                    a8 \glissando
                    b8 ~ \glissando
                    b8 \glissando
                    c'8 \glissando
                    c'8 \glissando
                    d'8 ~ \glissando
                    d'8
                }

        Ties are excluded when repeated pitches are not allowed because all
        ties comprise repeated pitches.

        Defaults to false.
        '''
        return self._allow_repeat_pitches

    @property
    def allow_ties(self):
        r'''Is true when glissando should allow ties. Otherwise false.

        ..  container:: example

            Does not allow repeated pitches (including ties):

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=False,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8
                    a8 \glissando
                    b8 ~
                    b8 \glissando
                    c'8
                    c'8 \glissando
                    d'8 ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Allows repeated pitches (but not ties):

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8 \glissando
                    a8 \glissando
                    b8 ~
                    b8 \glissando
                    c'8 \glissando
                    c'8 \glissando
                    d'8 ~
                    d'8
                }

        ..  container:: example

            Allows both repeated pitches and ties:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=True,
                ...     allow_ties=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8 \glissando
                    a8 \glissando
                    b8 ~ \glissando
                    b8 \glissando
                    c'8 \glissando
                    c'8 \glissando
                    d'8 ~ \glissando
                    d'8
                }

        Ties are excluded when repeated pitches are not allowed because all
        ties comprise repeated pitches.

        Defaults to false.
        '''
        return self._allow_ties

    @property
    def parenthesize_repeated_pitches(self):
        r'''Is true when glissando should parenthesize repeated pitches.
        Otherwise false.

        ..  container:: example

            Does not parenthesize repeated pitches:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando()
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8
                    a8 \glissando
                    b8 ~
                    b8 \glissando
                    c'8
                    c'8 \glissando
                    d'8 ~
                    d'8
                }

            This is default behavior.

        ..  container:: example

            Spans and parenthesizes repeated pitches:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     allow_repeat_pitches=True,
                ...     parenthesize_repeated_pitches=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8 \glissando
                    \parenthesize
                    a8 \glissando
                    b8 ~
                    \parenthesize
                    b8 \glissando
                    c'8 \glissando
                    \parenthesize
                    c'8 \glissando
                    d'8 ~
                    \parenthesize
                    d'8
                }

        ..  container:: example

            Parenthesizes (but does not span) repeated pitches:

            ::

                >>> staff = abjad.Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = abjad.Glissando(
                ...     parenthesize_repeated_pitches=True,
                ...     )
                >>> abjad.attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    a8
                    \parenthesize
                    a8 \glissando
                    b8 ~
                    \parenthesize
                    b8 \glissando
                    c'8
                    \parenthesize
                    c'8 \glissando
                    d'8 ~
                    \parenthesize
                    d'8
                }

        Defaults to false.
        '''
        return self._parenthesize_repeated_pitches
