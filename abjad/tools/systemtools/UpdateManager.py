# -*- coding: utf-8 -*-
from abjad.tools.abctools import AbjadObject


class UpdateManager(AbjadObject):
    '''Update manager.

    Updates start offset, stop offsets and indicators everywhere in score.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_score_tree_state_flags(parentage):
        offsets_are_current = True
        indicators_are_current = True
        offsets_in_seconds_are_current = True
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
    def _iterate_entire_score(score_root):
        from abjad.tools.topleveltools import iterate
        components = iterate(score_root).depth_first(
            capped=True,
            unique=True,
            forbid=None,
            direction=Left,
            )
        return components

    def _update_all_indicators(self, score_root):
        r'''Updating indicators does not update offsets.
        On the other hand, getting an effective indicator does update
        offsets when at least one indicator of the appropriate type
        attaches to score.
        '''
        components = self._iterate_entire_score(score_root)
        for component in components:
            for indicator in component._get_indicators(unwrap=False):
                if indicator.scope is not None:
                    assert hasattr(indicator, '_update_effective_context')
                    indicator._update_effective_context()
            component._indicators_are_current = True

    @staticmethod
    def _update_all_leaf_indices_and_measure_numbers(score_root):
        r'''Call only when updating offsets.
        No separate state flags exist for leaf indices or measure numbers.
        '''
        from abjad.tools import scoretools
        from abjad.tools.topleveltools import iterate
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

    def _update_all_offsets(self, score_root):
        r'''Updating offsets does not update indicators.
        Updating offsets does not update offsets in seconds.
        '''
        for component in self._iterate_entire_score(score_root):
            self._update_component_offsets(component)
            component._offsets_are_current = True

    def _update_all_offsets_in_seconds(self, score_root):
        for component in self._iterate_entire_score(score_root):
            self._update_component_offsets_in_seconds(component)
            component._offsets_in_seconds_are_current = True

    @classmethod
    def _update_component_offsets(class_, component):
        from abjad.tools import durationtools
        from abjad.tools import scoretools
        if (isinstance(component._parent, scoretools.GraceContainer) and
            not component._parent.kind == 'after'):
            pair = class_._get_grace_note_offsets(component)
            start_offset, stop_offset = pair
        elif (isinstance(component._parent, scoretools.GraceContainer) and
            component._parent.kind == 'after'):
            pair = class_._get_after_grace_note_offsets(component)
            start_offset, stop_offset = pair
        else:
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
                    previous._get_timespan(in_seconds=True)._stop_offset
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
        assert offsets or offsets_in_seconds or indicators
        if component._is_forbidden_to_update:
            return
        parentage = component._get_parentage(
            include_self=True,
            with_grace_notes=True,
            )
        for parent in parentage:
            if parent._is_forbidden_to_update:
                return
        (
            offsets_are_current,
            indicators_are_current,
            offsets_in_seconds_are_current,
            ) = self._get_score_tree_state_flags(parentage)
        score_root = parentage.root
        if offsets and not offsets_are_current:
            self._update_all_offsets(score_root)
            self._update_all_leaf_indices_and_measure_numbers(score_root)
        if offsets_in_seconds and not offsets_in_seconds_are_current:
            self._update_all_offsets_in_seconds(score_root)
        if indicators and not indicators_are_current:
            self._update_all_indicators(score_root)
            self._update_all_offsets_in_seconds(score_root)

    ### EXPERIMENTAL ###

    @staticmethod
    def _get_after_grace_note_offsets(grace_note):
        from abjad.tools import durationtools
        after_grace_container = grace_note._parent
        assert after_grace_container.kind == 'after'
        carrier_leaf = after_grace_container._carrier
        carrier_leaf_stop_offset = carrier_leaf._stop_offset
        grace_displacement = -grace_note.written_duration
        sibling = grace_note._get_sibling(1)
        while sibling is not None:
            grace_displacement -= sibling.written_duration
            sibling = sibling._get_sibling(1)
        start_offset = durationtools.Offset(
            carrier_leaf_stop_offset,
            grace_displacement=grace_displacement,
            )
        grace_displacement += grace_note.written_duration
        stop_offset = durationtools.Offset(
            carrier_leaf_stop_offset,
            grace_displacement=grace_displacement,
            )
        return start_offset, stop_offset

    @staticmethod
    def _get_grace_note_offsets(grace_note):
        from abjad.tools import durationtools
        grace_container = grace_note._parent
        carrier_leaf = grace_container._carrier
        carrier_leaf_start_offset = carrier_leaf._start_offset
        grace_displacement = -grace_note.written_duration
        sibling = grace_note._get_sibling(1)
        while sibling is not None:
            grace_displacement -= sibling.written_duration
            sibling = sibling._get_sibling(1)
        start_offset = durationtools.Offset(
            carrier_leaf_start_offset,
            grace_displacement=grace_displacement,
            )
        grace_displacement += grace_note.written_duration
        stop_offset = durationtools.Offset(
            carrier_leaf_start_offset,
            grace_displacement=grace_displacement,
            )
        return start_offset, stop_offset

    def _get_logical_measure_start_offsets(self, component):
        from abjad.tools import durationtools
        from abjad.tools import indicatortools
        from abjad.tools import sequencetools
        from abjad.tools.topleveltools import inspect_
        expressions = []
        prototype = indicatortools.TimeSignature
        score_root = component._get_parentage(include_self=True).root
        for component in self._iterate_entire_score(score_root):
            expressions_ = component._get_indicators(
                prototype,
                unwrap=False,
                )
            expressions.extend(expressions_)
        pairs = []
        for expression in expressions:
            inspector = inspect_(expression.component)
            start_offset = inspector.get_timespan()._start_offset
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
        score_stop_offset = inspector.get_timespan()._stop_offset
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
        component_start_offset = inspector.get_timespan()._start_offset
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
        score_root = component._get_parentage(include_self=True).root
        for component in self._iterate_entire_score(score_root):
            logical_measure_number = self._to_logical_measure_number(
                component,
                logical_measure_start_offsets,
                )
            component._logical_measure_number = logical_measure_number