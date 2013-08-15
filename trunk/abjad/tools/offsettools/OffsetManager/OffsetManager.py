from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class OffsetManager(AbjadObject):
    '''Update start offset, stop offsets and marks everywhere in score.
    '''

    ### PRIVATE METHODS ###

    @staticmethod
    def _iterate_entire_score(component):
        from abjad.tools import iterationtools
        parentage = component._select_parentage(include_self=True)
        components = iterationtools.iterate_components_depth_first(
            parentage.root, 
            capped=True, 
            unique=True, 
            forbid=None, 
            direction='left',
            )
        return components

    @staticmethod
    def _update_leaf_indices_and_measure_numbers(component):
        r'''Call only when updating offsets.
        No separate state flags exist for leaf indices or measure numbers.
        '''
        from abjad.tools import contexttools
        from abjad.tools import iterationtools
        parentage = component._select_parentage()
        score_root = parentage.root
        if isinstance(score_root, contexttools.Context):
            contexts = iterationtools.iterate_contexts_in_expr(score_root)
            for context in contexts:
                for leaf_index, leaf in enumerate(
                    iterationtools.iterate_leaves_in_expr(context)):
                    leaf._leaf_index = leaf_index
                for measure_index, measure in enumerate(
                    iterationtools.iterate_measures_in_expr(context)):
                    measure_number = measure_index + 1
                    measure._measure_number = measure_number
        else:
            for leaf_index, leaf in enumerate(
                iterationtools.iterate_leaves_in_expr(score_root)):
                leaf._leaf_index = leaf_index
            for measure_index, measure in enumerate(
                iterationtools.iterate_measures_in_expr(score_root)):
                measure_number = measure_index + 1
                measure._measure_number = measure_number

    @staticmethod
    def _update_marks(component):
        r'''Updating marks does not update offsets.
        On the other hand, getting effective mark updates offsets
        when at least one mark of appropriate type attaches to score.
        '''
        components = OffsetManager._iterate_entire_score(component)
        for component in components:
            for mark in component._start_marks:
                if hasattr(mark, '_update_effective_context'):
                    mark._update_effective_context()
            component._marks_are_current = True

    @staticmethod
    def _update_offsets(component):
        r'''Updating offsets does not update marks.
        Updating offsets does not update offsets in seconds.
        '''
        components = OffsetManager._iterate_entire_score(component)
        for component in components:
            OffsetManager.update_offset_values_of_component(component)
            component._offsets_are_current = True

    @staticmethod
    def _update_offsets_in_seconds(component):
        components = OffsetManager._iterate_entire_score(component)
        for component in components:
            OffsetManager.update_offset_values_of_component_in_seconds(
                component)
            component._offsets_in_seconds_are_current = True

    ### PUBLIC METHODS ###

    @staticmethod
    def update_offset_values_of_component(component):
        from abjad.tools import componenttools
        previous = \
            componenttools.get_nth_component_in_time_order_from_component(
            component, -1)
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
    def update_offset_values_of_component_in_seconds(component):
        from abjad.tools import componenttools
        try:
            current_duration_in_seconds = \
                component._get_duration(in_seconds=True)
            previous = \
                componenttools.get_nth_component_in_time_order_from_component(
                component, -1)
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
