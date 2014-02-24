# -*- encoding: utf-8 -*-
from abjad import *


red_markup = markuptools.MarkupInventory(
    [
        markuptools.Markup(
            contents=(
                markuptools.MarkupCommand(
                    'bold',
                    ['staccatissimo', 'luminoso']
                    ),
                ),
            ),
        markuptools.Markup(
            contents=(
                markuptools.MarkupCommand(
                    'italic',
                    ['serenamente']
                    ),
                ),
            ),
        ]
    )
