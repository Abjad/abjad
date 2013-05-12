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
	name='red directives'
	)
