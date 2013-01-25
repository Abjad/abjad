import copy
from abjad.tools import sequencetools
from abjad.tools import timespantools
from abjad.tools.timespantools.TimespanInventory import TimespanInventory


class TimespanScopedSingleContextSettingInventory(TimespanInventory):
    '''Timespan-scoped single-context setting inventory.
    '''

    ### PUBLIC METHODS ###

    def sort_and_split_settings(self):
        '''Operate in place and return timespan-scoped single-context setting inventory.
        '''
        cooked_settings = []
        for raw_setting in self[:]:
            setting_was_delayed, setting_was_split = False, False
            settings_to_remove, settings_to_curtail, settings_to_delay, settings_to_split = [], [], [], []
            for cooked_setting in cooked_settings:
                if raw_setting.timespan.contains_timespan_improperly(cooked_setting):
                    settings_to_remove.append(cooked_setting)
                elif raw_setting.timespan.delays_timespan(cooked_setting):
                    settings_to_delay.append(cooked_setting)
                elif raw_setting.timespan.curtails_timespan(cooked_setting):
                    settings_to_curtail.append(cooked_setting)
                elif raw_setting.timespan.trisects_timespan(cooked_setting):
                    settings_to_split.append(cooked_setting)
            #print settings_to_remove, settings_to_curtail, settings_to_delay, settings_to_split
            for setting_to_remove in settings_to_remove:
                cooked_settings.remove(setting_to_remove)
            for setting_to_curtail in settings_to_curtail:
                timespan = timespantools.Timespan(
                    setting_to_curtail.timespan.start_offset, raw_setting.timespan.start_offset)
                setting_to_curtail._timespan = timespan
            for setting_to_delay in settings_to_delay:
                timespan = timespantools.Timespan(
                    raw_setting.timespan.stop_offset, setting_to_delay.timespan.stop_offset)
                setting_to_delay._timespan = timespan
                setting_was_delayed = True
            # TODO: branch inside and implement a method to split while treating cyclic payload smartly.
            # or, alternatively, special-case for settings that cover the entire duration of score.
            for setting_to_split in settings_to_split:
                left_setting = setting_to_split
                middle_setting = raw_setting
                right_setting = copy.deepcopy(left_setting)
                timespan = timespantools.Timespan(
                    left_setting.timespan.start_offset, middle_setting.timespan.start_offset)
                left_setting._timespan = timespan
                timespan = timespantools.Timespan(
                    middle_setting.timespan.stop_offset, right_setting.timespan.stop_offset)
                right_setting._timespan = timespan
                setting_was_split = True
            if setting_was_delayed:
                index = cooked_settings.index(cooked_setting)
                cooked_settings.insert(index, raw_setting)
            elif setting_was_split:
                cooked_settings.append(middle_setting)
                cooked_settings.append(right_setting)
            else:
                cooked_settings.append(raw_setting)
            cooked_settings.sort()
            #self._debug_values(cooked_settings, 'cooked')
        #self._debug_values(cooked_settings, 'cooked')
        self[:] = cooked_settings
        return self

    def supply_missing_settings(self, attribute, score_specification, voice_name):
        '''Operate in place and return timespan-scoped single-context setting inventory.
        '''
        assert self.is_sorted
        if not self and not score_specification.time_signatures:
            return self
        elif not self and score_specification.time_signatures:
            timespan = score_specification.timespan
            setting = score_specification.make_default_timespan_scoped_single_context_setting(
                attribute, voice_name, timespan)
            self[:] = [setting]
            return self
        timespans = timespantools.TimespanInventory([expr.timespan for expr in self])
        timespans.append(score_specification.timespan)
        missing_region_timespans = timespans.compute_logical_xor() 
        for missing_region_timespan in missing_region_timespans:
            missing_setting = score_specification.make_default_timespan_scoped_single_context_setting(
                attribute, voice_name, missing_region_timespan)
            self.append(missing_setting)
        self.sort()
        return self
