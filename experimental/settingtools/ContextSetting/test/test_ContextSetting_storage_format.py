from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_ContextSetting_storage_format_01():

    segment_selector = selectortools.SegmentSelector(index='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan=timespan)
    setting = settingtools.ContextSetting(target, 'time_signatures', [(4, 8), (3, 8)], fresh=False)

    r'''
    settingtools.ContextSetting(
        selectortools.SingleContextTimespanSelector(
            'Voice 1',
            timespan=timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentSelector(
                    index='red'
                    )
                )
            ),
        'time_signatures',
        [(4, 8), (3, 8)],
        persistent=True,
        truncate=False,
        fresh=False
        )
    '''

    assert setting.storage_format == "settingtools.ContextSetting(\n\tselectortools.SingleContextTimespanSelector(\n\t\t'Voice 1',\n\t\ttimespan=timespantools.SingleSourceTimespan(\n\t\t\tselector=selectortools.SegmentSelector(\n\t\t\t\tindex='red'\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tpersistent=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
