from experimental import requesttools
from experimental import selectortools
from experimental import settingtools
from experimental import specificationtools
from abjad.tools import timerelationtools


def test_SingleContextSetting_storage_format_01():

    selector = selectortools.SingleSegmentTimespanSelector(identifier='red')
    setting = settingtools.SingleContextSetting(
        'time_signatures', requesttools.AbsoluteRequest([(4, 8), (3, 8)]), selector, 
        context_name='Voice 1', fresh=False)

    r'''
    settingtools.SingleContextSetting(
        'time_signatures',
        requesttools.AbsoluteRequest(
            [(4, 8), (3, 8)]
            ),
        selectortools.SingleSegmentTimespanSelector(
            identifier='red'
            ),
        context_name='Voice 1',
        fresh=False,
        persist=True
        )
    '''

    assert setting.storage_format == "settingtools.SingleContextSetting(\n\t'time_signatures',\n\trequesttools.AbsoluteRequest(\n\t\t[(4, 8), (3, 8)]\n\t\t),\n\tselectortools.SingleSegmentTimespanSelector(\n\t\tidentifier='red'\n\t\t),\n\tcontext_name='Voice 1',\n\tfresh=False,\n\tpersist=True\n\t)"
