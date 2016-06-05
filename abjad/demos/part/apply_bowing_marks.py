# -*- coding: utf-8 -*-
import copy
from abjad.tools import indicatortools
from abjad.tools import markuptools
from abjad.tools import scoretools
from abjad.tools.topleveltools import attach
from abjad.tools.topleveltools import iterate


def apply_bowing_marks(score):
    r'''Applies bowing marks to score.
    '''

    # apply alternating upbow and downbow for first two sounding bars
    # of the first violin
    for measure in score['First Violin Voice'][6:8]:
        for i, chord in enumerate(iterate(measure).by_class(scoretools.Chord)):
            if i % 2 == 0:
                articulation = indicatortools.Articulation('downbow')
                attach(articulation, chord)
            else:
                articulation = indicatortools.Articulation('upbow')
                attach(articulation, chord)

    # create and apply rebowing markup
    rebow_markup = markuptools.Markup.concat([
        markuptools.Markup.musicglyph('scripts.downbow'),
        markuptools.Markup.hspace(1),
        markuptools.Markup.musicglyph('scripts.upbow'),
        ])
    markup = copy.copy(rebow_markup)
    attach(markup, score['First Violin Voice'][64][0])
    markup = copy.copy(rebow_markup)
    attach(markup, score['Second Violin Voice'][75][0])
    markup = copy.copy(rebow_markup)
    attach(markup, score['Viola Voice'][86][0])