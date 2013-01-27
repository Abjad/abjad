from abjad.tools import beamtools
from abjad.tools import containertools
from abjad.tools import rhythmmakertools
from abjad.tools import spannertools
from abjad.tools import timespantools
from experimental.tools.expressiontools.RhythmRegionExpression import RhythmRegionExpression


class RhythmMakerRhythmRegionExpression(RhythmRegionExpression):
    '''Rhythm-maker rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, rhythm_maker=None, voice_name=None, start_offset=None, division_list=None):
        assert isinstance(rhythm_maker, rhythmmakertools.RhythmMaker), repr(rhythm_maker)
        self._rhythm_maker = rhythm_maker
        self._voice_name = voice_name
        self._start_offset = start_offset
        self._division_list = division_list

    ### PRIVATE METHODS ###

    def _conditionally_beam_rhythm_containers(self, rhythm_containers):
        if getattr(self.rhythm_maker, 'beam_cells_together', False):
            spannertools.destroy_spanners_attached_to_components_in_expr(rhythm_containers)
            durations = [x.prolated_duration for x in rhythm_containers]
            beamtools.DuratedComplexBeamSpanner(rhythm_containers, durations=durations, span=1)
        elif getattr(self.rhythm_maker, 'beam_each_cell', False):
            spannertools.destroy_spanners_attached_to_components_in_expr(rhythm_containers)
            for rhythm_container in rhythm_containers:
                beamtools.DuratedComplexBeamSpanner(
                    [rhythm_container], [rhythm_container.prolated_duration], span=1)

    def evaluate(self):
        from experimental.tools import expressiontools
        if not self.division_list:
            return
        leaf_lists = self.rhythm_maker(self.division_list.pairs)
        rhythm_containers = [containertools.Container(x) for x in leaf_lists]
        expression = expressiontools.StartPositionedRhythmPayloadExpression(
            payload=rhythm_containers, start_offset=self.start_offset)
        self._conditionally_beam_rhythm_containers(rhythm_containers)
        expression._voice_name = self.division_list.voice_name
        return expression

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def division_list(self):
        return self._division_list

    @property
    def rhythm_maker(self):
        return self._rhythm_maker

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def voice_name(self):
        return self._voice_name
