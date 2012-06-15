from abjad.tools import *
from experimental import specificationtools
from experimental.specificationtools import library
from experimental.specificationtools.Directive import Directive
from experimental.specificationtools.DirectiveInventory import DirectiveInventory
from experimental.specificationtools.ScoreObjectIndicator import ScoreObjectIndicator
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.specificationtools.Selection import Selection
from experimental.specificationtools.TemporalCursor import TemporalCursor
from experimental.specificationtools.TemporalScope import TemporalScope


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
                contexts=['Grouped Rhythmic Staves Score'],
                scope=specificationtools.TemporalScope(
                    start=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
                            segment='1'
                            ),
                        edge=left
                        ),
                    stop=specificationtools.TemporalCursor(
                        anchor=specificationtools.ScoreObjectIndicator(
                            segment='1'
                            ),
                        edge=right
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

    assert disk_format == "specificationtools.DirectiveInventory([\n\tspecificationtools.Directive(\n\t\tspecificationtools.Selection(\n\t\t\tcontexts=['Grouped Rhythmic Staves Score'],\n\t\t\tscope=specificationtools.TemporalScope(\n\t\t\t\tstart=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=left\n\t\t\t\t\t),\n\t\t\t\tstop=specificationtools.TemporalCursor(\n\t\t\t\t\tanchor=specificationtools.ScoreObjectIndicator(\n\t\t\t\t\t\tsegment='1'\n\t\t\t\t\t\t),\n\t\t\t\t\tedge=right\n\t\t\t\t\t)\n\t\t\t\t)\n\t\t\t),\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tpersistent=True,\n\t\ttruncate=False\n\t\t)\n\t])"

    directive_inventory_2 = eval(disk_format)

    assert isinstance(directive_inventory_1, DirectiveInventory)
    assert isinstance(directive_inventory_2, DirectiveInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
