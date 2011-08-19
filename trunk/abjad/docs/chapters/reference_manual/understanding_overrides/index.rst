Understanding Abjad overrides
=============================

Grob-override component plug-ins
--------------------------------

All Abjad containers have a grob-override plug-in:

::

	abjad> staff = Staff("c'4 d'4 e'4 f'4 g'4 a'4 g'2")


::

	abjad> staff.override.staff_symbol.color = 'blue'


::

	abjad> staff.override
	LilyPondGrobOverrideComponentPlugIn(staff_symbol__color = 'blue')


All Abjad leaves have a grob-override plug-in, too:

::

	abjad> leaf = staff[-1]


::

	abjad> leaf.override.note_head.color = 'red'
	abjad> leaf.override.stem.color = 'red'


::

	abjad> leaf.override
	LilyPondGrobOverrideComponentPlugIn(note_head__color = 'red', stem__color = 'red')


And so do Abjad spanners:

::

	abjad> slur = spannertools.SlurSpanner(staff[:])


::

	abjad> slur.override.slur.color = 'red'


::

	abjad> slur.override
	LilyPondGrobOverrideComponentPlugIn(slur__color = 'red')


Grob proxies
------------

Grob-override plug-ins contain grob proxies:

::

	abjad> leaf.override.note_head
	LilyPondGrobProxy(color = 'red')


::

	abjad> leaf.override.stem
	LilyPondGrobProxy(color = 'red')


Dot-chained override syntax
---------------------------

The's dot-chained grob override syntax shown here results from the special way
that the Abjad grob-override plug-in and grob proxy set and get their attributes.
