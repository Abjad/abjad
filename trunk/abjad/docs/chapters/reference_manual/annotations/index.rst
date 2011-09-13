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



Attaching annotations to a component
------------------------------------

Attach annotations to any component with ``attach()``:

::

	abjad> note = Note("c'4")
	abjad> annotation.attach(note)


::

	abjad> annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))(c'4)


::

	abjad> another_annotation = marktools.Annotation('special pitch', pitchtools.NamedChromaticPitch('bs'))
	abjad> another_annotation.attach(note)


::

	abjad> another_annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))(c'4)



Getting the annotations attached to a component
-----------------------------------------------

Use mark tools to get all the annotations attached to a component:

::

	abjad> marktools.get_annotations_attached_to_component(note)
	(Annotation('special pitch', NamedChromaticPitch('bs'))(c'4), Annotation('special pitch', NamedChromaticPitch('bs'))(c'4))



Detaching annotations from a component one at a time
----------------------------------------------------

Use ``detach()`` to detach annotations from a component one at a time:

::

	abjad> annotation.detach()


::

	abjad> annotation
	Annotation('special pitch', NamedChromaticPitch('bs'))



Detaching all annotations attached to a component at once
---------------------------------------------------------

Or use mark tools to detach all annotations attachd to a component at once:

::

	abjad> print marktools.detach_annotations_attached_to_component(note)
	(Annotation('special pitch', NamedChromaticPitch('bs')),)


::

	abjad> marktools.get_annotations_attached_to_component(note)
	()



Inspecting the component to which an annotation is attached
-----------------------------------------------------------

Use ``start_component`` to inspect the component to which an annotation is attached:

::

	abjad> annotation.attach(note)


::

	abjad> annotation.start_component
	Note("c'4")



Inspecting annotation name
--------------------------

Use ``name`` to get the name of any annotation:

::

	abjad> annotation.name
	'special pitch'



Inspecting annotation value
---------------------------

And use ``value`` to get the value of any annotation:

::

	abjad> annotation.value
	NamedChromaticPitch('bs')
