from abjad import *
import py.test


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_01( ):
   '''Move parentage, children and spanners from multiple containers to empty tuplet.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
   macros.diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   tuplet = FixedDurationTuplet((3, 8), [ ])
   containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[:2], tuplet)

   r'''
   \new Voice {
      \fraction \times 3/4 {
         c'8 [
         d'8
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\fraction \\times 3/4 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_02( ):
   '''Move parentage, children and spanners from container to empty voice.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
   t.name = 'foo'
   macros.diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)
   
   r'''
   \context Voice = "foo" {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   new = Voice( )
   new.name = 'foo'
   containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], new)

   r'''
   \context Voice = "foo" {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \context Voice = "foo" {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == '\\context Voice = "foo" {\n\t{\n\t\tc\'8 [ \\glissando\n\t\td\'8 \\glissando\n\t}\n\t\\context Voice = "foo" {\n\t\te\'8 \\glissando\n\t\tf\'8 \\glissando\n\t}\n\t{\n\t\tg\'8 \\glissando\n\t\ta\'8 ]\n\t}\n}'


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_03( ):
   '''Move parentage, children and spanners from container to empty tuplet.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
   macros.diatonicize(t)
   Glissando(t[:])
   Beam(t.leaves)
   
   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   containertools.move_parentage_children_and_spanners_from_components_to_empty_container(
      t[1:2], FixedDurationTuplet((3, 16), [ ]))

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      \fraction \times 3/4 {
         e'8 \glissando
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t\\fraction \\times 3/4 {\n\t\te'8 \\glissando\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"

   assert componenttools.is_well_formed_component(t)


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_04( ):
   '''Trying to move parentage, children and spanners to noncontainer raises type error.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   Beam(t[:])
   macros.diatonicize(t)

   assert py.test.raises(TypeError, 
      'containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], Note(4, (1, 4)))')


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_05( ):
   '''Trying to move parentage, children and spanners from nonempty container
   to nonempty container raises music contents error.'''
   
   t = Voice(Container(notetools.make_repeated_notes(2)) * 2)
   Beam(t[:])
   macros.diatonicize(t)

   tuplet = FixedDurationTuplet((2, 8), macros.scale(3))
   assert py.test.raises(MusicContentsError, 
      'containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], tuplet)')


def test_containertools_move_parentage_children_and_spanners_from_components_to_empty_container_06( ):
   '''Trying to move parentage, children and spanners from components that are not parent-contiguous
   raises exception.'''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
   macros.diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         e'8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   tuplet = FixedDurationTuplet((3, 8), [ ])
   assert py.test.raises(AssertionError, 
      'containertools.move_parentage_children_and_spanners_from_components_to_empty_container([t[0], t[2]], tuplet)')
