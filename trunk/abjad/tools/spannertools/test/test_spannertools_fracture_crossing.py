from abjad import *
import py.test


def test_spannertools_fracture_crossing_01( ):
   '''Fracture all spanners to the left of the leftmost component in list;
      fracture all spanners to the right of the rightmost component in list.
   '''

   t = Staff(scale(4))
   Beam(t[:])
   spannertools.fracture_crossing(t[1:3])

   r'''\new Staff {
      c'8 [ ]
      d'8 [
      e'8 ]
      f'8 [ ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8 [\n\te'8 ]\n\tf'8 [ ]\n}"
   

def test_spannertools_fracture_crossing_02( ):
   '''Fracture to the left of leftmost component;
      fracture to the right of rightmost component.'''

   t = Staff(scale(4))
   Beam(t[:])
   spannertools.fracture_crossing(t[1:2])

   r'''\new Staff {
      c'8 [ ]
      d'8 [ ]
      e'8 [
      f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\td'8 [ ]\n\te'8 [\n\tf'8 ]\n}"


def test_spannertools_fracture_crossing_03( ):
   '''Empty list raises no exception.'''

   result = spannertools.fracture_crossing([ ])
   assert result == [ ]


def test_spannertools_fracture_crossing_04( ):
   '''Nonsuccessive components raise ContiguityError.'''

   t1 = Staff(scale(4))
   t2 = Staff(scale(4))
   assert py.test.raises(
      ContiguityError, 'spannertools.fracture_crossing(t1[:] + t2[:])')


def test_spannertools_fracture_crossing_05( ):
   '''Fractures around components at only top level of list.'''

   t = Staff(Container(run(2)) * 3)
   pitchtools.diatonicize(t)
   Crescendo(t)
   Beam(t[:])
   
   r'''\new Staff {
      {
         c'8 [ \<
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ] \!
      }
   }'''

   spannertools.fracture_crossing(t[1:2])

   r'''\new Staff {
      {
         c'8 [ \<
         d'8 ]
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8 [
         a'8 ] \!
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [ \\<\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ] \\!\n\t}\n}"


def test_spannertools_fracture_crossing_06( ):
   '''Fractures around components at only top level of list.'''

   t = Staff(Container(run(2)) * 3)
   pitchtools.diatonicize(t)
   Crescendo(t)
   Beam(t[:])
   Trill(t.leaves)

   r'''\new Staff {
      {
         c'8 [ \< \startTrillSpan
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ] \! \stopTrillSpan
      }
   }'''

   spannertools.fracture_crossing(t[1:2])

   r'''\new Staff {
      {
         c'8 [ \< \startTrillSpan
         d'8 ]
      }
      {
         e'8 [
         f'8 ]
      }
      {
         g'8 [
         a'8 ] \! \stopTrillSpan
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\tc'8 [ \\< \\startTrillSpan\n\t\td'8 ]\n\t}\n\t{\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\tg'8 [\n\t\ta'8 ] \\! \\stopTrillSpan\n\t}\n}"
