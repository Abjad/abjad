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

    def make_context_mark_score_01(self):
        '''Make 200-note voice with dynamic mark on every 20th note.
    
        2.12 (r9704) initialization:        630,433 function calls
        2.12 (r9704) LilyPond format:       136,637 function calls.
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(staff[:], [20], cyclic=True):
            contexttools.DynamicMark('f')(part[0])
        return staff

    def make_context_mark_score_02(self):
        '''Make 200-note staff with dynamic mark on every 4th note.
    
        2.12 (r9704) initialization:        4,632,761 function calls
        2.12 (r9704) format performance:      220,277 function calls
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(staff[:], [4], cyclic=True):
            contexttools.DynamicMark('f')(part[0])
        return staff

    def make_context_mark_score_03(self):
        '''Make 200-note staff with dynamic mark on every note.
    
        2.12 (r9704) initialization:    53,450,195 function calls (!!)
        2.12 (r9704) LilyPond format:      533,927 function calls
        '''
        staff = stafftools.Staff(200 * notetools.Note("c'16"))
        for note in staff.leaves:
            contexttools.DynamicMark('f')(note)
        return staff

    def make_spanner_score_00(self):
        '''Make 200-note voice with no spanners.
        
        2.12 (r9703) format performance: 99,127 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        return voice

    def make_spanner_score_01(self):
        '''Make 200-note voice with durated complex beam spanner on every 4 notes.
    
        2.12 (r9703) format performance: 425,848 function calls. 
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_02(self):
        '''Make 200-note voice with durated complex beam spanner on every 20 notes.
    
        2.12 (r9703) format performance: 495,768 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_03(self):
        '''Make 200-note voice with durated complex beam spanner on every 100 notes.
    
        2.12 (r9703) format performance: 509,752 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            beamtools.DuratedComplexBeamSpanner(part)
        return voice

    def make_spanner_score_04(self):
        '''Make 200-note voice with slur spanner on every 4 notes.
    
        2.12 (r9703) format performance: 125,577 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_05(self):
        '''Make 200-note voice with slur spanner on every 20 notes.
    
        2.12 (r9703) format performance: 122,177 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_06(self):
        '''Make 200-note voice with slur spanner on every 100 notes.
    
        2.12 (r9703) format performance: 121,497 function calls.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            spannertools.SlurSpanner(part)
        return voice

    def make_spanner_score_07(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 4 notes.
    
        2.12 (r9703) format performance: 125,577.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [4], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice

    def make_spanner_score_08(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 20 notes.
    
        2.12 (r9703) format performance: 122,177.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [20], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice

    def make_spanner_score_09(self):
        '''Make 200-note voice with (vanilla) beam spanner on every 100 notes.
    
        2.12 (r9703) format performance: 121,497.
        '''
        voice = voicetools.Voice(200 * notetools.Note("c'16"))
        for part in sequencetools.partition_sequence_by_counts(voice[:], [100], cyclic=True):
            beamtools.BeamSpanner(part)
        return voice
