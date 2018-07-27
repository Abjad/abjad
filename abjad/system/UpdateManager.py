from abjad import enums
from abjad import exceptions
from abjad.system.AbjadObject import AbjadObject


class UpdateManager(AbjadObject):
    """
    Update manager.

    Updates start offset, stop offsets and indicators everywhere in score.
    """

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Managers'

    __slots__ = ()

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
        import abjad
        components = abjad.iterate(score_root)._depth_first(
            capped=True,
            unique=True,
            forbid=None,
            direction=enums.Left,
            )
        return components

    def _make_metronome_mark_map(self, score_root):
        from abjad.utilities.Multiplier import Multiplier
        from abjad.utilities.Offset import Offset
        from abjad.utilities.Sequence import Sequence
        from abjad.indicators.MetronomeMark import MetronomeMark
        from abjad.timespans.AnnotatedTimespan import AnnotatedTimespan
        from abjad.timespans.TimespanList import TimespanList
        pairs = []
        all_stop_offsets = set()
        for component in self._iterate_entire_score(score_root):
            indicators = component._get_indicators(MetronomeMark)
            if len(indicators) == 1:
                metronome_mark = indicators[0]
                if not metronome_mark.is_imprecise:
                    pair = (component._start_offset, metronome_mark)
                    pairs.append(pair)
            if component._stop_offset is not None:
                all_stop_offsets.add(component._stop_offset)
        pairs.sort(key=lambda _:_[0])
        if not pairs:
            return
        if pairs[0][0] != 0:
            return
        score_stop_offset = max(all_stop_offsets)
        timespans = TimespanList()
        clocktime_rate = MetronomeMark((1, 4), 60)
        clocktime_start_offset = Offset(0)
        for left, right in Sequence(pairs).nwise(wrapped=True):
            metronome_mark = left[-1]
            start_offset = left[0]
            stop_offset = right[0]
            # last timespan
            if stop_offset == 0:
                stop_offset = score_stop_offset
            duration = stop_offset - start_offset
            multiplier = Multiplier(60, metronome_mark.units_per_minute)
            clocktime_duration = duration / metronome_mark.reference_duration
            clocktime_duration *= multiplier
            timespan = AnnotatedTimespan(
                start_offset=start_offset,
                stop_offset=stop_offset,
                annotation=(clocktime_start_offset, clocktime_duration),
                )
            timespans.append(timespan)
            clocktime_start_offset += clocktime_duration
        return timespans

    def _update_all_indicators(self, score_root):
        """
        Updating indicators does not update offsets.
        On the other hand, getting an effective indicator does update
        offsets when at least one indicator of the appropriate type
        attaches to score.
        """
        import abjad
        components = self._iterate_entire_score(score_root)
        for component in components:
            for wrapper in abjad.inspect(component).wrappers():
                if wrapper.context is not None:
                    wrapper._update_effective_context()
            component._indicators_are_current = True

    @staticmethod
    def _update_all_leaf_indices_and_measure_numbers(score_root):
        """
        Call only when updating offsets.
        No separate state flags exist for leaf indices or measure numbers.
        """
        import abjad
        from abjad.top import iterate
        if isinstance(score_root, abjad.Context):
            contexts = iterate(score_root).components(abjad.Context)
            for context in contexts:
                for leaf_index, leaf in enumerate(iterate(context).leaves()):
                    leaf._leaf_index = leaf_index
                for measure_index, measure in enumerate(
                    iterate(context).components(abjad.Measure)):
                    measure_number = measure_index + 1
                    measure._measure_number = measure_number
        else:
            for leaf_index, leaf in enumerate(iterate(score_root).leaves()):
                leaf._leaf_index = leaf_index
            for measure_index, measure in enumerate(
                iterate(score_root).components(abjad.Measure)):
                measure_number = measure_index + 1
                measure._measure_number = measure_number

    def _update_all_offsets(self, score_root):
        """
        Updating offsets does not update indicators.
        Updating offsets does not update offsets in seconds.
        """
        for component in self._iterate_entire_score(score_root):
            self._update_component_offsets(component)
            component._offsets_are_current = True

    def _update_all_offsets_in_seconds(self, score_root):
        self._update_all_offsets(score_root)
        timespans = self._make_metronome_mark_map(score_root)
        for component in self._iterate_entire_score(score_root):
            self._update_clocktime_offsets(component, timespans)
            component._offsets_in_seconds_are_current = True

    @staticmethod
    def _update_clocktime_offsets(component, timespans):
        from abjad.utilities.Offset import Offset
        if not timespans:
            return
        for timespan in timespans:
            if (timespan.start_offset <= component._start_offset <
                timespan.stop_offset):
                pair = timespan.annotation
                clocktime_start_offset, clocktime_duration = pair
                local_offset = component._start_offset - timespan.start_offset
                multiplier = local_offset / timespan.duration
                duration = multiplier * clocktime_duration
                offset = clocktime_start_offset + duration
                component._start_offset_in_seconds = Offset(offset)
            if (timespan.start_offset <= component._stop_offset <
                timespan.stop_offset):
                pair = timespan.annotation
                clocktime_start_offset, clocktime_duration = pair
                local_offset = component._stop_offset - timespan.start_offset
                multiplier = local_offset / timespan.duration
                duration = multiplier * clocktime_duration
                offset = clocktime_start_offset + duration
                component._stop_offset_in_seconds = Offset(offset)
                return
        if component._stop_offset == timespans[-1].stop_offset:
            pair = timespans[-1].annotation
            clocktime_start_offset, clocktime_duration = pair
            offset = clocktime_start_offset + clocktime_duration
            component._stop_offset_in_seconds = Offset(offset)
            return
        raise Exception(f'can not find {stop_offset} in {timespans}.')

    @classmethod
    def _update_component_offsets(class_, component):
        import abjad
        if isinstance(component._parent, abjad.GraceContainer):
            pair = class_._get_grace_note_offsets(component)
            start_offset, stop_offset = pair
        elif isinstance(component._parent, abjad.AfterGraceContainer):
            pair = class_._get_after_grace_note_offsets(component)
            start_offset, stop_offset = pair
        else:
            previous = component._get_nth_component_in_time_order_from(-1)
            if previous is not None:
                start_offset = previous._stop_offset
            else:
                start_offset = abjad.Offset(0)
            stop_offset = start_offset + component._get_duration()
        component._start_offset = start_offset
        component._stop_offset = stop_offset
        component._timespan._start_offset = start_offset
        component._timespan._stop_offset = stop_offset

    def _update_now(
        self,
        component,
        offsets=False,
        offsets_in_seconds=False,
        indicators=False,
        ):
        import abjad
        assert offsets or offsets_in_seconds or indicators
        if component._is_forbidden_to_update:
            return
        parentage = abjad.inspect(component).parentage(
            include_self=True,
            grace_notes=True,
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

    ### EXPERIMENTAL ###

    @staticmethod
    def _get_after_grace_note_offsets(grace_note):
        import abjad
        after_grace_container = grace_note._parent
        assert isinstance(after_grace_container, abjad.AfterGraceContainer)
        carrier_leaf = after_grace_container._carrier
        carrier_leaf_stop_offset = carrier_leaf._stop_offset
        grace_displacement = -grace_note.written_duration
        sibling = grace_note._get_sibling(1)
        while sibling is not None:
            grace_displacement -= sibling.written_duration
            sibling = sibling._get_sibling(1)
        start_offset = abjad.Offset(
            carrier_leaf_stop_offset,
            grace_displacement=grace_displacement,
            )
        grace_displacement += grace_note.written_duration
        stop_offset = abjad.Offset(
            carrier_leaf_stop_offset,
            grace_displacement=grace_displacement,
            )
        return start_offset, stop_offset

    @staticmethod
    def _get_grace_note_offsets(grace_note):
        import abjad
        grace_container = grace_note._parent
        carrier_leaf = grace_container._carrier
        carrier_leaf_start_offset = carrier_leaf._start_offset
        grace_displacement = -grace_note.written_duration
        sibling = grace_note._get_sibling(1)
        while sibling is not None:
            grace_displacement -= sibling.written_duration
            sibling = sibling._get_sibling(1)
        start_offset = abjad.Offset(
            carrier_leaf_start_offset,
            grace_displacement=grace_displacement,
            )
        grace_displacement += grace_note.written_duration
        stop_offset = abjad.Offset(
            carrier_leaf_start_offset,
            grace_displacement=grace_displacement,
            )
        return start_offset, stop_offset

    def _get_measure_start_offsets(self, component):
        import abjad
        wrappers = []
        prototype = abjad.TimeSignature
        score_root = abjad.inspect(component).parentage(
            include_self=True).root
        for component in self._iterate_entire_score(score_root):
            wrappers_ = abjad.inspect(component).wrappers(prototype)
            wrappers.extend(wrappers_)
        pairs = []
        for wrapper in wrappers:
            inspector = abjad.inspect(wrapper.component)
            start_offset = inspector.timespan().start_offset
            time_signature = wrapper.indicator
            pair = start_offset, time_signature
            pairs.append(pair)
        offset_zero = abjad.Offset(0)
        default_time_signature = abjad.TimeSignature((4, 4))
        default_pair = (offset_zero, default_time_signature)
        if pairs and not pairs[0] == offset_zero:
            pairs.insert(0, default_pair)
        elif not pairs:
            pairs = [default_pair]
        pairs.sort(key=lambda x: x[0])
        parentage = abjad.inspect(component).parentage()
        score_root = parentage.root
        inspector = abjad.inspect(score_root)
        score_stop_offset = inspector.timespan().stop_offset
        dummy_last_pair = (score_stop_offset, None)
        pairs.append(dummy_last_pair)
        measure_start_offsets = []
        for current_pair, next_pair in abjad.sequence(pairs).nwise():
            current_start_offset, current_time_signature = current_pair
            next_start_offset, next_time_signature = next_pair
            measure_start_offset = current_start_offset
            while measure_start_offset < next_start_offset:
                measure_start_offsets.append(measure_start_offset)
                measure_start_offset += current_time_signature.duration
        return measure_start_offsets

    # TODO: reimplement with some type of bisection
    def _to_measure_number(
        self,
        component,
        measure_number_start_offsets,
        ):
        import abjad
        inspector = abjad.inspect(component)
        component_start_offset = inspector.timespan().start_offset
        measure_number_start_offsets = measure_number_start_offsets[:]
        measure_number_start_offsets.append(abjad.mathtools.Infinity())
        pairs = abjad.sequence(measure_number_start_offsets)
        pairs = pairs.nwise()
        for measure_index, pair in enumerate(pairs):
            if pair[0] <= component_start_offset < pair[-1]:
                measure_number = measure_index + 1
                return measure_number
        message = 'can not find measure number: {!r}, {!r}.'
        message = message.format(component, measure_number_start_offsets)
        raise ValueError(message)

    def _update_measure_numbers(self, component):
        import abjad
        measure_start_offsets = self._get_measure_start_offsets(component)
        assert measure_start_offsets, repr(measure_start_offsets)
        score_root = abjad.inspect(component).parentage(
            include_self=True).root
        for component in self._iterate_entire_score(score_root):
            measure_number = self._to_measure_number(
                component,
                measure_start_offsets,
                )
            component._measure_number = measure_number
