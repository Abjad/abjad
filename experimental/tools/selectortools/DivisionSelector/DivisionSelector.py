import copy
from abjad.tools import durationtools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools.selectortools.Selector import Selector


class DivisionSelector(Selector):
    r'''Division selector:

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` divisions that start during score::

        >>> selector = score_specification.interface.select_divisions('Voice 1')

    ::
        
        >>> z(selector)
        selectortools.DivisionSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` divisions that start during segment ``'red'``::

        >>> selector = red_segment.select_divisions('Voice 1')

    ::

        >>> z(selector)
        selectortools.DivisionSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Division selectors are immutable.
    '''
    
    ### PRIVATE METHODS ###

    # TODO: migrate in self._get_timespan_and_payload
    def _get_payload(self, score_specification, voice_name=None):
        from experimental.tools import settingtools
        # ignore voice_name input parameter
        voice_name = None
        anchor_timespan = score_specification.get_anchor_timespan(self, self.voice_name)
        voice_proxy = score_specification.contexts[self.voice_name]
        division_region_products = voice_proxy.division_region_products
        timespan_time_relation = timerelationtools.timespan_2_intersects_timespan_1(
            timespan_1=anchor_timespan)
        division_region_products = division_region_products.get_timespans_that_satisfy_time_relation(
            timespan_time_relation)
        division_region_products = timespantools.TimespanInventory(division_region_products)
        if not division_region_products:
            return
        if not division_region_products.all_are_contiguous:
            return
        trimmed_division_region_products = copy.deepcopy(division_region_products)
        trimmed_division_region_products = timespantools.TimespanInventory(
            trimmed_division_region_products)
        trimmed_division_region_products = trimmed_division_region_products & anchor_timespan
        trimmed_division_region_products.sort() 
        assert trimmed_division_region_products.all_are_contiguous
        trimmed_division_region_products = trimmed_division_region_products.compute_logical_or()
        assert len(trimmed_division_region_products) == 1
        final_expression = trimmed_division_region_products[0]
        divisions = trimmed_division_region_products[0].payload.divisions
        start_offset = trimmed_division_region_products[0].timespan.start_offset
        divisions, start_offset = self._apply_payload_callbacks(divisions, start_offset)
        result = settingtools.DivisionRegionProduct(
            divisions, 
            voice_name=final_expression.voice_name,
            start_offset=start_offset
            )
        #self._debug(result, 'old-fashioned payload')
        return result

    # TODO: migrate in self._get_timespan_and_payload()
    def _get_timespan(self, score_specification, voice_name=None):
        # ignore voice_name input parameter
        voice_name = None
        voice_division_list = score_specification.contexts[self.voice_name].voice_division_list
        divisions = []
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        specification_name = segment_specification.specification_name
        timespan_1 = score_specification[specification_name].timespan
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation.new(timespan_1=timespan_1)
        for division in voice_division_list:
            if time_relation(timespan_2=division, 
                score_specification=score_specification, 
                context_name=self.voice_name):
                divisions.append(division)
        start_offset = divisions[0].start_offset
        divisions, start_offset = self._apply_payload_callbacks(divisions, start_offset)
        start_offset = divisions[0].start_offset
        stop_offset = divisions[-1].stop_offset
        timespan = timespantools.Timespan(start_offset, stop_offset)
        timespan = self._apply_timespan_callbacks(timespan)
        #self._debug(timespan, 'old-fashioned timespan')
        return timespan

    def _get_timespan_and_payload(self, score_specification, voice_name=None):
        raise NotImplementedError
#        from experimental.tools import settingtools
#        # ignore voice_name input parameter
#        voice_name = None
#        anchor_timespan = score_specification.get_anchor_timespan(self, self.voice_name)
#        self._debug(anchor_timespan, 'anchor timespan')
#        voice_proxy = score_specification.contexts[self.voice_name]
#        division_region_products = voice_proxy.division_region_products
#        if division_region_products is None:
#            return None, None
#        voice_division_list = voice_proxy.voice_division_list
#        self._debug(voice_division_list, 'voice division list')
#        existing_voice_divisions = []
#        for division_region_product in division_region_products:
#            #existing_voice_divisions.extend(division_region_product.payload.divisions)
#            for division in division_region_product.payload.divisions:
#                assert division.start_offset is not None
#                existing_voice_divisions.append(division)
#        self._debug(existing_voice_divisions, 'existing voice divisions')
#
#        timespan_1 = anchor_timespan
#        if self.time_relation is None:
#            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=anchor_timespan)
#            #time_relation = timerelationtools.timespan_2_intersects_timespan_1(timespan_1=anchor_timespan)
#        else:
#            time_relation = self.time_relation.new(timespan_1=anchor_timespan)
#
#        divisions = []
#        #for division in voice_division_list:
#        for division in existing_voice_divisions:
#            self._debug(division, 'division')
#            if time_relation(timespan_2=division, 
#                score_specification=score_specification, 
#                context_name=self.voice_name):
#                divisions.append(division)
#        self._debug(divisions, 'divisions')
#        if not divisions:
#            return None, None
#        start_offset = divisions[0].start_offset
#        result = settingtools.DivisionRegionProduct(
#            divisions, voice_name=self.voice_name, start_offset=start_offset)
#        #result &= anchor_timespan
#        #result = result[0]
#        self._debug(result, 'result')
#        divisions = result.payload.divisions
#        divisions, new_start_offset = self._apply_payload_callbacks(divisions, result.start_offset)
#        result = settingtools.DivisionRegionProduct(
#            divisions, 
#            voice_name=self.voice_name,
#            start_offset=new_start_offset)
#
#        self._debug(result.timespan, 'timespan')
#        self._debug(result, 'payload')
#        print ''
#        return result.timespan, result
