from abjad.system.AbjadObject import AbjadObject


class BenchmarkScoreMaker(AbjadObject):
    """
    Benchmark score-maker.

    ..  container:: example

        >>> benchmark_score_maker = abjad.BenchmarkScoreMaker()

        >>> benchmark_score_maker
        BenchmarkScoreMaker()

    Use to instantiate scores for benchmark testing.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Benchmarking'

    __slots__ = ()

    ### PUBLIC METHODS ###

    def make_bound_hairpin_score_01(self):
        """
        Make 200-note voice with p-to-f bound crescendo spanner
        on every 4 notes.

        2.12 (r9726) initialization:        279,448 function calls

        2.12 (r9726) LilyPond format:       124,517 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.Sequenc(voice[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
            dynamic = abjad.Dynamic('p')
            abjad.attach(dynamic, part[0])
            dynamic = abjad.Dynamic('r')
            abjad.attach(dynamic, part[-1])
        return voice

    def make_bound_hairpin_score_02(self):
        """
        Make 200-note voice with p-to-f bound crescendo spanner
        on every 20 notes.

        2.12 (r9726) initialization:        268,845 function calls

        2.12 (r9726) LilyPond format:       117,846 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
            dynamic = abjad.Dynamic('p')
            abjad.attach(dynamic, part[0])
            dynamic = abjad.Dynamic('r')
            abjad.attach(dynamic, part[-1])
        return voice

    def make_bound_hairpin_score_03(self):
        """
        Make 200-note voice with p-to-f bound crescendo spanner
        on every 100 notes.

        2.12 (r9726) initialization:        267,417 function calls

        2.12 (r9726) LilyPond format:       116,534 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [100],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
            dynamic = abjad.Dynamic('p')
            abjad.attach(dynamic, part[0])
            dynamic = abjad.Dynamic('r')
            abjad.attach(dynamic, part[-1])
        return voice

    def make_hairpin_score_01(self):
        """
        Make 200-note voice with crescendo spanner on every 4 notes.

        2.12 (r9726) initialization:        248,502 function calls
        2.12 (r9728) initialization:        248,502 function calls

        2.12 (r9726) LilyPond format:       138,313 function calls
        2.12 (r9728) LilyPond format:       134,563 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
        return voice

    def make_hairpin_score_02(self):
        """
        Make 200-note voice with crescendo spanner on every 20 notes.

        2.12 (r9726) initialization:        248,687 function calls
        2.12 (r9728) initialization:        248,687 function calls

        2.12 (r9726) LilyPond format:       134,586 function calls
        2.12 (r9728) LilyPond format:       129,836 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
        return voice

    def make_hairpin_score_03(self):
        """
        Make 200-note voice with crescendo spanner on every 100 notes.

        2.12 (r9726) initialization:        249,363 function calls
        2.12 (r9726) initialization:        249,363 function calls

        2.12 (r9726) LilyPond format:       133,898 function calls
        2.12 (r9728) LilyPond format:       128,948 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [100],
            cyclic=True,
            ):
            crescendo = abjad.Hairpin('<')
            abjad.attach(crescendo, part)
        return voice

    def make_score_00(self):
        """
        Make 200-note voice (with nothing else).

        2.12 (r9710) initialization:        156,821 function calls
        2.12 (r9726) initialization:        156,827 function calls

        2.12 (r9703) LilyPond format:        99,127 function calls
        2.12 (r9710) LilyPond format:       100,126 function calls
        2.12 (r9726) LilyPond format:       105,778 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        return voice

    def make_score_with_indicators_01(self):
        """
        Make 200-note voice with dynamic on every 20th note:

        2.12 (r9704) initialization:        630,433 function calls
        2.12 (r9710) initialization:        235,120 function calls
        2.12 r(9726) initialization:        235,126 function calls

        2.12 (r9704) LilyPond format:       136,637 function calls
        2.12 (r9710) LilyPond format:        82,730 function calls
        2.12 (r9726) LilyPond format:        88,382 function calls

        """
        import abjad
        staff = abjad.Staff(200 * abjad.Note("c'16"))
        for part in abjad.sequence(staff[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            dynamic = abjad.Dynamic('f')
            abjad.attach(dynamic, part[0])
        return staff

    def make_score_with_indicators_02(self):
        """
        Make 200-note staff with dynamic on every 4th note.

        2.12 (r9704) initialization:      4,632,761 function calls
        2.12 (r9710) initialization:        327,280 function calls
        2.12 (r9726) initialization:        325,371 function calls

        2.12 (r9704) LilyPond format:       220,277 function calls
        2.12 (r9710) LilyPond format:        84,530 function calls
        2.12 (r9726) LilyPond format:        90,056 function calls

        """
        import abjad
        staff = abjad.Staff(200 * abjad.Note("c'16"))
        for part in abjad.sequence(staff[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            dynamic = abjad.Dynamic('f')
            abjad.attach(dynamic, part[0])
        return staff

    def make_score_with_indicators_03(self):
        """
        Make 200-note staff with dynamic on every note.

        2.12 (r9704) initialization:     53,450,195 function calls (!!)
        2.12 (r9710) initialization:      2,124,500 function calls
        2.12 (r9724) initialization:      2,122,591 function calls

        2.12 (r9704) LilyPond format:       533,927 function calls
        2.12 (r9710) LilyPond format:        91,280 function calls
        2.12 (r9724) LilyPond format:        96,806 function calls

        """
        import abjad
        staff = abjad.Staff(200 * abjad.Note("c'16"))
        selector = abjad.select().leaves()
        for note in selector(staff):
            dynamic = abjad.Dynamic('f')
            abjad.attach(dynamic, note)
        return staff

    def make_spanner_score_01(self):
        """
        Make 200-note voice with durated complex beam spanner on every 4 notes.

        2.12 (r9710) initialization:        248,654 function calls
        2.12 (r9724) initialization:        248,660 function calls

        2.12 (r9703) LilyPond format:       425,848 function calls
        2.12 (r9710) LilyPond format:       426,652 function calls
        2.12 (r9724) LilyPond format:       441,884 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice

    def make_spanner_score_02(self):
        """
        Make 200-note voice with durated complex beam spanner
        on every 20 notes.

        2.12 (r9710) initialization:        250,954 function calls
        2.12 (r9724) initialization:        248,717 function calls

        2.12 (r9703) LilyPond format:       495,768 function calls
        2.12 (r9710) LilyPond format:       496,572 function calls
        2.12 (r9724) LilyPond format:       511,471 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice

    def make_spanner_score_03(self):
        """
        Make 200-note voice with durated complex beam spanner
        on every 100 notes.

        2.12 (r9710) initialization:        251,606 function calls
        2.12 (r9724) initialization:        249,369 function calls

        2.12 (r9703) LilyPond format:       509,752 function calls
        2.12 (r9710) LilyPond format:       510,556 function calls
        2.12 (r9724) LilyPond format:       525,463 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [100],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice

    def make_spanner_score_04(self):
        """
        Make 200-note voice with slur spanner on every 4 notes.

        2.12 (r9724) initialization:        245,683 function calls

        2.12 (r9703) LilyPond format:       125,577 function calls
        2.12 (r9724) LilyPond format:       111,341 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            slur = abjad.Slur()
            abjad.attach(slur, part)
        return voice

    def make_spanner_score_05(self):
        """
        Make 200-note voice with slur spanner on every 20 notes.

        2.12 (r9724) initialization:        248,567 function calls

        2.12 (r9703) LilyPond format:       122,177 function calls
        2.12 (r9724) LilyPond format:       107,486 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            slur = abjad.Slur()
            abjad.attach(slur, part)
        return voice

    def make_spanner_score_06(self):
        """
        Make 200-note voice with slur spanner on every 100 notes.

        2.12 (r9724) initialization:        249,339 function calls

        2.12 (r9703) LilyPond format:       121,497 function calls
        2.12 (r9724) LilyPond format:       106,718 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [100],
            cyclic=True,
            ):
            slur = abjad.Slur()
            abjad.attach(slur, part)
        return voice

    def make_spanner_score_07(self):
        """
        Make 200-note voice with (vanilla) beam spanner on every 4 notes.

        2.12 (r9724) initialization:        245,683 function calls

        2.12 (r9703) LilyPond format:       125,577 function calls
        2.12 (r9724) LilyPond format:       132,556 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [4],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice

    def make_spanner_score_08(self):
        """
        Make 200-note voice with (vanilla) beam spanner on every 20 notes.

        2.12 (r9724) initialization:        248,567 function calls

        2.12 (r9703) LilyPond format:       122,177 function calls
        2.12 (r9724) LilyPond format:       129,166 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [20],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice

    def make_spanner_score_09(self):
        """
        Make 200-note voice with (vanilla) beam spanner on every 100 notes.

        2.12 (r9724) initialization:        249,339 function calls

        2.12 (r9703) LilyPond format:       121,497 function calls
        2.12 (r9724) LilyPond format:       128,494 function calls

        """
        import abjad
        voice = abjad.Voice(200 * abjad.Note("c'16"))
        for part in abjad.sequence(voice[:]).partition_by_counts(
            [100],
            cyclic=True,
            ):
            beam = abjad.Beam()
            abjad.attach(beam, part)
        return voice
