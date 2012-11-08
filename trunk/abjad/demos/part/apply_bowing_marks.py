import copy
from abjad import *


def apply_bowing_marks(score):

    # apply alternating upbow and downbow for first two sounding bars
    # of the first violin
    for measure in score['First Violin Voice'][6:8]:
        for i, chord in enumerate(iterationtools.iterate_chords_in_expr(measure)):
            if i % 2 == 0:
                marktools.Articulation('downbow')(chord)
            else:
                marktools.Articulation('upbow')(chord)

    # create and apply rebowing markup
    rebow_markup = markuptools.Markup(
        markuptools.MarkupCommand(
            'concat', [
            markuptools.MarkupCommand(
                'musicglyph',
                schemetools.Scheme(
                    'scripts.downbow',
                    force_quotes=True,
                    ),
                ),
            markuptools.MarkupCommand(
                'hspace',
                1,
                ),
            markuptools.MarkupCommand(
                'musicglyph',
                schemetools.Scheme(
                    'scripts.upbow',
                    force_quotes=True,
                    ),
                ),
            ]))
    copy.copy(rebow_markup)(score['First Violin Voice'][64][0]) 
    copy.copy(rebow_markup)(score['Second Violin Voice'][75][0]) 
    copy.copy(rebow_markup)(score['Viola Voice'][86][0]) 

