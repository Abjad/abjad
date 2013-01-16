from abjad.tools import timerelationtools
from abjad.tools import timespantools
from abjad.tools import wellformednesstools
from experimental.tools.settingtools.FinalizedRhythmRegionCommand import FinalizedRhythmRegionCommand


class SelectorRhythmRegionCommand(FinalizedRhythmRegionCommand):
    '''Selector rhythm region command.
    '''

    ### INITIALIZER ###

    def __init__(self, selector=None, total_duration=None, voice_name=None, start_offset=None):
        self._selector = selector
        self._total_duration = total_duration
        self._voice_name = voice_name
        self._start_offset = start_offset

    ### PRIVATE METHODS ###

    def _get_payload(self, score_specification, voice_name, start_offset=None, stop_offset=None):
        from experimental.tools import settingtools
        assert voice_name == self.voice_name
        assert start_offset is not None, repr(start_offset)
        assert stop_offset is not None, repr(stop_offset)
        anchor_timespan = score_specification.get_anchor_timespan(self, voice_name)
        voice_proxy = score_specification.contexts[voice_name]
        rhythm_region_products = voice_proxy.rhythm_region_products
        time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
        rhythm_region_products = rhythm_region_products.get_timespans_that_satisfy_time_relation(time_relation)
        if not rhythm_region_products:
            return
        rhythm_region_products = copy.deepcopy(rhythm_region_products)
        rhythm_region_products = timespantools.TimespanInventory(rhythm_region_products)
        rhythm_region_products.sort()
        assert anchor_timespan.is_well_formed, repr(anchor_timespan)
        rhythm_region_products = rhythm_region_products & anchor_timespan
        result = settingtools.RhythmRegionProduct(voice_name=voice_name, start_offset=start_offset)
        for rhythm_region_product in rhythm_region_products:
            result.payload.extend(rhythm_region_product.payload)
        assert wellformednesstools.is_well_formed_component(result.payload)
        result, new_start_offset = self._apply_payload_callbacks(result, result.start_offset)
        assert isinstance(result, settingtools.RhythmRegionProduct), repr(result)
        keep_timespan = timespantools.Timespan(start_offset, stop_offset)
        assert not keep_timespan.starts_before_timespan_starts(result.timespan), repr((result.timespan, keep_timespan))
        assert result.timespan.start_offset == keep_timespan.start_offset, repr((result.timespan, keep_timespan))
        result = result & keep_timespan
        assert isinstance(result, timespantools.TimespanInventory), repr(result)
        assert len(result) == 1
        result = result[0]
        assert isinstance(result, settingtools.RhythmRegionProduct), repr(result)
        result.repeat_to_stop_offset(stop_offset)
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def selector(self):
        return self._selector

    @property
    def start_offset(self):
        return self._start_offset

    @property
    def total_duration(self):
        return self._total_duration

    @property
    def voice_name(self):
        return self._voice_name
