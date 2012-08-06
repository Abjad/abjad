from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespantools


def test_SingleContextSetting_storage_format_01():

    segment_selector = selectortools.SegmentItemSelector(identifier='red')
    timespan = timespantools.SingleSourceTimespan(selector=segment_selector)
    selector = selectortools.TimespanSelector(timespan)
    setting = settingtools.SingleContextSetting('time_signatures', [(4, 8), (3, 8)], selector, 
        context_name='Voice 1', fresh=False)

    r'''
    settingtools.SingleContextSetting(
        'time_signatures',
        [(4, 8), (3, 8)],
        selectortools.TimespanSelector(
            timespantools.SingleSourceTimespan(
                selector=selectortools.SegmentItemSelector(
                    identifier='red'
                    )
                )
            ),
        context_name='Voice 1',
        persist=True,
        truncate=False,
        fresh=False
        )
    '''

    assert setting.storage_format == "settingtools.SingleContextSetting(\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tselectortools.TimespanSelector(\n\t\ttimespantools.SingleSourceTimespan(\n\t\t\tselector=selectortools.SegmentItemSelector(\n\t\t\t\tidentifier='red'\n\t\t\t\t)\n\t\t\t)\n\t\t),\n\tcontext_name='Voice 1',\n\tpersist=True,\n\ttruncate=False,\n\tfresh=False\n\t)"
