from .StorageFormatManager import StorageFormatManager


class BenchmarkScoreMaker(object):
    """
    Benchmark score-maker.

    ..  container:: example

        >>> benchmark_score_maker = abjad.BenchmarkScoreMaker()

        >>> benchmark_score_maker
        BenchmarkScoreMaker()

    Use to instantiate scores for benchmark testing.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = "Benchmarking"

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PUBLIC METHODS ###

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
        for part in abjad.sequence(staff[:]).partition_by_counts([20], cyclic=True):
            dynamic = abjad.Dynamic("f")
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
        for part in abjad.sequence(staff[:]).partition_by_counts([4], cyclic=True):
            dynamic = abjad.Dynamic("f")
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
            dynamic = abjad.Dynamic("f")
            abjad.attach(dynamic, note)
        return staff
