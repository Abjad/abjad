Annotations
===========

Annotate components with user-specific information.

Annotations do not impact formatting.


Creating annotations
--------------------

Create annotations like this:

<abjad>
annotation_1 = indicatortools.Annotation('is inner voice', True)
</abjad>


Attaching annotations to a component
------------------------------------

Attach annotations to any component with ``attach()``:

<abjad>
note = Note("c'4")
attach(annotation_1, note)
</abjad>

<abjad>
annotation_2 = indicatortools.Annotation('is phrase-initial', False)
attach(annotation_2, note)
</abjad>


Getting the annotations attached to a component
-----------------------------------------------

Use the inspector to get all the annotations attached to a component:

<abjad>
annotations = inspect_(note).get_indicators(indicatortools.Annotation)
for annotation in annotations: annotation
</abjad>


Detaching annotations from a component
--------------------------------------

Use ``detach()`` to detach annotations from a component:

<abjad>
detach(annotation_1, note)
</abjad>


Inspecting annotation name
--------------------------

Use ``name`` to get the name of any annotation:

<abjad>
annotation_2.name
</abjad>


Inspecting annotation value
---------------------------

Use ``value`` to get the value of any annotation:

<abjad>
annotation_2.value
</abjad>


Getting the value of an annotation in a single call
---------------------------------------------------

Use the inspector to the get the value of an annotation in a single call:

<abjad>
inspect_(note).get_annotation('is phrase-initial')
</abjad>
