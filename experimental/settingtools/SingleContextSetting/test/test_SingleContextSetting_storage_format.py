from experimental import requesttools
from experimental import settingtools
from experimental import specificationtools
from experimental import symbolictimetools
from abjad.tools import timerelationtools


def test_SingleContextSetting_storage_format_01():

    selector = symbolictimetools.SingleSegmentSymbolicTimespan(identifier='red')
    setting = settingtools.SingleContextSetting(
        'time_signatures', requesttools.AbsoluteRequest([(4, 8), (3, 8)]), selector, 
        context_name='Voice 1', fresh=False)

    r'''
    settingtools.SingleContextSetting(
        'time_signatures',
        requesttools.AbsoluteRequest(
            [(4, 8), (3, 8)]
            ),
        symbolictimetools.SingleSegmentSymbolicTimespan(
            identifier='red'
            ),
        context_name='Voice 1',
        fresh=False,
        persist=True
        )
    '''

    assert setting.storage_format == "settingtools.SingleContextSetting(\n\t'time_signatures',\n\trequesttools.AbsoluteRequest(\n\t\t[(4, 8), (3, 8)]\n\t\t),\n\tsymbolictimetools.SingleSegmentSymbolicTimespan(\n\t\tidentifier='red'\n\t\t),\n\tcontext_name='Voice 1',\n\tfresh=False,\n\tpersist=True\n\t)"
