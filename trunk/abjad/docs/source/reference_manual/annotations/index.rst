Annotations
===========

Annotate components with user-specific information for future use.

Annotations do not impact formatting.


Creating annotations
--------------------

Use mark tools to create annotations:

::

   >>> annotation = marktools.Annotation('special pitch', pitchtools.NamedPitch('bs'))


::

   >>> annotation
   Annotation('special pitch', NamedPitch('bs'))



Attaching annotations to a component
------------------------------------

Attach annotations to any component with ``attach()``:

::

   >>> note = Note("c'4")
   >>> annotation.attach(note)
   Annotation('special pitch', NamedPitch('bs'))(c'4)


::

   >>> annotation
   Annotation('special pitch', NamedPitch('bs'))(c'4)


::

   >>> another_annotation = marktools.Annotation('special pitch', pitchtools.NamedPitch('bs'))
   >>> another_annotation.attach(note)
   Annotation('special pitch', NamedPitch('bs'))(c'4)


::

   >>> another_annotation
   Annotation('special pitch', NamedPitch('bs'))(c'4)



Getting the annotations attached to a component
-----------------------------------------------

Use mark tools to get all the annotations attached to a component:

::

   >>> marktools.get_annotations_attached_to_component(note)
   (Annotation('special pitch', NamedPitch('bs'))(c'4), Annotation('special pitch', NamedPitch('bs'))(c'4))



Detaching annotations from a component one at a time
----------------------------------------------------

Use ``detach()`` to detach annotations from a component one at a time:

::

   >>> annotation.detach()
   Annotation('special pitch', NamedPitch('bs'))


::

   >>> annotation
   Annotation('special pitch', NamedPitch('bs'))



Detaching all annotations attached to a component at once
---------------------------------------------------------

Or use mark tools to detach all annotations attachd to a component at once:

::

   >>> print marktools.detach_annotations_attached_to_component(note)
   (Annotation('special pitch', NamedPitch('bs')),)


::

   >>> marktools.get_annotations_attached_to_component(note)
   ()



Inspecting the component to which an annotation is attached
-----------------------------------------------------------

Use ``start_component`` to inspect the component to which an annotation is attached:

::

   >>> annotation.attach(note)
   Annotation('special pitch', NamedPitch('bs'))(c'4)


::

   >>> annotation.start_component
   Note("c'4")



Inspecting annotation name
--------------------------

Use ``name`` to get the name of any annotation:

::

   >>> annotation.name
   'special pitch'



Inspecting annotation value
---------------------------

And use ``value`` to get the value of any annotation:

::

   >>> annotation.value
   NamedPitch('bs')
