from abjad import *


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_01( ):
   '''Flip leaf under continuous spanner.'''

   t = Voice(macros.scale(4))
   Beam(t[:])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8
      d'8
      f'8 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\td'8\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_02( ):
   '''Flip leaf across spanner boundaries.'''

   t = Voice(macros.scale(4))
   Beam(t[:2])
   Beam(t[2:])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8 [
      f'8 ]
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])
   
   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8 [
      f'8 ]
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8 [\n\tf'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_03( ):
   '''Flip leaf from within to without spanner.'''

   t = Voice(macros.scale(4))
   Beam(t[:2])

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8
      f'8
   }
   '''

   componenttools.move_component_subtree_to_right_in_score_and_spanners(t[1])

   r'''
   \new Voice {
      c'8 [
      e'8 ]
      d'8
      f'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8 ]\n\td'8\n\tf'8\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_04( ):
   '''Donate from empty container to leaf.'''

   t = Voice([Container(macros.scale(2)), Container([ ])])
   Glissando(t[:])
   Beam(t[:])

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 ]
      }
      {
      }
   }
   '''

   #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], Note(4, (1, 8)))
   ## ALSO WORKS:
   componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [Note(4, (1, 8))])

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      e'8 ]
   }
   '''
   
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\te'8 ]\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_05( ):
   '''Donate from empty container to nonempty container.'''

   t = Voice([Container(macros.scale(2)), Container([ ])])
   Glissando(t[:])
   Beam(t[:])

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 ]
      }
      {
      }
   }
   '''

   container = Container([Note(4, (1, 8)), Note(5, (1, 8))])
   #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1:2], container)
   ## ALSO WORKS:
   componenttools.move_parentage_and_spanners_from_components_to_components(t[1:2], [container])

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         e'8 \glissando
         f'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\te'8 \\glissando\n\t\tf'8 ]\n\t}\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_06( ):
   '''Donate from note to rest.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(t)
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

   old = t.leaves[2]
   #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t.leaves[2:3], Rest((1, 8)))
   ## ALSO WORKS:
   componenttools.move_parentage_and_spanners_from_components_to_components(t.leaves[2:3], [Rest((1, 8))])

   r'''
   \new Voice {
      {
         c'8 [
         d'8
      }
      {
         r8
         f'8
      }
      {
         g'8
         a'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\tr8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"


def test_componenttools_move_component_subtree_to_right_in_score_and_spanners_07( ):
   '''Donate from note to tuplet.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 3)
   pitchtools.diatonicize(t)
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
   
   tuplet = FixedDurationTuplet((1, 8), Note(0, (1, 16)) * 3)
   #containertools.move_parentage_children_and_spanners_from_components_to_empty_container(t[1][:1], tuplet)
   ## ALSO WORKS:
   componenttools.move_parentage_and_spanners_from_components_to_components(t[1][:1], [tuplet])

   r'''
   \new Voice {
      {
         c'8 [ \glissando
         d'8 \glissando
      }
      {
         \times 2/3 {
            c'16 \glissando
            c'16 \glissando
            c'16 \glissando
         }
         f'8 \glissando
      }
      {
         g'8 \glissando
         a'8 ]
      }
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [ \\glissando\n\t\td'8 \\glissando\n\t}\n\t{\n\t\t\\times 2/3 {\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t\tc'16 \\glissando\n\t\t}\n\t\tf'8 \\glissando\n\t}\n\t{\n\t\tg'8 \\glissando\n\t\ta'8 ]\n\t}\n}"
