from abjad import *


def test_marktools_detach_marks_attached_to_component_01( ):

   staff = Staff(macros.scale(4))
   slur = spannertools.SlurSpanner(staff.leaves)
   marktools.Articulation('^')(staff[0])
   marktools.Comment('comment 1')(staff[0])
   marktools.LilyPondCommandMark('slurUp')(staff[0])
   marks = marktools.get_marks_attached_to_component(staff[0])
   assert len(marks) == 3

   marktools.detach_marks_attached_to_component(staff[0])
   marks = marktools.get_marks_attached_to_component(staff[0])
   assert len(marks) == 0
