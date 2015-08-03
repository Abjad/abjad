# -*- encoding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class UpdateManager(AbjadObject):
    '''Update manager.

    Updates start offset, stop offsets and indicators everywhere in score.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_score_tree_state_flags(component):
        offsets_are_current = True
        indicators_are_current = True
        offsets_in_seconds_are_current = True
        parentage = component._get_parentage()
        for component in parentage:
            if offsets_are_current:
                if not component._offsets_are_current:
                    offsets_are_current = False
            if indicators_are_current:
                if not component._indicators_are_current:
                    indicators_are_current = False
            if offsets_in_seconds_are_current:
                if not component._offsets_in_seconds_are_current:
                    offsets_in_seconds_are_current = False
        return (
            offsets_are_current,
            indicators_are_current,
            offsets_in_seconds_are_current,
            )

    @staticmethod
    def _iterate_entire_score(component):
        from abjad.tools.topleveltools import iterate
        parentage = component._get_parentage(include_self=True)
        components = iterate(parentage.root).depth_first(
            capped=True,
            unique=True,
            forbid=None,
            direction='left',
            )
        return components

    def _update_all_indicators(self, component):
        r'''Updating indicators does not update offsets.
        On the other hand, getting an effective indicator does update
        offsets when at least one indicator of the appropriate type
        attaches to score.
        '''
        components = self._iterate_entire_score(component)
        for component in components:
            indicators = component._get_indicators(unwrap=False)
            for indicator in component._get_indicators(unwrap=False):
                if indicator.scope is not None:
                    assert hasattr(indicator, '_update_effective_context')
                    indicator._update_effective_context()
            component._indicators_are_current = True

    @staticmethod
    def _update_all_leaf_indices_and_measure_numbers(component):
        r'''Call only when updating offsets.
        No separate state flags exist for leaf indices or measure numbers.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
        parentage = component._get_parentage()
        score_root = parentage.root
        if isinstance(score_root, scoretools.Context):
            contexts = iterate(score_root).by_class(scoretools.Context)
            for context in contexts:
                for leaf_index, leaf in enumerate(
                    iterate(context).by_class(scoretools.Leaf)):
                    leaf._leaf_index = leaf_index
                for measure_index, measure in enumerate(
                    iterate(context).by_class(scoretools.Measure)):
                    measure_number = measure_index + 1
                    measure._measure_number = measure_number
        else:
            for leaf_index, leaf in enumerate(
                iterate(score_root).by_class(scoretools.Leaf)):
                leaf._leaf_index = leaf_index
            for measure_index, measure in enumerate(
                iterate(score_root).by_class(scoretools.Measure)):
                measure_number = measure_index + 1
                measure._measure_number = measure_number

    def _update_all_offsets(self, component):
        r'''Updating offsets does not update indicators.
        Updating offsets does not update offsets in seconds.
        '''
        components = self._iterate_entire_score(component)
        for component in components:
            self._update_component_offsets(component)
            component._offsets_are_current = True

    def _update_all_offsets_in_seconds(self, component):
        components = self._iterate_entire_score(component)
        for component in components:
            self._update_component_offsets_in_seconds(component)
            component._offsets_in_seconds_are_current = True

    @staticmethod
    def _update_component_offsets(component):
        from abjad.tools import durationtools
        previous = component._get_nth_component_in_time_order_from(-1)
        if previous is not None:
            start_offset = previous._stop_offset
        else:
            start_offset = durationtools.Offset(0)
        stop_offset = start_offset + component._get_duration()
        component._start_offset = start_offset
        component._stop_offset = stop_offset
        component._timespan._start_offset = start_offset
        component._timespan._stop_offset = stop_offset

    @staticmethod
    def _update_component_offsets_in_seconds(component):
        from abjad.tools import durationtools
        try:
            current_duration_in_seconds = \
                component._get_duration(in_seconds=True)
            previous = component._get_nth_component_in_time_order_from(-1)
            if previous is not None:
                component._start_offset_in_seconds = \
                    previous._get_timespan(in_seconds=True).stop_offset
            else:
                component._start_offset_in_seconds = durationtools.Offset(0)
            # this one case is possible for containers only
            if component._start_offset_in_seconds is None:
                raise MissingTempoError
            component._stop_offset_in_seconds = \
                component._start_offset_in_seconds + \
                current_duration_in_seconds
        except MissingTempoError:
            pass

    def _update_now(
        self,
        component,
        offsets=False,
        offsets_in_seconds=False,
        indicators=False,
        ):
        if component._is_forbidden_to_update:
            return
        parentage = component._get_parentage()
        for parent in parentage:
            if parent._is_forbidden_to_update:
                return
        state_flags = self._get_score_tree_state_flags(component)
        offsets_are_current = state_flags[0]
        indicators_are_current = state_flags[1]
        offsets_in_seconds_are_current = state_flags[2]
        if offsets and not offsets_are_current:
            self._update_all_offsets(component)
            self._update_all_leaf_indices_and_measure_numbers(component)
        if offsets_in_seconds and not offsets_in_seconds_are_current:
            self._update_all_offsets_in_seconds(component)
        if indicators and not indicators_are_current:
            self._update_all_indicators(component)
            self._update_all_offsets_in_seconds(component)

    ### EXPERIMENTAL ###

    def _get_logical_measure_start_offsets(self, component):
        from abjad.tools import durationtools
        from abjad.tools import indicatortools
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import inspect_
        expressions = []
        prototype = indicatortools.TimeSignature
        components = self._iterate_entire_score(component)
        for component in components:
            expressions_ = component._get_indicators(
                prototype,
                unwrap=False,
                )
            expressions.extend(expressions_)
        pairs = []
        for expression in expressions:
            inspector = inspect_(expression.component)
            start_offset = inspector.get_timespan().start_offset
            time_signature = expression.indicator
            pair = start_offset, time_signature
            pairs.append(pair)
        offset_zero = durationtools.Offset(0)
        default_time_signature = indicatortools.TimeSignature((4, 4))
        default_pair = (offset_zero, default_time_signature)
        if pairs and not pairs[0] == offset_zero:
            pairs.insert(0, default_pair)
        elif not pairs:
            pairs = [default_pair]
        pairs.sort(key=lambda x: x[0])
        parentage = component._get_parentage()
        score_root = parentage.root
        inspector = inspect_(score_root)
        score_stop_offset = inspector.get_timespan().stop_offset
        dummy_last_pair = (score_stop_offset, None)
        pairs.append(dummy_last_pair)
        measure_start_offsets = []
        pairs = sequencetools.iterate_sequence_nwise(pairs, n=2)
        for current_pair, next_pair in pairs:
            current_start_offset, current_time_signature = current_pair
            next_start_offset, next_time_signature = next_pair
            measure_start_offset = current_start_offset
            while measure_start_offset < next_start_offset:
                measure_start_offsets.append(measure_start_offset)
                measure_start_offset += current_time_signature.duration
        return measure_start_offsets

    # TODO: reimplement with some type of bisection
    def _to_logical_measure_number(
        self,
        component,
        logical_measure_number_start_offsets,
        ):
        from abjad.tools import mathtools
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import inspect_
        inspector = inspect_(component)
        component_start_offset = inspector.get_timespan().start_offset
        logical_measure_number_start_offsets = \
            logical_measure_number_start_offsets[:]
        logical_measure_number_start_offsets.append(mathtools.Infinity())
        pairs = sequencetools.iterate_sequence_nwise(
            logical_measure_number_start_offsets,
            n=2,
            )
        for logical_measure_index, pair in enumerate(pairs):
            if pair[0] <= component_start_offset < pair[-1]:
                logical_measure_number = logical_measure_index + 1
                return logical_measure_number
        message = 'can not find logical measure number: {!r}, {!r}.'
        message = message.format(
            component,
            logical_measure_number_start_offsets,
            )
        raise ValueError(message)

    def _update_logical_measure_numbers(self, component):
        logical_measure_start_offsets = \
            self._get_logical_measure_start_offsets(component)
        assert logical_measure_start_offsets, repr(
            logical_measure_start_offsets)
        components = self._iterate_entire_score(component)
        for component in components:
            logical_measure_number = self._to_logical_measure_number(
                component,
                logical_measure_start_offsets,
                )
            component._logical_measure_number = logical_measure_number