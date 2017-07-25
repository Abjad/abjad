# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect


class StemTremoloSpanner(Spanner):
    r'''Stem tremolo spanner.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> staff = abjad.Staff("c'32 d'16. e'8 f'4. g'4.")
            >>> tremolo_spanner = abjad.StemTremoloSpanner()
            >>> abjad.attach(tremolo_spanner, staff[:])
            >>> f(staff)
            \new Staff {
                c'32 :256
                d'16. :128
                e'8 :64
                f'4. :32
                g'4. :32
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_minimum_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        minimum_duration=None,
        overrides=None,
        ):
        Spanner.__init__(
            self,
            overrides=overrides,
            )
        if minimum_duration is not None:
            minimum_duration = durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        new._minimum_duration = self.minimum_duration

    def _get_lilypond_format_bundle(self, leaf):
        import abjad
        bundle = self._get_basic_lilypond_format_bundle(leaf)
        if not isinstance(leaf, (abjad.Chord, abjad.Note)):
            return bundle
        logical_tie = abjad.inspect(leaf).get_logical_tie()
        if (self.minimum_duration is not None and
            logical_tie.get_duration() < self.minimum_duration):
            return bundle
        flag_count = leaf.written_duration.flag_count
        tremolo_count = 32
        if flag_count:
            tremolo_count *= pow(2, flag_count)
        tremolo_string = ':{}'.format(tremolo_count)
        bundle.right.stem_tremolos.append(tremolo_string)
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_duration(self):
        r'''Gets minimum logical tie duration to which stem tremolos will be
        applied.

        Returns minimum duration.
        '''
        return self._minimum_duration
