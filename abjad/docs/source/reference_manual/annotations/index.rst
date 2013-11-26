Annotations
===========

Annotate components with user-specific information.

Annotations do not impact formatting.


Creating annotations
--------------------

Use mark tools to create annotations:

::

   >>> annotation_1 = indicatortools.Annotation('is inner voice', True)


::

   >>> annotation_1
   Annotation('is inner voice', True)



Attaching annotations to a component
------------------------------------

Attach annotations to any component with ``attach()``:

::

   >>> note = Note("c'4")
   >>> annotation_1.attach(note)
   Annotation('is inner voice', True)(c'4)


::

   >>> annotation_1
   Annotation('is inner voice', True)(c'4)


::

   >>> annotation_2 = indicatortools.Annotation('is phrase-initial', False)
   >>> annotation_2.attach(note)
   Annotation('is phrase-initial', False)(c'4)


::

   >>> annotation_2
   Annotation('is phrase-initial', False)(c'4)



Getting the annotations attached to a component
-----------------------------------------------

Use the inspector to get all the annotations attached to a component:

::

   >>> annotations = inspect(note).get_marks(mark_classes=indicatortools.Annotation)
   >>> for annotation in annotations: annotation
   ... 
   Annotation('is inner voice', True)(c'4)
   Annotation('is phrase-initial', False)(c'4)



Detaching annotations from a component
--------------------------------------

Use ``detach()`` to detach annotations from a component:

::

   >>> annotation_1.detach()
   Annotation('is inner voice', True)


::

   >>> annotation_1
   Annotation('is inner voice', True)



Inspecting the component to which an annotation is attached
-----------------------------------------------------------

Use ``start_component`` to inspect the component to which an annotation 
is attached:

::

   >>> annotation_1.attach(note)
   Annotation('is inner voice', True)(c'4)


::

   >>> annotation_1.start_component
   Note("c'4")



Inspecting annotation name
--------------------------

Use ``name`` to get the name of any annotation:

::

   >>> annotation_1.name
   'is inner voice'



Inspecting annotation value
---------------------------

Use ``value`` to get the value of any annotation:

::

   >>> annotation_1.value
   True



Getting the value of an annotation in a single call
---------------------------------------------------

Use the inspector to the get the value of an annotation in a single call:

::

   >>> inspect(note).get_annotation('is inner voice')
   True
