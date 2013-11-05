# -*- encoding: utf-8 -*-
from abjad import *


def test_marktools_TempoMark_storage_format_01():

    tempo_mark = marktools.TempoMark('Allegro', (1, 4), 84)

    r'''
    marktools.TempoMark(
        'Allegro',
        durationtools.Duration(1, 4),
        84
        )
    '''

    assert tempo_mark.storage_format == "marktools.TempoMark(\n\t'Allegro',\n\tdurationtools.Duration(1, 4),\n\t84\n\t)"
