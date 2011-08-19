Annotations
===========

Annotate components with user-specific information for future use.

Annotations do not impact formatting.

Creating annotations
--------------------

Use mark tools to create annotations:

::

	abjad> annotation = marktools.Annotation('special pitch', pitchtools.NamedChromaticPitch('bs'))


::

	abjad> annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))


Attaching annotations
---------------------

Attach annotations by calling them:

::

	abjad> note = Note("c'4")
	abjad> annotation(note)


::

	abjad> annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))(c'4)


Creating and attaching annotations in one step
----------------------------------------------

Create and attach annotations in one step like this:

::

	abjad> another_annotation = marktools.Annotation('special pitch', pitchtools.NamedChromaticPitch('bs'))(note)


::

	abjad> another_annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))(c'4)


Getting annotations
-------------------

Use mark tools to get annotations:

::

	abjad> marktools.get_annotations_attached_to_component(note)
	(Annotation('special pitch', NamedChromaticPitch('bs'))(c'4), Annotation('special pitch', NamedChromaticPitch('bs'))(c'4))


Detaching annotations by hand
-----------------------------

Detach annotations by hand:

::

	abjad> annotation.detach_mark( )


::

	abjad> annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))


Detaching annotations automatically
-----------------------------------

Or use mark tools to detach all annotations at once:

::

	abjad> print marktools.detach_annotations_attached_to_component(note)
	(Annotation('special pitch', NamedChromaticPitch('bs')),)


::

	abjad> marktools.get_annotations_attached_to_component(note)
	()


Inspecting attachment
---------------------

Use ``start_component`` to inspect attachment:

::

	abjad> annotation(note)


::

	abjad> annotation.start_component
	Note("c'4")


Inspecting name
---------------

Use ``name`` to get the name of any annotation:

::

	abjad> annotation.name
	'special pitch'


Inspecting value
----------------

And use ``value`` to get the value of any annotation:

::

	abjad> annotation.value
	NamedChromaticPitch('bs')

