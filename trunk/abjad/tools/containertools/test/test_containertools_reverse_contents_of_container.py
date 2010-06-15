from abjad import *
import py.test


def test_containertools_reverse_contents_of_container_01( ):
   '''Retrograde works on a depth-0 Container with no spanners and no parent.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   leaves_rev = reversed(t.leaves)
   containertools.reverse_contents_of_container(t)

   assert list(leaves_rev) == list(t.leaves)
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_02( ):
   '''Retrograde works on a depth-0 Container with 
      one spanner attached and no parent.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   beam = Beam(t)
   leaves_rev = reversed(t.leaves)
   containertools.reverse_contents_of_container(t)

   assert list(leaves_rev) == list(t.leaves)
   assert beam.components == (t, )
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_03( ):
   '''Retrograde works on a depth-0 Container 
      with one spanner attached to its leaves and with no parent.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   beam = Beam(t.leaves)
   leaves_rev = reversed(t.leaves)
   containertools.reverse_contents_of_container(t)

   assert list(leaves_rev) == list(t.leaves)
   assert beam.components == tuple(t.leaves)
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_04( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to itself and with a parent.'''

   t = Staff([DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))] + leaftools.make_repeated_notes(2))
   beam = Beam(t[0])
   leaves_rev = reversed(t[0].leaves)
   containertools.reverse_contents_of_container(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == (t[0], )
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_05( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its leaves and with a parent.'''

   t = Staff([DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))] + leaftools.make_repeated_notes(2))
   beam = Beam(t[0].leaves)
   leaves_rev = reversed(t[0].leaves)
   containertools.reverse_contents_of_container(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == tuple(t[0].leaves)
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_06( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its parent.'''

   t = Staff([DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))] + leaftools.make_first_n_notes_in_ascending_diatonic_scale(2))
   beam = Beam(t)
   leaves_rev = reversed(t[0].leaves)
   containertools.reverse_contents_of_container(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == tuple([t])
   assert componenttools.is_well_formed_component(t)


def test_containertools_reverse_contents_of_container_07( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its parent's contents.'''

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)
   measure = DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   t = Staff([measure] + notes)
   beam = Beam(t[:])
   leaves_rev = reversed(t[0].leaves)
   containertools.reverse_contents_of_container(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == tuple([measure] + notes)
   assert componenttools.is_well_formed_component(t)


## TODO: Added componenttools.is_well_formed_component( ) check for measure contiguity. ##

def test_containertools_reverse_contents_of_container_08( ):
   '''Retrograde unable to apply because of measure contiguity.'''

   notes = leaftools.make_first_n_notes_in_ascending_diatonic_scale(2)
   measure = DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(8))
   t = Staff([measure] + notes)
   beam = Beam(t[:])

   r'''
   \new Staff {
                   \time 1/1
                   c'8 [
                   d'8
                   e'8
                   f'8
                   g'8
                   a'8
                   b'8
                   c''8
           c'8
           d'8 ]
   }
   '''

   ## TODO: Make MeasureContiguityError raise here ##

#   assert py.test.raises(MeasureContiguityError, 
#      'containertools.reverse_contents_of_container(t)')


def test_containertools_reverse_contents_of_container_09( ):
   '''Retrograde works on a depth-2 Container with 
      no parent and with spanners at all levels.'''

   m1 = DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4)) 
   m2 = DynamicMeasure(leaftools.make_first_n_notes_in_ascending_diatonic_scale(3))
   staff = Staff([m1, m2])
   pedal = PianoPedal(staff)
   trill = Trill(staff[:])
   beam1 = Beam(staff[0])
   beam2 = Beam(staff[1])
   gliss = Glissando(staff.leaves)
   containertools.reverse_contents_of_container(staff)
   assert staff[0] is m2
   assert staff[1] is m1
   assert len(m2) == 3
   assert len(m1) == 4
   assert pedal.components == (staff, )
   assert trill.components == tuple(staff[:])
   assert beam1.components == (m1, )
   assert beam2.components == (m2, )
   assert gliss.components == tuple(staff.leaves)
   assert componenttools.is_well_formed_component(staff)
