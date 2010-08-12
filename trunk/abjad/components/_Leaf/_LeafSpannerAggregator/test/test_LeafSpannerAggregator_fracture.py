from abjad import *


def test_LeafSpannerAggregator_fracture_01( ):
   '''
   Fracture left of t[0].

   Start with spanner spanning the four components in t.
   The spanner aggregator of component t[i] in t knows that 
   p and only p references t[i].

   Call clone_components_and_fracture_crossing_spanners('left') on the zeroth component t[0] in t.
   Three-element receipt returns. 
   Source spanner returns unaltered and continues to hold references
   to all four components in t.
   'left' part of receipt returns empty spanner and holds no references
   to any components in t.
   'right' part of receipt returns new spanner and holds references
   to all four components in t.
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[0].spanners.fracture('left')

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_02( ):
   '''
   Fracture left of t[1].
   
   Fracture left of positive index. 
   Three-element receipt.
   Source spanner returns unaltered.
   'left' and 'right' parts return new spanners.
   'left' and 'right' parts partition components in t.
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[1].spanners.fracture('left')

   r'''
   \new Voice {
      c'8 [ ]
      d'8 [
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ ]\n\td'8 [\n\te'8\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_03( ):
   '''
   Fracture left of t[-1].

   Three-element receipt.
   Source spanner returns unaltered.
   'left' and 'right' parts return new spanners.
   'left' and 'right' parts partition components in t.
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[-1].spanners.fracture('left')

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8 ]
      f'8 [ ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'8 [ ]\n}"


def test_LeafSpannerAggregator_fracture_04( ):
   '''
   Fracture right of t[0].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[0].spanners.fracture('right')   

   r'''
   \new Voice {
      c'8 [ ]
      d'8 [
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ ]\n\td'8 [\n\te'8\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_05( ):
   '''
   Fracture right of t[1].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[1].spanners.fracture('right')

   r'''
   \new Voice {
      c'8 [
      d'8 ]
      e'8 [
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n\te'8 [\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_06( ):
   '''
   Fracture right of t[-1].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[-1].spanners.fracture('right')

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_07( ):
   '''
   Fracture both sides of t[0].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[0].spanners.fracture( )

   r'''
   \new Voice {
      c'8 [ ]
      d'8 [
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ ]\n\td'8 [\n\te'8\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_08( ):
   '''
   Fracture both sides of t[1].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[1].spanners.fracture( )

   r'''
   \new Voice {
      c'8 [ ]
      d'8 [ ]
      e'8 [
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ ]\n\td'8 [ ]\n\te'8 [\n\tf'8 ]\n}"


def test_LeafSpannerAggregator_fracture_09( ):
   '''
   Fracture both sides of t[-1].
   '''

   t = Voice(macros.scale(4))
   p = Beam(t[ : ])

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8
      f'8 ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n}"

   t[-1].spanners.fracture( )

   r'''
   \new Voice {
      c'8 [
      d'8
      e'8 ]
      f'8 [ ]
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8\n\te'8 ]\n\tf'8 [ ]\n}"


def test_LeafSpannerAggregator_fracture_10( ):
   '''
   Fracture multiple spanners to either side of some component.
   '''

   t = Voice(macros.scale(4))
   p1 = Beam(t[ : ])
   p2 = Trill(t[ : ])

   r'''
   \new Voice {
      c'8 [ \startTrillSpan
      d'8
      e'8
      f'8 ] \stopTrillSpan
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ \\startTrillSpan\n\td'8\n\te'8\n\tf'8 ] \\stopTrillSpan\n}"

   t[1].spanners.fracture( )

   r'''
   \new Voice {
      c'8 [ ] \startTrillSpan \stopTrillSpan
      d'8 [ ] \startTrillSpan \stopTrillSpan
      e'8 [ \startTrillSpan
      f'8 ] \stopTrillSpan
   }
   '''

   assert t.format == "\\new Voice {\n\tc'8 [ ] \\startTrillSpan \\stopTrillSpan\n\td'8 [ ] \\startTrillSpan \\stopTrillSpan\n\te'8 [ \\startTrillSpan\n\tf'8 ] \\stopTrillSpan\n}"


def test_LeafSpannerAggregator_fracture_11( ):
   '''
   Fracturing left of a leaf doe NOT fracture 'up' into 
   spanners attaching to any containers in the parentage of leaf.
   '''

   t = Voice(Container(notetools.make_repeated_notes(2)) * 3)
   pitchtools.set_ascending_diatonic_pitches_on_nontied_pitched_components_in_expr(t)
   p = Beam(t[ : ])

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

   assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

   for leaf in t.leaves:
      leaf.spanners.fracture( )
      assert t.format == "\\new Voice {\n\t{\n\t\tc'8 [\n\t\td'8\n\t}\n\t{\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\tg'8\n\t\ta'8 ]\n\t}\n}"

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
