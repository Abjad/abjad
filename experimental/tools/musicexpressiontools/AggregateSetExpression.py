# -*- encoding: utf-8 -*-
from abjad.tools import instrumenttools
from abjad.tools import pitchtools
from abjad.tools import scoretools
from abjad.tools.topleveltools import inspect_
from experimental.tools.musicexpressiontools.LeafSetExpression \
    import LeafSetExpression



class AggregateSetExpression(LeafSetExpression):
    r'''Aggregate set expression.
    '''

    ### PUBLIC METHODS ###

    def execute_against_score(self, score):
        r'''Execute aggregate set expression against `score`.
        '''
        aggregate = self.source_expression.payload
        for leaf in self._iterate_selected_leaves_in_score(score):
            assert isinstance(leaf, scoretools.Note), repr(leaf)
            sounding_pitch = inspect_(leaf).get_sounding_pitch()
            sounding_pitches = \
                pitchtools.register_pitch_class_numbers_by_pitch_number_aggregate(
                [sounding_pitch.pitch_number], aggregate)
            #leaf.sounding_pitch = sounding_pitches[0]
            instrument = leaf._get_effective(instrumenttools.Instrument)
            if instrument:
                reference_pitch = instrument.sounding_pitch_of_written_middle_c
            else:
                reference_pitch = pitchtools.NamedPitch('C4')
            t_n = reference_pitch - pitchtools.NamedPitch('C4')
            sounding_pitch = sounding_pitches[0]
            written_pitch = pitchtools.transpose_pitch_carrier_by_interval(
                sounding_pitch, t_n)
            leaf.written_pitch = written_pitch
            assert inspect_(leaf).get_sounding_pitch() == sounding_pitch
