from abjad import *



def test_container_delitem_01( ):
   '''Delete spanned component.
   Component withdraws crossing spanners.
   Component carries covered spanners forward.
   Operation always leaves all expressions in tact.
   '''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[:])
   Slur(t[0][:])
   Slur(t[1][:])

   r'''
   \new Voice {
      {
         c'8 [ (
         d'8 )
      }
      {
         e'8 (
         f'8 ] )
      }
   }
   '''

   old = t[0]
   del(t[0])

   "Container t is now ..."

   r'''
   \new Voice {
      {
         e'8 [ (
         f'8 ] )
      }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t{\n\t\te'8 [ (\n\t\tf'8 ] )\n\t}\n}"

   "Deleted component is now ..."

   r'''
   {
      c'8 (
      d'8 )
   }
   '''

   assert check.wf(old)
   assert old.format == "{\n\tc'8 (\n\td'8 )\n}"


def test_container_delitem_02( ):
   '''Delete 1 leaf in container. 
   Spanner structure is preserved.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   del(t[1])

   r'''
   \new Voice {
           c'8 [
           e'8
           f'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\te'8\n\tf'8 ]\n}"


def test_container_delitem_03( ):
   '''Delete slice in middle of container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   del(t[1:3])

   r'''
   \new Voice {
           c'8 [
           f'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\tf'8 ]\n}"


def test_container_delitem_04( ):
   '''Delete slice from beginning to middle of container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   del(t[:2])

   r'''
   \new Voice {
           e'8 [
           f'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\te'8 [\n\tf'8 ]\n}"


def test_container_delitem_05( ):
   '''Delete slice from middle to end of container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   Beam(t[:])

   del(t[2:])

   r'''
   \new Voice {
           c'8 [
           d'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 [\n\td'8 ]\n}"


def test_container_delitem_06( ):
   '''Delete slice from beginning to end of container.'''

   t = Voice(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)) 
   Beam(t[:])

   del(t[:])

   r'''
   \new Voice {
   }
   '''

   assert check.wf(t)
   assert t.format == '\\new Voice {\n}'


def test_container_delitem_07( ):
   '''Detach leaf from tuplet and spanner.'''

   t = FixedDurationTuplet((2, 8), leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   Beam(t[:])

   del(t[1])

   r'''
   {
      c'8 [
      e'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "{\n\tc'8 [\n\te'8 ]\n}"
