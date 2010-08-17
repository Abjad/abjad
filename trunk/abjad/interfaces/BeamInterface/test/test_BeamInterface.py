from abjad import *


def test_BeamInterface_01( ):
   '''Beam interface attributes on a lone note.'''

   t = Note(0, (3, 64))
   #assert t.beam.counts is None
   assert not t.beam.spanned
   assert t.beam.spanners == set([ ])
   #assert t.beam.beamable
   assert not t.beam.first
   assert not t.beam.last
   assert not t.beam.only
   '''
   c'32.
   '''


def test_BeamInterface_02( ):
   '''Beam interface attributes on a contained note.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   #assert t[0].beam.counts is None
   assert not t[0].beam.spanned
   assert t[0].beam.spanners == set([ ])
   #assert t[0].beam.beamable
   assert not t[0].beam.first
   assert not t[0].beam.last
   assert not t[0].beam.only
   r'''
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


def test_BeamInterface_03( ):
   '''Beam interface attributes for a beamed note; first in beam.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t.leaves[ : 4])
   #assert t[0].beam.counts is None
   assert t[0].beam.spanned
   assert len(t[0].beam.spanners) == 1
   #assert t[0].beam.beamable
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


def test_BeamInterface_04( ):
   '''Beam interface attributes for beamed note; middle of beam.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t.leaves[ : 4])
   #assert t[1].beam.counts is None
   assert t[1].beam.spanned
   assert len(t[1].beam.spanners) == 1
   #assert t[1].beam.beamable
   assert not t[1].beam.first
   assert not t[1].beam.last
   assert not t[1].beam.only
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
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


def test_BeamInterface_05( ):
   '''Beam interface attributes for beamed note; last of beam.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t.leaves[ : 4])
   #assert t[3].beam.counts is None
   assert t[3].beam.spanned
   assert len(t[3].beam.spanners) == 1
   #assert t[3].beam.beamable
   assert not t[3].beam.first
   assert t[3].beam.last
   assert not t[3].beam.only
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
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


def test_BeamInterface_06( ):
   '''Beam interface attributes for beamed note; lone beam.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   spannertools.BeamSpanner(t[3])
   #assert t[3].beam.counts is None
   assert t[3].beam.spanned
   assert len(t[3].beam.spanners) == 1
   #assert t[3].beam.beamable
   assert t[3].beam.first
   assert t[3].beam.last
   assert t[3].beam.only
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\td'8\n\tef'8 [ ]\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
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


def test_BeamInterface_07( ):
   '''None can assign to counts.'''
   t = Note(0, (1, 32))
   #t.beam.counts = None
   #assert t.beam.counts is None
   assert t.format == "c'32"
   '''
   c'32
   '''


def test_BeamInterface_08( ):
   '''Zero can assign to counts.'''
   t = Note(0, (1, 32))
   #t.beam.counts = 0
   t.set.stem_left_beam_count = 0
   t.set.stem_right_beam_count = 0
   assert t.format == "\\set stemLeftBeamCount = #0\n\\set stemRightBeamCount = #0\nc'32"
   '''
   \set stemLeftBeamCount = #0
   \set stemRightBeamCount = #0
   c'32
   '''


def test_BeamInterface_09( ):
   '''A single positive integer can assign to counts.'''
   t = Note(0, (1, 32))
   #t.beam.counts = 3
   t.set.stem_left_beam_count = 3
   t.set.stem_right_beam_count = 3
   assert t.format == "\\set stemLeftBeamCount = #3\n\\set stemRightBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #3
   \set stemRightBeamCount = #3
   c'32
   '''


def test_BeamInterface_10( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   #t.beam.counts = None, 32
   t.set.stem_right_beam_count = 32
   assert t.format == "\\set stemRightBeamCount = #32\nc'32"
   '''
   \set stemRightBeamCount = #32
   c'32
   '''


def test_BeamInterface_11( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   #t.beam.counts = 3, None
   t.set.stem_left_beam_count = 3
   assert t.format == "\\set stemLeftBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #3
   c'32
   '''


def test_BeamInterface_12( ):
   '''Pairs of elements can assign to counts;
      each member must be either a nonnegative integer or None.'''
   t = Note(0, (1, 32))
   #t.beam.counts = 1, 3
   t.set.stem_left_beam_count = 1
   t.set.stem_right_beam_count = 3
   assert t.format == "\\set stemLeftBeamCount = #1\n\\set stemRightBeamCount = #3\nc'32"
   '''
   \set stemLeftBeamCount = #1
   \set stemRightBeamCount = #3
   c'32
   '''


def test_BeamInterface_13( ):
   '''Composer attributes assign and format.'''
   t = Note(0, (1, 32))
   t.override.beam.color = 'red'
   assert t.format == "\\once \\override Beam #'color = #red\nc'32"
   '''
   \once \override Beam #'color = #red
   c'32
   '''


def test_BeamInterface_14( ):
   '''Composer attributes clear.'''
   t = Note(0, (1, 32))
   t.override.beam.color = 'red'
   del(t.override.beam)
   assert t.format == "c'32"


def test_BeamInterface_15( ):
   '''Counts can set agrammatically but will not check.'''
   t = Note(0, (1, 32))
   assert componenttools.is_well_formed_component(t)
   #t.beam.counts = 1
   t.set.stem_left_beam_count = 1
   t.set.stem_right_beam_count = 1
   assert not componenttools.is_well_formed_component(t)
   #t.counts = 2
   t.set.stem_left_beam_count = 2
   t.set.stem_right_beam_count = 2
   assert not componenttools.is_well_formed_component(t)
   #t.counts = 3
   t.set.stem_left_beam_count = 3
   t.set.stem_right_beam_count = 3
   assert componenttools.is_well_formed_component(t)
   #t.counts = 3, 1
   t.set.stem_left_beam_count = 1
   t.set.stem_right_beam_count = 3
   assert componenttools.is_well_formed_component(t)
   #t.counts = 1, 3
   t.set.stem_left_beam_count = 1
   t.set.stem_right_beam_count = 3
   assert componenttools.is_well_formed_component(t)
   #t.counts = 3, 4
   t.set.stem_left_beam_count = 3
   t.set.stem_right_beam_count = 4
   assert not componenttools.is_well_formed_component(t)
   t.counts = 4
   t.set.stem_left_beam_count = 4
   t.set.stem_right_beam_count = 4
   assert not componenttools.is_well_formed_component(t)
   #t.counts = None
   del(t.set.stem_left_beam_count)
   del(t.set.stem_right_beam_count)
   assert componenttools.is_well_formed_component(t)
