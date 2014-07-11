# -*- encoding: utf-8 -*-
from abjad import *


markup_inventory = markuptools.MarkupInventory(
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