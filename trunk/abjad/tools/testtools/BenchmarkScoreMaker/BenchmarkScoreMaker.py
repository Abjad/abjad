from abjad.tools import beamtools
from abjad.tools import contexttools
from abjad.tools import notetools
from abjad.tools import sequencetools
from abjad.tools import spannertools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.abctools import AbjadObject


class BenchmarkScoreMaker(AbjadObject):
    '''.. versionadded:: 2.12

    Benchmark score maker:

    ::

        >>> benchmark_score_maker = testtools.BenchmarkScoreMaker()

    ::

        >>> benchmark_score_maker
        BenchmarkScoreMaker()

    Use to instantiate scores for benchmark testing.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def make_score_00(self):
        '''Make 200-note voice (with nothing else).

        ::
        
            2.12 (r9710) initialization:        156,821 function calls
            2.12 (r9726) initialization:        156,827 function calls

            2.12 (r9703) LilyPond format:        99,127 function calls
            2.12 (r9710) LilyPond format:       100,126 function calls
            2.12 (r9726) LilyPond format:       105,778 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        return voice

    def make_context_mark_score_01(self):
        '''Make 200-note voice with dynamic mark on every 20th note:

        ::
    
            2.12 (r9704) initialization:        630,433 function calls
            2.12 (r9710) initialization:        235,120 function calls
            2.12 r(9726) initialization:        235,126 function calls

            2.12 (r9704) LilyPond format:       136,637 function calls
            2.12 (r9710) LilyPond format:        82,730 function calls
            2.12 (r9726) LilyPond format:        88,382 function calls
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(staff[:], [20], cyclic=True):
            contexttools.DynamicMark('f')(part[0])
        return staff

    def make_context_mark_score_02(self):
        '''Make 200-note staff with dynamic mark on every 4th note.
    
        ::

            2.12 (r9704) initialization:      4,632,761 function calls
            2.12 (r9710) initialization:        327,280 function calls
            2.12 (r9726) initialization:        325,371 function calls

            2.12 (r9704) LilyPond format:       220,277 function calls
            2.12 (r9710) LilyPond format:        84,530 function calls
            2.12 (r9726) LilyPond format:        90,056 function calls
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(staff[:], [4], cyclic=True):
            contexttools.DynamicMark('f')(part[0])
        return staff

    def make_context_mark_score_03(self):
        '''Make 200-note staff with dynamic mark on every note.
    
        ::

            2.12 (r9704) initialization:     53,450,195 function calls (!!)
            2.12 (r9710) initialization:      2,124,500 function calls
            2.12 (r9724) initialization:      2,122,591 function calls 

            2.12 (r9704) LilyPond format:       533,927 function calls
            2.12 (r9710) LilyPond format:        91,280 function calls
            2.12 (r9724) LilyPond format:        96,806 function calls
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for note in staff.leaves:
            contexttools.DynamicMark('f')(note)
        return staff

    def make_spanner_score_01(self):
        '''Make 200-note voice with durated complex beam spanner on every 4 notes.
    
        ::

            2.12 (r9710) initialization:        248,654 function calls
            2.12 (r9724) initialization:        248,660 function calls

            2.12 (r9703) LilyPond format:       425,848 function calls 
            2.12 (r9710) LilyPond format:       426,652 function calls
            2.12 (r9724) LilyPond format:       441,884 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_02(self):
        '''Make 200-note voice with durated complex beam spanner on every 20 notes.
    
        ::

            2.12 (r9710) initialization:        250,954 function calls
            2.12 (r9724) initialization:        248,717 function calls

            2.12 (r9703) LilyPond format:       495,768 function calls
            2.12 (r9710) LilyPond format:       496,572 function calls
            2.12 (r9724) LilyPond format:       511,471 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_03(self):
        '''Make 200-note voice with durated complex beam spanner on every 100 notes.
    
        ::

            2.12 (r9710) initialization:        251,606 function calls
            2.12 (r9724) initialization:        249,369 function calls

            2.12 (r9703) LilyPond format:       509,752 function calls
            2.12 (r9710) LilyPond format:       510,556 function calls
            2.12 (r9724) LilyPond format:       525,463 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_04(self):
        '''Make 200-note voice with slur spanner on every 4 notes.
    
        ::

            2.12 (r9724) initialization:        245,683 function calls 

            2.12 (r9703) LilyPond format:       125,577 function calls
            2.12 (r9724) LilyPond format:       111,341 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_05(self):
        '''Make 200-note voice with slur spanner on every 20 notes.
    
        ::

            2.12 (r9724) initialization:        248,567 function calls

            2.12 (r9703) LilyPond format:       122,177 function calls
            2.12 (r9724) LilyPond format:       107,486 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_06(self):
        '''Make 200-note voice with slur spanner on every 100 notes.
    
        ::

            2.12 (r9724) initialization:        249,339 function calls

            2.12 (r9703) LilyPond format:       121,497 function calls
            2.12 (r9724) LilyPond format:       106,718 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_07(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 4 notes.
    
        ::

            2.12 (r9724) initialization:        245,683 function calls

            2.12 (r9703) LilyPond format:       125,577 function calls
            2.12 (r9724) LilyPond format:       132,556 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice

    def make_spanner_score_08(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 20 notes.
    
        ::

            2.12 (r9724) initialization:        248,567 function calls

            2.12 (r9703) LilyPond format:       122,177 function calls
            2.12 (r9724) LilyPond format:       129,166 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice

    def make_spanner_score_09(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 100 notes.
    
        ::
            
            2.12 (r9724) initialization:        249,339 function calls

            2.12 (r9703) LilyPond format:       121,497 function calls
            2.12 (r9724) LilyPond format:       128,494 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice

    def make_hairpin_score_01(self):
        '''Make 200-note voice with crescendo spanner on every 4 notes.
    
        ::
            
            2.12 (r9726) initialization:        248,502 function calls

            2.12 (r9726) LilyPond format:       246,267 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            spannertools.CrescendoSpanner(part)
        return voice

    def make_hairpin_score_02(self):
        '''Make 200-note voice with crescendo spanner on every 20 notes.
    
        ::
            
            2.12 (r9726) initialization:        250,922 function calls

            2.12 (r9726) LilyPond format:       248,687 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            spannertools.CrescendoSpanner(part)
        return voice

    def make_hairpin_score_03(self):
        '''Make 200-note voice with crescendo spanner on every 100 notes.
    
        ::
            
            2.12 (r9726) initialization:        251,598 function calls

            2.12 (r9726) LilyPond format:       249,363 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            spannertools.CrescendoSpanner(part)
        return voice

    def make_bound_hairpin_score_01(self):
        '''Make 200-note voice with p-to-f bound crescendo spanner on every 4 notes.
    
        ::
            
            2.12 (r9726) initialization:        279,448 function calls

            2.12 (r9726) LilyPond format:       124,517 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            spannertools.CrescendoSpanner(part)
            contexttools.DynamicMark('p')(part[0])
            contexttools.DynamicMark('r')(part[-1])
        return voice

    def make_bound_hairpin_score_02(self):
        '''Make 200-note voice with p-to-f bound crescendo spanner on every 20 notes.
    
        ::
            
            2.12 (r9726) initialization:        268,845 function calls

            2.12 (r9726) LilyPond format:       117,846 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            spannertools.CrescendoSpanner(part)
            contexttools.DynamicMark('p')(part[0])
            contexttools.DynamicMark('r')(part[-1])
        return voice

    def make_bound_hairpin_score_03(self):
        '''Make 200-note voice with p-to-f bound crescendo spanner on every 100 notes.
    
        ::
            
            2.12 (r9726) initialization:        267,417 function calls

            2.12 (r9726) LilyPond format:       116,534 function calls
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            spannertools.CrescendoSpanner(part)
            contexttools.DynamicMark('p')(part[0])
            contexttools.DynamicMark('r')(part[-1])
        return voice
