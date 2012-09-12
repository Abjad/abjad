from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from experimental import timespaninequalitytools


def test_SingleContextSetting_storage_format_01():

    selector = selectortools.SingleSegmentSelector(identifier='red')
    setting = settingtools.SingleContextSetting('time_signatures', [(4, 8), (3, 8)], selector, 
        context_name='Voice 1', fresh=False)

    r'''
    settingtools.SingleContextSetting(
        'time_signatures',
        [(4, 8), (3, 8)],
        selectortools.SingleSegmentSelector(
            identifier='red'
            ),
        context_name='Voice 1',
        persist=True,
        fresh=False
        )
    '''

    assert setting.storage_format == "settingtools.SingleContextSetting(\n\t'time_signatures',\n\t[(4, 8), (3, 8)],\n\tselectortools.SingleSegmentSelector(\n\t\tidentifier='red'\n\t\t),\n\tcontext_name='Voice 1',\n\tpersist=True,\n\tfresh=False\n\t)"
