from abjad.tools import *
from experimental import selectortools
from experimental import specificationtools
from experimental import timespantools
from experimental.specificationtools import library
from experimental.specificationtools.Setting import Setting
from experimental.specificationtools.SettingInventory import SettingInventory
from experimental.selectortools.CounttimeComponentSelector import CounttimeComponentSelector
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextSelection import MultipleContextSelection
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan


def test_SettingInventory_storage_format_01():
    '''Storage format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    storage_format = directive_inventory_1.storage_format

    r'''
    specificationtools.SettingInventory([
        specificationtools.Setting(
            selectortools.MultipleContextSelection(
                contexts=['Grouped Rhythmic Staves Score'],
                timespan=timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='1'
                        )
                    )
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False
            )
        ])
    '''

    assert storage_format == "specificationtools.SettingInventory([\n\tspecificationtools.Setting(\n\t\tselectortools.MultipleContextSelection(\n\t\t\tcontexts=['Grouped Rhythmic Staves Score'],\n\t\t\ttimespan=timespantools.Timespan(\n\t\t\t\tselector=selectortools.SegmentSelector(\n\t\t\t\t\tindex='1'\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(storage_format)

    assert isinstance(directive_inventory_1, SettingInventory)
    assert isinstance(directive_inventory_2, SettingInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
