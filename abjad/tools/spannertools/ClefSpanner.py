# -*- encoding: utf-8 -*-
from abjad.tools import indicatortools
from abjad.tools import scoretools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class ClefSpanner(Spanner):
    r'''Clef spanner.

    ..  container:: example

        **Example 1.** Attaches percussion clef spanner to notes in middle of
        staff:

        ::

            >>> staff = Staff("c' d' e' f' g' a' b' c''")
            >>> clef = Clef('treble')
            >>> attach(clef, staff[0])
            >>> clef_spanner = spannertools.ClefSpanner('percussion')
            >>> attach(clef_spanner, staff[2:-2])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \clef "treble"
                c'4
                d'4
                \clef "percussion"
                e'4
                f'4
                g'4
                a'4
                \clef "treble"
                b'4
                c''4
            }

    ..  container:: example

        **Example 2.** Attaches two clef spanners to notes in middle of staff.
        Only the first clef spanner formats a new clef:

        ::

            >>> staff = Staff("r4 c'4 d'4 r4 e'4 f'4 r4")
            >>> clef = Clef('treble')
            >>> attach(clef, staff[0])
            >>> clef_spanner = spannertools.ClefSpanner('percussion')
            >>> attach(clef_spanner, staff[1:3])
            >>> clef_spanner = spannertools.ClefSpanner('percussion')
            >>> attach(clef_spanner, staff[4:6])
            >>> show(staff) # doctest: +SKIP

        ..  doctest::

            >>> print(format(staff))
            \new Staff {
                \clef "treble"
                r4
                \clef "percussion"
                c'4
                d'4
                r4
                e'4
                f'4
                \clef "treble"
                r4
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_clef',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        clef='percussion',
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        clef = indicatortools.Clef(clef)
        self._clef = clef

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        r'''Gets new arguments of spanner.

        Returns empty tuple.
        '''
        return (
            self.clef,
            )

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._clef = self.clef

    def _get_lilypond_format_bundle(self, leaf):
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (scoretools.Note, scoretools.Chord, type(None))
        first_leaf = self._get_leaves()[0]
        current_clef = inspect_(first_leaf).get_effective(indicatortools.Clef)
        set_clef = False
        reset_clef = False
        if self._is_my_only_leaf(leaf):
            if self.clef != current_clef:
                set_clef = True
                reset_clef = True

            previous_leaf = inspect_(leaf).get_leaf(-1)
            while not isinstance(previous_leaf, prototype):
                previous_leaf = inspect_(previous_leaf).get_leaf(-1)
            if previous_leaf is not None:
                spanners = inspect_(previous_leaf).get_spanners(type(self))
                spanners = tuple(spanners)
                if spanners:
                    if spanners[0].clef == self.clef:
                        set_clef = False
            next_leaf = inspect_(leaf).get_leaf(1)
            while not isinstance(next_leaf, prototype):
                next_leaf = inspect_(next_leaf).get_leaf(1)
            if next_leaf is not None:
                spanners = inspect_(next_leaf).get_spanners(type(self))
                spanners = tuple(spanners)
                if spanners:
                    if spanners[0].clef == self.clef:
                        reset_clef = False
        elif self._is_my_first_leaf(leaf):
            if self.clef != current_clef:
                set_clef = True
            previous_leaf = inspect_(leaf).get_leaf(-1)
            while not isinstance(previous_leaf, prototype):
                previous_leaf = inspect_(previous_leaf).get_leaf(-1)
            if previous_leaf is not None:
                spanners = inspect_(previous_leaf).get_spanners(type(self))
                spanners = tuple(spanners)
                if spanners:
                    if spanners[0].clef == self.clef:
                        set_clef = False
        elif self._is_my_last_leaf(leaf):
            if self.clef != current_clef and current_clef is not None:
                reset_clef = True

            next_leaf = inspect_(leaf).get_leaf(1)
            while not isinstance(next_leaf, prototype):
                next_leaf = inspect_(next_leaf).get_leaf(1)
            if next_leaf is not None:
                spanners = inspect_(next_leaf).get_spanners(type(self))
                spanners = tuple(spanners)
                if spanners:
                    if spanners[0].clef == self.clef:
                        reset_clef = False
        if set_clef:
            string = format(self.clef, 'lilypond')
            lilypond_format_bundle.before.indicators.append(string)
        if reset_clef and current_clef is not None:
            string = format(current_clef, 'lilypond')
            lilypond_format_bundle.after.indicators.append(string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def clef(self):
        r'''Gets clef.

        Set to clef or clef name.

        Defaults to ``'percussion'``.

        Returns clef.
        '''
        return self._clef
