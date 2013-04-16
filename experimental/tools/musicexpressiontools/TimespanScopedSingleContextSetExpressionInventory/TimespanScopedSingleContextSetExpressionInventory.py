import copy
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.timespantools.TimespanInventory import TimespanInventory


class TimespanScopedSingleContextSetExpressionInventory(TimespanInventory):
    '''Timespan-scoped single-context set expression inventory.
    '''

    ### PUBLIC METHODS ###

    def sort_and_split_set_expressions(self):
        '''Operate in place and return inventory.
        '''
        cooked_set_expressions = []
        for raw_set_expression in self[:]:
            set_expression_was_delayed, set_expression_was_split = False, False
            set_expressions_to_remove, set_expressions_to_curtail = [], []
            set_expressions_to_delay, set_expressions_to_split = [], []
            for cooked_set_expression in cooked_set_expressions:
                if raw_set_expression.target_timespan.contains_timespan_improperly(cooked_set_expression):
                    set_expressions_to_remove.append(cooked_set_expression)
                elif raw_set_expression.target_timespan.delays_timespan(cooked_set_expression):
                    set_expressions_to_delay.append(cooked_set_expression)
                elif raw_set_expression.target_timespan.curtails_timespan(cooked_set_expression):
                    set_expressions_to_curtail.append(cooked_set_expression)
                elif raw_set_expression.target_timespan.trisects_timespan(cooked_set_expression):
                    set_expressions_to_split.append(cooked_set_expression)
            for set_expression_to_remove in set_expressions_to_remove:
                cooked_set_expressions.remove(set_expression_to_remove)
            for set_expression_to_curtail in set_expressions_to_curtail:
                timespan = timespantools.Timespan(
                    set_expression_to_curtail.target_timespan.start_offset,
                    raw_set_expression.target_timespan.start_offset)
                set_expression_to_curtail._target_timespan = timespan
            for set_expression_to_delay in set_expressions_to_delay:
                timespan = timespantools.Timespan(
                    raw_set_expression.target_timespan.stop_offset,
                    set_expression_to_delay.target_timespan.stop_offset)
                set_expression_to_delay._target_timespan = timespan
                set_expression_was_delayed = True
            # TODO: branch inside and implement a method to split while treating cyclic payload smartly.
            # or, alternatively, special-case for set_expressions that cover the entire duration of score.
            for set_expression_to_split in set_expressions_to_split:
                left_set_expression = set_expression_to_split
                middle_set_expression = raw_set_expression
                right_set_expression = copy.deepcopy(left_set_expression)
                timespan = timespantools.Timespan(
                    left_set_expression.target_timespan.start_offset,
                    middle_set_expression.target_timespan.start_offset)
                left_set_expression._target_timespan = timespan
                timespan = timespantools.Timespan(
                    middle_set_expression.target_timespan.stop_offset,
                    right_set_expression.target_timespan.stop_offset)
                right_set_expression._target_timespan = timespan
                set_expression_was_split = True
            if set_expression_was_delayed:
                index = cooked_set_expressions.index(cooked_set_expression)
                cooked_set_expressions.insert(index, raw_set_expression)
            elif set_expression_was_split:
                cooked_set_expressions.append(middle_set_expression)
                cooked_set_expressions.append(right_set_expression)
            else:
                cooked_set_expressions.append(raw_set_expression)
            cooked_set_expressions.sort()
            #self._debug_values(cooked_set_expressions, 'cooked')
        #self._debug_values(cooked_set_expressions, 'cooked')
        self[:] = cooked_set_expressions
        return self

    def supply_missing_set_expressions(self, attribute, score_specification, voice_name):
        '''Operate in place and return inventory.
        '''
        assert self.is_sorted
        if not self and not score_specification.time_signatures:
            return self
        elif not self and score_specification.time_signatures:
            timespan = score_specification.timespan
            set_expression = score_specification.make_default_timespan_scoped_single_context_set_expression(
                attribute, timespan, voice_name)
            self[:] = [set_expression]
            return self
        timespans = timespantools.TimespanInventory([expr.target_timespan for expr in self])
        timespans.append(score_specification.timespan)
        missing_region_timespans = timespans.compute_logical_xor()
        for missing_region_timespan in missing_region_timespans:
            missing_set_expression = \
                score_specification.make_default_timespan_scoped_single_context_set_expression(
                attribute, missing_region_timespan, voice_name)
            self.append(missing_set_expression)
        self.sort()
        return self
