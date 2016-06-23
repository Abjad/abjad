# -*- coding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class BenchmarkScoreMaker(AbjadObject):
    '''Benchmark score maker:

    ::

        >>> benchmark_score_maker = systemtools.BenchmarkScoreMaker()

    ::

        >>> benchmark_score_maker
        BenchmarkScoreMaker()

    Use to instantiate scores for benchmark testing.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Benchmarking'

    ### PUBLIC METHODS ###

    def make_bound_hairpin_score_01(self):
        r'''Make 200-note voice with p-to-f bound crescendo spanner
        on every 4 notes.

        ::

            2.12 (r9726) initialization:        279,448 function calls

            2.12 (r9726) LilyPond format:       124,517 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [4],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
            dynamic = indicatortools.Dynamic('p')
            topleveltools.attach(dynamic, part[0])
            dynamic = indicatortools.Dynamic('r')
            topleveltools.attach(dynamic, part[-1])
        return voice

    def make_bound_hairpin_score_02(self):
        r'''Make 200-note voice with p-to-f bound crescendo spanner
        on every 20 notes.

        ::

            2.12 (r9726) initialization:        268,845 function calls

            2.12 (r9726) LilyPond format:       117,846 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [20],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
            dynamic = indicatortools.Dynamic('p')
            topleveltools.attach(dynamic, part[0])
            dynamic = indicatortools.Dynamic('r')
            topleveltools.attach(dynamic, part[-1])
        return voice

    def make_bound_hairpin_score_03(self):
        r'''Make 200-note voice with p-to-f bound crescendo spanner
        on every 100 notes.

        ::

            2.12 (r9726) initialization:        267,417 function calls

            2.12 (r9726) LilyPond format:       116,534 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [100],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
            dynamic = indicatortools.Dynamic('p')
            topleveltools.attach(dynamic, part[0])
            dynamic = indicatortools.Dynamic('r')
            topleveltools.attach(dynamic, part[-1])
        return voice

    def make_hairpin_score_01(self):
        r'''Make 200-note voice with crescendo spanner on every 4 notes.

        ::

            2.12 (r9726) initialization:        248,502 function calls
            2.12 (r9728) initialization:        248,502 function calls

            2.12 (r9726) LilyPond format:       138,313 function calls
            2.12 (r9728) LilyPond format:       134,563 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [4],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
        return voice

    def make_hairpin_score_02(self):
        r'''Make 200-note voice with crescendo spanner on every 20 notes.

        ::

            2.12 (r9726) initialization:        248,687 function calls
            2.12 (r9728) initialization:        248,687 function calls

            2.12 (r9726) LilyPond format:       134,586 function calls
            2.12 (r9728) LilyPond format:       129,836 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [20],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
        return voice

    def make_hairpin_score_03(self):
        r'''Make 200-note voice with crescendo spanner on every 100 notes.

        ::

            2.12 (r9726) initialization:        249,363 function calls
            2.12 (r9726) initialization:        249,363 function calls

            2.12 (r9726) LilyPond format:       133,898 function calls
            2.12 (r9728) LilyPond format:       128,948 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [100],
            cyclic=True,
            ):
            crescendo = spannertools.Crescendo()
            topleveltools.attach(crescendo, part)
        return voice

    def make_score_00(self):
        r'''Make 200-note voice (with nothing else).

        ::

            2.12 (r9710) initialization:        156,821 function calls
            2.12 (r9726) initialization:        156,827 function calls

            2.12 (r9703) LilyPond format:        99,127 function calls
            2.12 (r9710) LilyPond format:       100,126 function calls
            2.12 (r9726) LilyPond format:       105,778 function calls

        '''
        from abjad.tools import scoretools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        return voice

    def make_score_with_indicators_01(self):
        r'''Make 200-note voice with dynamic on every 20th note:

        ::

            2.12 (r9704) initialization:        630,433 function calls
            2.12 (r9710) initialization:        235,120 function calls
            2.12 r(9726) initialization:        235,126 function calls

            2.12 (r9704) LilyPond format:       136,637 function calls
            2.12 (r9710) LilyPond format:        82,730 function calls
            2.12 (r9726) LilyPond format:        88,382 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import topleveltools
        staff = scoretools.Staff(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            staff[:],
            [20],
            cyclic=True,
            ):
            dynamic = indicatortools.Dynamic('f')
            topleveltools.attach(dynamic, part[0])
        return staff

    def make_score_with_indicators_02(self):
        r'''Make 200-note staff with dynamic on every 4th note.

        ::

            2.12 (r9704) initialization:      4,632,761 function calls
            2.12 (r9710) initialization:        327,280 function calls
            2.12 (r9726) initialization:        325,371 function calls

            2.12 (r9704) LilyPond format:       220,277 function calls
            2.12 (r9710) LilyPond format:        84,530 function calls
            2.12 (r9726) LilyPond format:        90,056 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import topleveltools
        staff = scoretools.Staff(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            staff[:],
            [4],
            cyclic=True,
            ):
            dynamic = indicatortools.Dynamic('f')
            topleveltools.attach(dynamic, part[0])
        return staff

    def make_score_with_indicators_03(self):
        r'''Make 200-note staff with dynamic on every note.

        ::

            2.12 (r9704) initialization:     53,450,195 function calls (!!)
            2.12 (r9710) initialization:      2,124,500 function calls
            2.12 (r9724) initialization:      2,122,591 function calls

            2.12 (r9704) LilyPond format:       533,927 function calls
            2.12 (r9710) LilyPond format:        91,280 function calls
            2.12 (r9724) LilyPond format:        96,806 function calls

        '''
        from abjad.tools import indicatortools
        from abjad.tools import scoretools
        from abjad.tools import topleveltools
        staff = scoretools.Staff(200 * scoretools.Note("c'16"))
        selector = topleveltools.select().by_leaf(flatten=True)
        for note in selector(staff):
            dynamic = indicatortools.Dynamic('f')
            topleveltools.attach(dynamic, note)
        return staff

    def make_spanner_score_01(self):
        r'''Make 200-note voice with durated complex beam spanner
        on every 4 notes.

        ::

            2.12 (r9710) initialization:        248,654 function calls
            2.12 (r9724) initialization:        248,660 function calls

            2.12 (r9703) LilyPond format:       425,848 function calls
            2.12 (r9710) LilyPond format:       426,652 function calls
            2.12 (r9724) LilyPond format:       441,884 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [4],
            cyclic=True,
            ):
            beam = spannertools.DuratedComplexBeam()
            topleveltools.attach(beam, part)
        return voice

    def make_spanner_score_02(self):
        r'''Make 200-note voice with durated complex beam spanner
        on every 20 notes.

        ::

            2.12 (r9710) initialization:        250,954 function calls
            2.12 (r9724) initialization:        248,717 function calls

            2.12 (r9703) LilyPond format:       495,768 function calls
            2.12 (r9710) LilyPond format:       496,572 function calls
            2.12 (r9724) LilyPond format:       511,471 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [20],
            cyclic=True,
            ):
            beam = spannertools.DuratedComplexBeam()
            topleveltools.attach(beam, part)
        return voice

    def make_spanner_score_03(self):
        r'''Make 200-note voice with durated complex beam spanner
        on every 100 notes.

        ::

            2.12 (r9710) initialization:        251,606 function calls
            2.12 (r9724) initialization:        249,369 function calls

            2.12 (r9703) LilyPond format:       509,752 function calls
            2.12 (r9710) LilyPond format:       510,556 function calls
            2.12 (r9724) LilyPond format:       525,463 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [100],
            cyclic=True,
            ):
            beam = spannertools.DuratedComplexBeam()
            topleveltools.attach(beam, part)
        return voice

    def make_spanner_score_04(self):
        r'''Make 200-note voice with slur spanner on every 4 notes.

        ::

            2.12 (r9724) initialization:        245,683 function calls

            2.12 (r9703) LilyPond format:       125,577 function calls
            2.12 (r9724) LilyPond format:       111,341 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [4],
            cyclic=True,
            ):
            slur = spannertools.Slur()
            topleveltools.attach(slur, part)
        return voice

    def make_spanner_score_05(self):
        r'''Make 200-note voice with slur spanner on every 20 notes.

        ::

            2.12 (r9724) initialization:        248,567 function calls

            2.12 (r9703) LilyPond format:       122,177 function calls
            2.12 (r9724) LilyPond format:       107,486 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [20],
            cyclic=True,
            ):
            slur = spannertools.Slur()
            topleveltools.attach(slur, part)
        return voice

    def make_spanner_score_06(self):
        r'''Make 200-note voice with slur spanner on every 100 notes.

        ::

            2.12 (r9724) initialization:        249,339 function calls

            2.12 (r9703) LilyPond format:       121,497 function calls
            2.12 (r9724) LilyPond format:       106,718 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [100],
            cyclic=True,
            ):
            slur = spannertools.Slur()
            topleveltools.attach(slur, part)
        return voice

    def make_spanner_score_07(self):
        r'''Make 200-note voice with (vanilla) beam spanner on every 4 notes.

        ::

            2.12 (r9724) initialization:        245,683 function calls

            2.12 (r9703) LilyPond format:       125,577 function calls
            2.12 (r9724) LilyPond format:       132,556 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [4],
            cyclic=True,
            ):
            beam = spannertools.Beam()
            topleveltools.attach(beam, part)
        return voice

    def make_spanner_score_08(self):
        r'''Make 200-note voice with (vanilla) beam spanner on every 20 notes.

        ::

            2.12 (r9724) initialization:        248,567 function calls

            2.12 (r9703) LilyPond format:       122,177 function calls
            2.12 (r9724) LilyPond format:       129,166 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [20],
            cyclic=True,
            ):
            beam = spannertools.Beam()
            topleveltools.attach(beam, part)
        return voice

    def make_spanner_score_09(self):
        r'''Make 200-note voice with (vanilla) beam spanner on every 100 notes.

        ::

            2.12 (r9724) initialization:        249,339 function calls

            2.12 (r9703) LilyPond format:       121,497 function calls
            2.12 (r9724) LilyPond format:       128,494 function calls

        '''
        from abjad.tools import scoretools
        from abjad.tools import sequencetools
        from abjad.tools import spannertools
        from abjad.tools import topleveltools
        voice = scoretools.Voice(200 * scoretools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(
            voice[:],
            [100],
            cyclic=True,
            ):
            beam = spannertools.Beam()
            topleveltools.attach(beam, part)
        return voice