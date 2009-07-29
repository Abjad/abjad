from abjad import *


def test_beam_interface_01( ):
   '''Beam interface attributes on a lone note.'''
   t = Note(0, (3, 64))
   assert t.beam.counts == (None, None)
   assert not t.beam.spanned
   assert t.beam.spanners == set([ ])
   assert t.beam.beamable
   assert not t.beam.first
   assert not t.beam.last
   assert not t.beam.only
   '''
   c'32.
   '''


def test_beam_interface_02( ):
   '''Beam interface attributes on a contained note.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   assert t[0].beam.counts == (None, None)
   assert not t[0].beam.spanned
   assert t[0].beam.spanners == set([ ])
   assert t[0].beam.beamable
   assert not t[0].beam.first
   assert not t[0].beam.last
   assert not t[0].beam.only
   '''
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_beam_interface_03( ):
   '''Beam interface attributes for a beamed note;
      first in beam.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t.leaves[ : 4])
   assert t[0].beam.counts == (None, None)
   assert t[0].beam.spanned
   assert len(t[0].beam.spanners) == 1
   assert t[0].beam.beamable
   assert t[0].beam.first
   assert not t[0].beam.last
   assert not t[0].beam.only
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_beam_interface_04( ):
   '''Beam interface attributes for beamed note;
      middle of beam.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t.leaves[ : 4])
   assert t[1].beam.counts == (None, None)
   assert t[1].beam.spanned
   assert len(t[1].beam.spanners) == 1
   assert t[1].beam.beamable
   assert not t[1].beam.first
   assert not t[1].beam.last
   assert not t[1].beam.only
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_beam_interface_05( ):
   '''Beam interface attributes for beamed note;
      last of beam.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t.leaves[ : 4])
   assert t[3].beam.counts == (None, None)
   assert t[3].beam.spanned
   assert len(t[3].beam.spanners) == 1
   assert t[3].beam.beamable
   assert not t[3].beam.first
   assert t[3].beam.last
   assert not t[3].beam.only
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_beam_interface_06( ):
   '''Beam interface attributes for beamed note;
      lone beam.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[3])
   assert t[3].beam.counts == (None, None)
   assert t[3].beam.spanned
   assert len(t[3].beam.spanners) == 1
   assert t[3].beam.beamable
   assert t[3].beam.first
   assert t[3].beam.last
   assert t[3].beam.only
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8 [ ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
   \new Staff {
           c'8
           cs'8
           d'8
           ef'8 [ ]
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_beam_interface_07( ):
   '''None can assign to counts.'''
   t = Note(0, (1, 32))
   t.beam.counts = None
   assert t.beam.counts == (None, None)
   assert t.format == "c'32"
   '''
   c'32
   '''


def test_beam_interface_08( ):
   '''Zero can assign to counts.'''
   t = Note(0, (1, 32))
   t.beam.counts = 0
   assert t.format == "\\set stemLeftBeamCount = #0\n\\set stemRightBeamCount = #0\nc'32"
   '''
   \set stemLeftBeamCount = #0
   \set stemRightBeamCount = #0
   c'32
   '''


def test_beam_interface_09( ):
   '''A single positive integer can assign to counts.'''
   t = Note(0, (1, 32))
   t.beam.counts = 3
   assert t.format == "\\set stemLeftBeamCount = #3\n\\set stemRightBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #3
   \set stemRightBeamCount = #3
   c'32
   '''


def test_beam_interface_10( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   t.beam.counts = None, 32
   assert t.format == "\\set stemRightBeamCount = #32\nc'32"
   '''
   \set stemRightBeamCount = #32
   c'32
   '''


def test_beam_interface_11( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   t.beam.counts = 3, None
   assert t.format == "\\set stemLeftBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #3
   c'32
   '''


def test_beam_interface_12( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   t.beam.counts = 1, 3
   assert t.format == "\\set stemLeftBeamCount = #1\n\\set stemRightBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #1
   \set stemRightBeamCount = #3
   c'32
   '''


def test_beam_interface_13( ):
   '''Composer attributes assign and format.'''
   t = Note(0, (1, 32))
   t.beam.color = 'red'
   assert t.format == "\\once \\override Beam #'color = #red\nc'32"
   '''
   \once \override Beam #'color = #red
   c'32
   '''


def test_beam_interface_14( ):
   '''Composer attributes clear.'''
   t = Note(0, (1, 32))
   t.beam.color = 'red'
   #t.beam.clear( )
   overridetools.clear_all(t.beam)
   assert t.format == "c'32"


#def test_beam_interface_15( ):
#   '''bridge( ) fuses adjacent beams towards the right.'''
#   t = Staff([Note(i,(1,16)) for i in range(8)])
#   Beam(t[0:4])
#   Beam(t[4:])
#   t[3].beam.bridge(1,'right')
#   assert t.format == "\\new Staff {\n\tc'16 [\n\tcs'16\n\td'16\n\t\\set stemRightBeamCount = #1\n\tef'16\n\t\\set stemLeftBeamCount = #1\n\te'16\n\tf'16\n\tfs'16\n\tg'16 ]\n}"
#   '''
#   \new Staff {
#           c'16 [
#           cs'16
#           d'16
#           \set stemRightBeamCount = #1
#           ef'16
#           \set stemLeftBeamCount = #1
#           e'16             
#           f'16
#           fs'16
#           g'16 ]
#   }
#   '''
 

#def test_beam_interface_16( ):
#   '''bridge( ) fuses adjacent beams towards the left.'''
#   t = Staff([Note(i,(1,16)) for i in range(8)])
#   Beam(t[0:4])
#   Beam(t[4:])
#   t[4].beam.bridge(1,'left')
#   assert t.format == "\\new Staff {\n\tc'16 [\n\tcs'16\n\td'16\n\t\\set stemRightBeamCount = #1\n\tef'16\n\t\\set stemLeftBeamCount = #1\n\te'16\n\tf'16\n\tfs'16\n\tg'16 ]\n}"
#   '''
#   \new Staff {
#           c'16 [
#           cs'16
#           d'16
#           \set stemRightBeamCount = #1
#           ef'16
#           \set stemLeftBeamCount = #1
#           e'16             
#           f'16
#           fs'16
#           g'16 ]
#   }
#   '''


#def test_beam_interface_17( ):
#   '''subdivide( ) works towards the right.'''
#   t = Staff([Note(i,(1,16)) for i in range(8)]) 
#   Beam(t[:])
#   t[4].beam.subdivide(1, 'right')
#   assert t.format == "\\new Staff {\n\tc'16 [\n\tcs'16\n\td'16\n\tef'16\n\t\\set stemRightBeamCount = #1\n\te'16\n\t\\set stemLeftBeamCount = #1\n\tf'16\n\tfs'16\n\tg'16 ]\n}"
#   '''
#   \new Staff {
#           c'16 [
#           cs'16
#           d'16
#           ef'16
#           \set stemRightBeamCount = #1
#           e'16
#           \set stemLeftBeamCount = #1
#           f'16
#           fs'16
#           g'16 ]
#   }
#   '''


#def test_beam_interface_18( ):
#   '''subdivide( ) works towards the left.'''
#   t = Staff([Note(i,(1,16)) for i in range(8)])
#   Beam(t[:])
#   t[3].beam.subdivide(1, 'left')
#   assert t.format == "\\new Staff {\n\tc'16 [\n\tcs'16\n\t\\set stemRightBeamCount = #1\n\td'16\n\t\\set stemLeftBeamCount = #1\n\tef'16\n\te'16\n\tf'16\n\tfs'16\n\tg'16 ]\n}"
#   '''
#   \new Staff {
#           c'16 [
#           cs'16
#           \set stemRightBeamCount = #1
#           d'16
#           \set stemLeftBeamCount = #1
#           ef'16
#           e'16
#           f'16
#           fs'16
#           g'16 ]    
#   }
#   '''


#def test_beam_interface_19( ):
#   '''None removes the effects of subdivide( ).'''
#   t = Staff([Note(i,(1,16)) for i in range(8)])
#   Beam(t[:])
#   t[3].beam.subdivide(1, 'left')
#   t[3].beam.subdivide(None, 'left')
#   assert t.format == "\\new Staff {\n\tc'16 [\n\tcs'16\n\td'16\n\tef'16\n\te'16\n\tf'16\n\tfs'16\n\tg'16 ]\n}"
#   '''
#   \new Staff {
#           c'16 [
#           cs'16
#           d'16
#           ef'16
#           e'16
#           f'16
#           fs'16
#           g'16 ]
#   }
#   '''


def test_beam_interface_20( ):
   '''Counts can set agrammatically but will not check.'''
   t = Note(0, (1, 32))
   assert check.wf(t)
   t.beam.counts = 1
   assert not check.wf(t)
   t.beam.counts = 2
   assert not check.wf(t)
   t.beam.counts = 3
   assert check.wf(t)
   t.beam.counts = 3, 1
   assert check.wf(t)
   t.beam.counts = 1, 3
   assert check.wf(t)
   t.beam.counts = 3, 4
   assert not check.wf(t)
   t.beam.counts = 4
   assert not check.wf(t)
   t.beam.counts = None
   assert check.wf(t)
