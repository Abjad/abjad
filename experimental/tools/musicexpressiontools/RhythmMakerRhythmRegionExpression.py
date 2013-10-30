# -*- encoding: utf-8 -*-
from abjad.tools import scoretools
from abjad.tools import durationtools
from abjad.tools import iterationtools
from abjad.tools import rhythmmakertools
from abjad.tools import spannertools
from abjad.tools import timespantools
from abjad.tools.scoretools import attach
from experimental.tools.musicexpressiontools.RhythmRegionExpression import \
    RhythmRegionExpression
    


class RhythmMakerRhythmRegionExpression(RhythmRegionExpression):
    r'''Rhythm-maker rhythm region expression.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        source_expression=None, 
        division_list=None, 
        start_offset=None, 
        voice_name=None,
        ):   
        from experimental.tools import musicexpressiontools
        assert isinstance(source_expression, rhythmmakertools.RhythmMaker)
        assert isinstance(division_list, musicexpressiontools.DivisionList)
        RhythmRegionExpression.__init__(
            self, 
            source_expression=source_expression, 
            start_offset=start_offset,
            total_duration=division_list.duration, 
            voice_name=voice_name,
            )
        self._division_list = division_list

    ### PRIVATE METHODS ###

    def _beam_rhythm_containers(self, rhythm_containers):
        beam_cells_together = getattr(
            self.source_expression, 'beam_cells_together', False)
        beam_each_cell = getattr(
            self.source_expression, 'beam_each_cell', False)
        if beam_cells_together:
            for container in iterationtools.iterate_components_in_expr(
                rhythm_containers):
                spanners = container._get_spanners()
                for spanner in spanners:
                    spanner.detach()
            durations = [x._get_duration() for x in rhythm_containers]
            beam = spannertools.DuratedComplexBeamSpanner(
                durations=durations, 
                span=1,
                )
            attach(beam, rhythm_containers)
        elif beam_each_cell:
            for container in iterationtools.iterate_components_in_expr(
                rhythm_containers):
                spanners = container._get_spanners()
                for spanner in spanners:
                    spanner.detach()
            for rhythm_container in rhythm_containers:
                beam = spannertools.DuratedComplexBeamSpanner(
                    durations=[rhythm_container._get_duration()], 
                    span=1,
                    )
                attach(beam, rhythm_container) 

    ### PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        r'''Rhythm-maker rhythm region expression division list.

        Returns division list.
        '''
        return self._division_list

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate rhythm-maker rhythm region expression.

        Returns none when nonevaluable.

        Returns start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        if not self.division_list:
            return
        leaf_lists = self.source_expression(self.division_list.pairs)
        rhythm_containers = [scoretools.Container(x) for x in leaf_lists]
        expression = \
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
            payload=rhythm_containers, start_offset=self.start_offset)
        self._beam_rhythm_containers(rhythm_containers)
        expression._voice_name = self.division_list.voice_name
        return expression
