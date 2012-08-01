from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_SingleContextSetting_storage_format_01():

    segment_selector = selectortools.SegmentItemSelector(index='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    target = selectortools.SingleContextTimespanSelector('Voice 1', timespan)
    setting = settingtools.SingleContextSetting('time_signatures', [(4, 8), (3, 8)], target, fresh=False)

    r'''
    settingtools.SingleContextSetting(
        'time_signatures',
        [(4, 8), (3, 8)],
        selectortools.SingleContextTimespanSelector(
            'Voice 1',
            timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentItemSelector(
                    index='red'
                    )
                )
            ),
        persist=True,
        truncate=False,
        fresh=False
        )
    '''

    assert setting.storage_format == "settingtools.SingleContextSetting(\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tselectortools.SingleContextTimespanSelector(\n\t\t'Voice 1',\n\t\ttimespantools.SingleSourceTimespan(\n\t\t\tselector=selectortools.SegmentItemSelector(\n\t\t\t\tindex='red'\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\tpersist=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
