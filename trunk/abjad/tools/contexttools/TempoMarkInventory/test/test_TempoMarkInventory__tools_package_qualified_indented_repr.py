from abjad import *


def test_TempoMarkInventory__tools_package_qualified_indented_repr_01():

    tempo_mark_inventory = contexttools.TempoMarkInventory([('Allegro', (1, 4), 84)])

    r'''
    contexttools.TempoMarkInventory([
        contexttools.TempoMark(
            'Allegro',
            durationtools.Duration(
                1,
                4
                ),
            84
            )
        ])
    '''

    assert tempo_mark_inventory._tools_package_qualified_indented_repr == "contexttools.TempoMarkInventory([\n\tcontexttools.TempoMark(\n\t\t'Allegro',\n\t\tdurationtools.Duration(\n\t\t\t1,\n\t\t\t4\n\t\t\t),\n\t\t84\n\t\t)\n\t])"

    assert tempo_mark_inventory._tools_package_qualified_repr == "contexttools.TempoMarkInventory([contexttools.TempoMark('Allegro', durationtools.Duration(1, 4), 84)])"
