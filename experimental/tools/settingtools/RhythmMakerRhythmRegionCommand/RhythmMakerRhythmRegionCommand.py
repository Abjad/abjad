from abjad.tools import beamtools
from abjad.tools import containertools
from abjad.tools import spannertools
from abjad.tools import timespantools
from experimental.tools.settingtools.FinalizedRhythmRegionCommand import FinalizedRhythmRegionCommand


class RhythmMakerRhythmRegionCommand(FinalizedRhythmRegionCommand):
    '''Rhythm-maker rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, 
        rhythm_maker=None, voice_name=None, rhythm_region_division_list=None, start_offset=None):
        self._rhythm_maker = rhythm_maker
        self._voice_name = voice_name
        self._rhythm_region_division_list = rhythm_region_division_list
        self._start_offset = start_offset

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

    def _get_payload(self, score_specification=None, voice_name=None):
        from experimental.tools import settingtools
        if self.rhythm_region_division_list:
            leaf_lists = self.rhythm_maker(self.rhythm_region_division_list.pairs)
            rhythm_containers = [containertools.Container(x) for x in leaf_lists]
            timespan = timespantools.Timespan(self.start_offset)
            rhythm_region_product = settingtools.RhythmRegionProduct(
                payload=rhythm_containers,
                voice_name=self.rhythm_region_division_list.voice_name,
                timespan=timespan)
            self._conditionally_beam_rhythm_containers(rhythm_containers)
            return rhythm_region_product

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def rhythm_maker(self):
        return self._rhythm_maker

    @property
    def rhythm_region_division_list(self):
        return self._rhythm_region_division_list

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def voice_name(self):
        return self._voice_name
