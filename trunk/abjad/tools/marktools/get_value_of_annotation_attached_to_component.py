from abjad.exceptions import ExtraMarkError
from abjad.exceptions import MissingMarkError
from abjad.tools.marktools.get_annotations_attached_to_component import \
   get_annotations_attached_to_component


def get_value_of_annotation_attached_to_component(component, name):
   r'''.. versionadded:: 1.1.2

   Get value of annotation with `name` attached to `component`::

      abjad> staff = Staff("c'8 d'8 e'8 f'8")
      abjad> marktools.Annotation('special dictionary', { })(staff[0])

   ::

      abjad> f(staff)
      \new Staff {
         c'8
         d'8
         e'8
         f'8
      }
      
   ::
      
      abjad> marktools.get_value_of_annotation_attached_to_component(staff[0], 'special dictionary') 
      { }

   Return arbitrary value of annotation.

   Raise missing mark error when no annotation with `name` is attached.

   Raise extra mark error when more than one annotation with `name` is attached.
   '''

   annotations = get_annotations_attached_to_component(component)
   if not annotations:
      raise MissingMarkError

   with_correct_name = [ ]
   for annotation in annotations:
      if annotation.name == name:
         with_correct_name.append(annotation)

   if not with_correct_name:
      raise MissingMarkError

   if 1 < len(with_correct_name):
      raise ExtraMarkError

   return with_correct_name[0].value
