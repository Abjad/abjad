from abjad import *


def test_marktools_detach_annotations_attached_to_component_01( ):

   staff = Staff(macros.scale(4))
   slur = spannertools.SlurSpanner(staff.leaves)
   marktools.Annotation('comment 1')(staff[0])
   marktools.Annotation('comment 2')(staff[0])
   annotations = marktools.get_annotations_attached_to_component(staff[0])
   assert len(annotations) == 2

   marktools.detach_annotations_attached_to_component(staff[0])
   annotations = marktools.get_annotations_attached_to_component(staff[0])
   assert len(annotations) == 0
