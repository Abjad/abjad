from abjad import *
import py.test


def test_containertools_contents_reverse_01( ):
   '''Retrograde works on a depth-0 Container with no spanners and no parent.'''

   t = Staff(construct.scale(8))
   leaves_rev = reversed(t.leaves)
   containertools.contents_reverse(t)

   assert list(leaves_rev) == list(t.leaves)
   assert check.wf(t)


def test_containertools_contents_reverse_02( ):
   '''Retrograde works on a depth-0 Container with 
      one spanner attached and no parent.'''

   t = Staff(construct.scale(8))
   beam = Beam(t)
   leaves_rev = reversed(t.leaves)
   containertools.contents_reverse(t)

   assert list(leaves_rev) == list(t.leaves)
   assert beam.components == [t]
   assert check.wf(t)


def test_containertools_contents_reverse_03( ):
   '''Retrograde works on a depth-0 Container 
      with one spanner attached to its leaves and with no parent.'''

   t = Staff(construct.scale(8))
   beam = Beam(t.leaves)
   leaves_rev = reversed(t.leaves)
   containertools.contents_reverse(t)

   assert list(leaves_rev) == list(t.leaves)
   assert beam.components == list(t.leaves)
   assert check.wf(t)


def test_containertools_contents_reverse_04( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to itself and with a parent.'''

   t = Staff([DynamicMeasure(construct.scale(8))] + construct.run(2))
   beam = Beam(t[0])
   leaves_rev = reversed(t[0].leaves)
   containertools.contents_reverse(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == [t[0]]
   assert check.wf(t)


def test_containertools_contents_reverse_05( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its leaves and with a parent.'''

   t = Staff([DynamicMeasure(construct.scale(8))] + construct.run(2))
   beam = Beam(t[0].leaves)
   leaves_rev = reversed(t[0].leaves)
   containertools.contents_reverse(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == list(t[0].leaves)
   assert check.wf(t)


def test_containertools_contents_reverse_06( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its parent.'''

   t = Staff([DynamicMeasure(construct.scale(8))] + construct.scale(2))
   beam = Beam(t)
   leaves_rev = reversed(t[0].leaves)
   containertools.contents_reverse(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == [t]
   assert check.wf(t)


def test_containertools_contents_reverse_06( ):
   '''Retrograde works on a depth-0 Container with one spanner 
      attached to its parent's contents.'''

   notes = construct.scale(2)
   measure = DynamicMeasure(construct.scale(8))
   t = Staff([measure] + notes)
   beam = Beam(t[:])
   leaves_rev = reversed(t[0].leaves)
   containertools.contents_reverse(t[0])
   assert list(leaves_rev) == list(t[0].leaves)
   assert beam.components == [measure] + notes
   assert check.wf(t)


## TODO: Added check.wf( ) check for measure contiguity. ##

def test_containertools_contents_reverse_07( ):
   '''Retrograde unable to apply because of measure contiguity.'''

   notes = construct.scale(2)
   measure = DynamicMeasure(construct.scale(8))
   t = Staff([measure] + notes)
   beam = Beam(t[:])

   r'''\new Staff {
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
   }'''

   ## TODO: Make MeasureContiguityError raise here ##

#   assert py.test.raises(MeasureContiguityError, 
#      'containertools.contents_reverse(t)')


def test_containertools_contents_reverse_10( ):
   '''Retrograde works on a depth-2 Container with 
      no parent and with spanners at all levels.'''

   m1 = DynamicMeasure(construct.scale(4)) 
   m2 = DynamicMeasure(construct.scale(3))
   staff = Staff([m1, m2])
   pedal = PianoPedal(staff)
   trill = Trill(staff[:])
   beam1 = Beam(staff[0])
   beam2 = Beam(staff[1])
   gliss = Glissando(staff.leaves)
   containertools.contents_reverse(staff)
   assert staff[0] is m2
   assert staff[1] is m1
   assert len(m2) == 3
   assert len(m1) == 4
   assert pedal.components == [staff]
   assert trill.components == staff[:]
   assert beam1.components == [m1]
   assert beam2.components == [m2]
   assert gliss.components == list(staff.leaves)
   assert check.wf(staff)
