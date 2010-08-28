from abjad import *
import py.test


def test_ClefInterface_copy_01( ):
   '''Forced clefs copy.'''

   py.test.skip('extend function to copy clef marks.')
   t = Staff(notetools.make_repeated_notes(8))
   macros.chromaticize(t)
   #t[0].clef.forced = stafftools.Clef('treble')
   #t[4].clef.forced = stafftools.Clef('bass')
   marktools.ClefMark('treble')(t[0])
   marktools.ClefMark('bass')(t[4])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[:2]))

   r'''
   \new Staff {
           \clef "treble"
           c'8
           cs'8
           d'8
           ef'8
           \clef "bass"
           e'8
           f'8
           fs'8
           g'8
           \clef "treble"
           c'8
           cs'8
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t[0].clef.effective == stafftools.Clef('treble')
   assert t[1].clef.effective == stafftools.Clef('treble')
   assert t[2].clef.effective == stafftools.Clef('treble')
   assert t[3].clef.effective == stafftools.Clef('treble')
   assert t[4].clef.effective == stafftools.Clef('bass')
   assert t[5].clef.effective == stafftools.Clef('bass')
   assert t[6].clef.effective == stafftools.Clef('bass')
   assert t[7].clef.effective == stafftools.Clef('bass')
   assert t[8].clef.effective == stafftools.Clef('treble')
   assert t[9].clef.effective == stafftools.Clef('treble')

   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\t\\clef "treble"\n\tc'8\n\tcs'8\n}'''


def test_ClefInterface_copy_02( ):
   '''Implicit clefs do not copy.'''

   t = Staff(notetools.make_repeated_notes(8))
   macros.chromaticize(t)
   marktools.ClefMark('treble')(t[0])
   marktools.ClefMark('bass')(t[4])
   t.extend(componenttools.clone_components_and_immediate_parent_of_first_component(t[2:4]))

   assert componenttools.is_well_formed_component(t)
   assert t[0].clef.effective == marktools.ClefMark('treble')
   assert t[1].clef.effective == marktools.ClefMark('treble')
   assert t[2].clef.effective == marktools.ClefMark('treble')
   assert t[3].clef.effective == marktools.ClefMark('treble')
   assert t[4].clef.effective == marktools.ClefMark('bass')
   assert t[5].clef.effective == marktools.ClefMark('bass')
   assert t[6].clef.effective == marktools.ClefMark('bass')
   assert t[7].clef.effective == marktools.ClefMark('bass')
   assert t[8].clef.effective == marktools.ClefMark('bass')
   assert t[9].clef.effective == marktools.ClefMark('bass')

   assert t.format == '''\\new Staff {\n\t\\clef "treble"\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\t\\clef "bass"\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n\td'8\n\tef'8\n}'''
