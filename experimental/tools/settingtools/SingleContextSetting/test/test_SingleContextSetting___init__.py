from experimental import requesttools
from experimental import settingtools
from experimental import specificationtools
from experimental import symbolictimetools
from abjad.tools import timerelationtools


def test_SingleContextSetting___init___01():
    '''Initialize by hand.
    '''

    setting = settingtools.SingleContextSetting(
        'time_signatures', requesttools.AbsoluteRequest([(4, 8), (3, 8)]), 'red', context_name='Voice 1')

    assert isinstance(setting, settingtools.SingleContextSetting)
