# -*- encoding: utf-8 -*-
from abjad.tools import containertools
from abjad.tools import durationtools
from abjad.tools import rhythmmakertools
from abjad.tools import spannertools
from abjad.tools import timespantools
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
            spannertools.detach_spanners_attached_to_components_in_expr(
                rhythm_containers)
            durations = [x.duration for x in rhythm_containers]
            spannertools.DuratedComplexBeamSpanner(
                rhythm_containers, durations=durations, span=1)
        elif beam_each_cell:
            spannertools.detach_spanners_attached_to_components_in_expr(
                rhythm_containers)
            for rhythm_container in rhythm_containers:
                spannertools.DuratedComplexBeamSpanner(
                    [rhythm_container], [rhythm_container.duration], span=1)

    ### PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        r'''Rhythm-maker rhythm region expression division list.

        Return division list.
        '''
        return self._division_list

    ### PUBLIC METHODS ###

    def evaluate(self):
        r'''Evaluate rhythm-maker rhythm region expression.

        Return none when nonevaluable.

        Return start-positioned rhythm payload expression when evaluable.
        '''
        from experimental.tools import musicexpressiontools
        if not self.division_list:
            return
        leaf_lists = self.source_expression(self.division_list.pairs)
        rhythm_containers = [containertools.Container(x) for x in leaf_lists]
        expression = \
            musicexpressiontools.StartPositionedRhythmPayloadExpression(
            payload=rhythm_containers, start_offset=self.start_offset)
        self._beam_rhythm_containers(rhythm_containers)
        expression._voice_name = self.division_list.voice_name
        return expression
