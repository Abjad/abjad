from abjad.tools.abctools import AbjadObject


class UpdateManager(AbjadObject):
    '''Update start offset, stop offsets and marks everywhere in score.
    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _get_score_tree_state_flags(component):
        offsets_are_current = True
        marks_are_current = True
        offsets_in_seconds_are_current = True
        parentage = component._get_parentage()
        for component in parentage:
            if offsets_are_current:
                if not component._offsets_are_current:
                    offsets_are_current = False
            if marks_are_current:
                if not component._marks_are_current:
                    marks_are_current = False
            if offsets_in_seconds_are_current:
                if not component._offsets_in_seconds_are_current:
                    offsets_in_seconds_are_current = False
        return (
            offsets_are_current,
            marks_are_current,
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

    @staticmethod
    def _update_all_indicators(component):
        r'''Updating marks does not update offsets.
        On the other hand, getting effective mark updates offsets
        when at least one mark of appropriate type attaches to score.
        '''
        components = UpdateManager._iterate_entire_score(component)
        for component in components:
            for wrapper in component._get_wrappers():
                wrapper._update_effective_context()
            component._marks_are_current = True

    @staticmethod
    def _update_all_offsets(component):
        r'''Updating offsets does not update marks.
        Updating offsets does not update offsets in seconds.
        '''
        components = UpdateManager._iterate_entire_score(component)
        for component in components:
            UpdateManager._update_component_offsets(component)
            component._offsets_are_current = True

    @staticmethod
    def _update_all_offsets_in_seconds(component):
        components = UpdateManager._iterate_entire_score(component)
        for component in components:
            UpdateManager._update_component_offsets_in_seconds(component)
            component._offsets_in_seconds_are_current = True

    @staticmethod
    def _update_component_offsets(component):
        from abjad.tools import durationtools
        from abjad.tools import scoretools
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
        from abjad.tools import scoretools
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

    @staticmethod
    def _update_now(
        component,
        offsets=False,
        offsets_in_seconds=False,
        marks=False,
        ):
        if component._is_forbidden_to_update:
            return
        state_flags = UpdateManager._get_score_tree_state_flags(component)
        offsets_are_current = state_flags[0]
        marks_are_current = state_flags[1]
        offsets_in_seconds_are_current = state_flags[2]
        if offsets and not offsets_are_current:
            UpdateManager._update_all_offsets(component)
            UpdateManager._update_all_leaf_indices_and_measure_numbers(
                component)
        if offsets_in_seconds and not offsets_in_seconds_are_current:
            UpdateManager._update_all_offsets_in_seconds(component)
        if marks and not marks_are_current:
            UpdateManager._update_all_indicators(component)
            UpdateManager._update_all_offsets_in_seconds(component)
