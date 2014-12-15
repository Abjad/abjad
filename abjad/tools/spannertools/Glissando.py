# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools.inspect_ import inspect_


class Glissando(Spanner):
    r'''A glissando.

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

    Formats nonlast leaves in spanner with LilyPond ``\glissando`` command.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_repeated_pitches',
        '_include_tied_leaves',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        include_repeated_pitches=False,
        include_tied_leaves=False,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        assert isinstance(include_tied_leaves, bool), repr(include_tied_leaves)
        self._include_tied_leaves = include_tied_leaves
        assert isinstance(include_repeated_pitches, bool), repr(
            include_repeated_pitches)
        self._include_repeated_pitches = include_repeated_pitches

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Chord, scoretools.Note)
        should_attach_glissando = False
        if self._is_my_last_leaf(leaf):
            pass
        elif not isinstance(leaf, prototype):
            pass
        elif self.include_repeated_pitches and self.include_tied_leaves:
            should_attach_glissando = True
        elif self.include_repeated_pitches and not self.include_tied_leaves:
            should_attach_glissando = self._is_last_in_tie_chain(leaf)
        elif not self.include_repeated_pitches and self.include_tied_leaves:
            if self._next_leaf_changes_current_pitch(leaf):
                should_attach_glissando = True
        elif (
            not self.include_repeated_pitches and 
            not self.include_tied_leaves):
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

    ### PUBLIC PROPERTIES ###

    @property
    def include_repeated_pitches(self):
        r'''Is true when glissando should include repeated pitches.
        Otherwise false.

        ..  container:: example

            **Example 1.** Does not include repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=False,
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

            **Example 2.** Does include repeated pitches:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=True,
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

        Defaults to false.
        '''
        return self._include_repeated_pitches
        
    @property
    def include_tied_leaves(self):
        r'''Is true when glissando should include tied leaves.
        Otherwise false.

        ..  container:: example

            **Example 1.** Includes neither repeated pitches nor ties:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=False,
                ...     include_tied_leaves=False,
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

            **Example 2.** Same as above:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=False,
                ...     include_tied_leaves=True,
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

            Including ties is blocked when repeated pitches
            are not included (because ties all repeat a preceding pitch).

        ..  container:: example

            **Example 3.** Includes repeated pitches but not ties:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=True,
                ...     include_tied_leaves=False,
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

            **Example 4.** Includes both repeated pitches and ties:

            ::

                >>> staff = Staff("a8 a8 b8 ~ b8 c'8 c'8 d'8 ~ d'8")
                >>> glissando = Glissando(
                ...     include_repeated_pitches=True,
                ...     include_tied_leaves=True,
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

        Defaults to false.
        '''
        return self._include_tied_leaves