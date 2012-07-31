from experimental import helpertools
from experimental.settingtools.Setting import Setting
import copy


class SingleContextSetting(Setting):
    r'''.. versionadded:: 1.0

    Single-context setting::

        >>> from experimental import *


    Set `attribute` to `source` for `target`::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=segment_selector.timespan)

    ::

        >>> single_context_setting = settingtools.SingleContextSetting(
        ... 'time_signatures', [(4, 8), (3, 8)], target, fresh=False)

    ::

        >>> z(single_context_setting)
        settingtools.SingleContextSetting(
            'time_signatures',
            [(4, 8), (3, 8)],
            selectortools.SingleContextTimespanSelector(
                'Voice 1',
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            persist=True,
            truncate=False,
            fresh=False
            )

    Return single-context setting.
    '''

    ### INITIALIZER ###

    def __init__(self, attribute, source, target, persist=True, truncate=False, fresh=True):
        Setting.__init__(self, attribute, source, target, persist=persist, truncate=truncate)
        assert isinstance(fresh, bool)
        self._fresh = fresh

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def fresh(self):
        '''True when single-context setting has been newly specified::

            >>> single_context_setting.fresh
            False

        Need to clarify relationship between `persist` and `fresh` keywords.

        Return boolean.
        '''
        return self._fresh

    @property
    def storage_format(self):
        '''Single-context setting storage format::

            >>> z(single_context_setting)
            settingtools.SingleContextSetting(
                'time_signatures',
                [(4, 8), (3, 8)],
                selectortools.SingleContextTimespanSelector(
                    'Voice 1',
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                persist=True,
                truncate=False,
                fresh=False
                )

        Return string.
        '''
        return Setting.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def copy_setting_to_segment(self, segment):
        '''Create new setting. Set new setting target to timespan of `segment`.
        Set new setting `fresh` to false.

        Only works when self encompasses one segment exactly.

        Return new setting.
        '''
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        new = copy.deepcopy(self)
        new.set_setting_to_segment(segment)
        new._fresh = False
        return new

    def set_setting_to_segment(self, segment):
        '''Set target of self to timespan of entire `segment`.

        Only works when self encompasses one segment exactly.

        Return none.
        '''
        from experimental import selectortools
        from experimental import specificationtools
        assert self.target.timespan.encompasses_one_segment_exactly, repr(self)
        segment_name = helpertools.expr_to_segment_name(segment)
        segment_selector = selectortools.SegmentSelector(index=segment_name)
        self.target._timespan = segment_selector.timespan
