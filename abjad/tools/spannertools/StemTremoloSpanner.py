# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.spannertools.Spanner import Spanner
from abjad.tools.topleveltools import inspect_


class StemTremoloSpanner(Spanner):
    r'''Stem tremolo spanner.

    ::

        >>> staff = Staff("c'32 d'16. e'8 f'4. g'4.")
        >>> tremolo_spanner = spannertools.StemTremoloSpanner()
        >>> attach(tremolo_spanner, staff[:])
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
        from abjad.tools import scoretools
        lilypond_format_bundle = self._get_basic_lilypond_format_bundle(leaf)
        prototype = (
            scoretools.Note,
            scoretools.Chord,
            )
        if not isinstance(leaf, prototype):
            return lilypond_format_bundle
        logical_tie = inspect_(leaf).get_logical_tie()
        if self.minimum_duration is not None and \
            logical_tie.get_duration() < self.minimum_duration:
            return lilypond_format_bundle
        flag_count = leaf.written_duration.flag_count
        tremolo_count = 32
        if flag_count:
            tremolo_count *= pow(2, flag_count)
        tremolo_string = ':{}'.format(tremolo_count)
        lilypond_format_bundle.right.stem_tremolos.append(tremolo_string)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_duration(self):
        r'''Gets minimum logical tie duration to which stem tremolos will be
        applied.

        Returns minimum duration.
        '''
        return self._minimum_duration
