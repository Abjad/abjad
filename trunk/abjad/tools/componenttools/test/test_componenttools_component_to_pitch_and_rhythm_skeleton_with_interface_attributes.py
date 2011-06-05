from abjad import *
import py.test
py.test.skip('fix me')


def test_componenttools_component_to_pitch_and_rhythm_skeleton_with_interface_attributes_01( ):
   '''Pitch and rhythm skeleton preserves grob overrides.
   '''

   note = Note(0, (1, 4))
   note.override.beam.thickness = 2
   note.override.note_head.color = 'red'
   note.override.note_head.size = 3

   r'''
   \once \override Beam #'thickness = #2
   \once \override NoteHead #'color = #red
   \once \override NoteHead #'size = #3
   c'4
   '''

   skeleton = componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(note)

   r'''
   Note(('c', 4), Duration(1, 4), 
      override__beam__thickness = 2,
      override__note_head__color = 'red',
      override__note_head__size = 3)
   '''
   
   assert skeleton == "Note(('c', 4), Duration(1, 4), \n\toverride__beam__thickness = 2,\n\toverride__note_head__color = 'red',\n\toverride__note_head__size = 3)"

   new_note = eval(skeleton)
   new_skeleton = \
      componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(note)

   assert new_skeleton == skeleton


def test_componenttools_component_to_pitch_and_rhythm_skeleton_with_interface_attributes_02( ):
   '''Pitch and rhythm skeleton preserves context settings.
   '''

   note = Note(0, (1, 4))
   note.set.auto_beaming = False
   note.set.tuplet_full_length = True
   note.set.staff.instrument_name = 'Foo Bar'
   note.set.staff.short_instrument_name = 'F. b.'

   r'''
   \set Staff.instrumentName = "Foo Bar"
   \set Staff.shortInstrumentName = "F. b."
   \set autoBeaming = ##f
   \set tupletFullLength = ##t
   c'4
   '''

   skeleton = componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(note)

   r'''
   Note(('c', 4), Duration(1, 4), 
      set__auto_beaming = False,
      set__staff__instrument_name = 'Foo Bar',
      set__staff__short_instrument_name = 'F. b.',
      set__tuplet_full_length = True)
   '''

   assert skeleton == "Note(('c', 4), Duration(1, 4), \n\tset__auto_beaming = False,\n\tset__staff__instrument_name = 'Foo Bar',\n\tset__staff__short_instrument_name = 'F. b.',\n\tset__tuplet_full_length = True)"

   new_note = eval(skeleton)
   new_skeleton = \
      componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(note)
   
   assert new_note == note 
   assert new_skeleton == skeleton
