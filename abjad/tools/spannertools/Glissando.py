# -*- coding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools.inspect_ import inspect_


class Glissando(Spanner):
    r'''Glissando.

    ..  container:: example

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> glissando = spannertools.Glissando()
            >>> attach(glissando, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8 \glissando
                d'8 \glissando
                e'8 \glissando
                f'8
            }

    ..  container:: example

        Glissando avoids BendAfter indicators.

        ::

            >>> staff = Staff("c'8 d'8 e'8 f'8")
            >>> bend_after = indicatortools.BendAfter()
            >>> attach(bend_after, staff[1], is_annotation=True)
            >>> glissando = spannertools.Glissando()
            >>> attach(glissando, staff[:])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                c'8 \glissando
                d'8 - \bendAfter #'-4.0
                e'8 \glissando
                f'8
            }

    Formats notes and chords with LilyPond ``\glissando`` command.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_allow_repeated_pitches',
        '_allow_ties',
        '_parenthesize_repeated_pitches',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        allow_repeated_pitches=False,
        allow_ties=False,
        overrides=None,
        parenthesize_repeated_pitches=False,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        allow_ties = bool(allow_ties)
        allow_repeated_pitches = bool(allow_repeated_pitches)
        parenthesize_repeated_pitches = bool(parenthesize_repeated_pitches)
        self._allow_ties = allow_ties
        self._allow_repeated_pitches = allow_repeated_pitches
        self._parenthesize_repeated_pitches = parenthesize_repeated_pitches

    ### PRIVATE METHODS ###

    def _attachment_test_all(self, expr):
        return self._at_least_two_leaves(expr)

    def _copy_keyword_args(self, new):
        Spanner._copy_keyword_args(self, new)
        new._allow_repeated_pitches = self.allow_repeated_pitches
        new._allow_ties = self.allow_ties
        new._parenthesize_repeated_pitches = self.parenthesize_repeated_pitches

    def _get_annotations(self, leaf):
        inspector = inspect_(leaf)
        bend_after = None
        prototype = indicatortools.BendAfter
        if inspector.has_indicator(prototype):
            bend_after = inspector.get_indicator(prototype)
        return bend_after

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Chord, scoretools.Note)
        bend_after = self._get_annotations(leaf)
        should_attach_glissando = False
        if not self._is_my_first_leaf(leaf):
            if self.parenthesize_repeated_pitches:
                if not self._previous_leaf_changes_current_pitch(leaf):
                    self._parenthesize_leaf(leaf)
        if bend_after:
            lilypond_format_bundle.update(
                bend_after._get_lilypond_format_bundle(),
                )
        elif self._is_my_last_leaf(leaf):
            pass
        elif not isinstance(leaf, prototype):
            pass
        elif self.allow_repeated_pitches and self.allow_ties:
            should_attach_glissando = True
        elif self.allow_repeated_pitches and not self.allow_ties:
            should_attach_glissando = self._is_last_in_tie_chain(leaf)
        elif not self.allow_repeated_pitches and self.allow_ties:
            if self._next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif (
            not self.allow_repeated_pitches and
            not self.allow_ties):
            if self._next_leaf_changes_current_pitch(leaf):
                if self._is_last_in_tie_chain(leaf):
                    should_attach_glissando = True
        if should_attach_glissando:
            lilypond_format_bundle.right.spanner_starts.append('\glissando')
        return lilypond_format_bundle

    @staticmethod
    def _is_last_in_tie_chain(leaf):
        logical_tie = inspect_(leaf).get_logical_tie()
        return leaf is logical_tie[-1]

    @staticmethod
    def _next_leaf_changes_current_pitch(leaf):
        next_leaf = inspect_(leaf).get_leaf(n=1)
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
        previous_leaf = inspect_(leaf).get_leaf(n=-1)
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
    def allow_repeated_pitches(self):
        r'''Is true when glissando should allow repeated pitches.
        Otherwise false.

        ..  container:: example

            **Example 1.** Does not allow repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=False,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Allows repeated pitches (but not ties):

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Allows both repeated pitches and ties:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=True,
                ...     allow_ties=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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
        return self._allow_repeated_pitches

    @property
    def allow_ties(self):
        r'''Is true when glissando should allow ties. Otherwise false.

        ..  container:: example

            **Example 1.** Does not allow repeated pitches (including ties):

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=False,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Allows repeated pitches (but not ties):

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Allows both repeated pitches and ties:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=True,
                ...     allow_ties=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 1.** Does not parenthesize repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando()
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 2.** Spans and parenthesizes repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     allow_repeated_pitches=True,
                ...     parenthesize_repeated_pitches=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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

            **Example 3.** Parenthesizes (but does not span) repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     parenthesize_repeated_pitches=True,
                ...     )
                >>> attach(glissando, staff[:])
                >>> show(staff) # doctest: +SKIP

            ..  doctest::

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