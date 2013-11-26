# -*- encoding: utf-8 -*-
from abjad.tools import markuptools


red_directives = markuptools.MarkupInventory([
	markuptools.Markup(
		'\\bold { staccatissimo luminoso }',
		markup_name='staccatissimo'
		),
	markuptools.Markup(
		'\\italic { serenamente }',
		markup_name='serenamente'
		)
	],
	custom_identifier='red directives'
	)
