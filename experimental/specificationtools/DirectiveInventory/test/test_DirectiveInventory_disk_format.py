from abjad.tools import *
from specificationtools.DirectiveInventory import DirectiveInventory
from specificationtools.ScoreSpecification import ScoreSpecification
import specificationtools


def test_DirectiveInventory_disk_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives

    disk_format = directive_inventory_1._disk_format

    r'''
    specificationtools.DirectiveInventory([
        specificationtools.Directive(
            specificationtools.Selection(
                '1'
                ),
            'time_signatures',
            [(4, 8), (3, 8)],
            persistent=True,
            truncate=False
            )
        ])
    '''

    assert disk_format == "specificationtools.DirectiveInventory([\n\tspecificationtools.Directive(\n\t\tspecificationtools.Selection(\n\t\t\t'1'\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(disk_format)

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
