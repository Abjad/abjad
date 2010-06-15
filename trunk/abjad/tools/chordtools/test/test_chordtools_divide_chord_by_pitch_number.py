from abjad import *


def test_chordtools_divide_chord_by_pitch_number_01( ):
   '''Chord split by number only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t, Pitch('d', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_02( ):
   '''Chord split by number only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t, Pitch('ef', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('d', 4), ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_03( ):
   '''Chord split by number only; one-note treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t, Pitch('e', 4))
   assert isinstance(treble, Note)
   assert treble.signature == ((('e', 4), ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_04( ):
   '''Chord split by number only; empty treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t, Pitch('f', 4))
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_05( ):
   '''Typographically crossed split by number only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t, Pitch('f', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('es', 4), ('g', 4)), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ff', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   
   
def test_chordtools_divide_chord_by_pitch_number_06( ):
   '''Single note below pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(note, Pitch('f', 4))
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('c', 4), ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_07( ):
   '''Single note at pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(note, Pitch('c', 4))
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_08( ):
   '''Single note above pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(note, Pitch('f', 3))
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_09( ):
   '''Rest splits into two new rests.'''
   t = Rest((1, 4))
   treble, bass = chordtools.divide_chord_by_pitch_number(t)
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_divide_chord_by_pitch_number_10( ):
   '''Split copies over note_head coloring.'''

   t = Chord([0, 1, 2, 3], (1, 4))
   t[0].color = 'red'
   t[1].color = 'red'
   t[2].color = 'blue'
   t[3].color = 'blue'
   
   r'''
   <
           \tweak #'color #red
           c'
           \tweak #'color #red
           cs'
           \tweak #'color #blue
           d'
           \tweak #'color #blue
           ef'
   >4
   '''

   treble, bass = chordtools.divide_chord_by_pitch_number(t, 2)

   r'''
   <
           \tweak #'color #blue
           d'
           \tweak #'color #blue
           ef'
   >4
   '''

   assert componenttools.is_well_formed_component(treble)
   assert treble.format == "<\n\t\\tweak #'color #blue\n\td'\n\t\\tweak #'color #blue\n\tef'\n>4"

   r'''
   <
           \tweak #'color #red
           c'
           \tweak #'color #red
           cs'
   >4   
   '''

   assert componenttools.is_well_formed_component(bass)
   assert bass.format == "<\n\t\\tweak #'color #red\n\tc'\n\t\\tweak #'color #red\n\tcs'\n>4"


def test_chordtools_divide_chord_by_pitch_number_11( ):
   '''Copy up-markup to treble and down-markup to bass.'''

   t = Chord([-11, 2, 5], (1, 4))
   t.markup.up.append('UP')
   t.markup.down.append('DOWN')

   "<cs d' f'>4 ^ \markup { UP } _ \markup { DOWN }"

   treble, bass = chordtools.divide_chord_by_pitch_number(t, 0)

   "<d' f'>4 ^ \markup { UP }"

   assert componenttools.is_well_formed_component(treble)
   assert treble.format == "<d' f'>4 ^ \\markup { UP }"

   "cs4 _ \markup { DOWN }"

   assert componenttools.is_well_formed_component(bass)
   assert bass.format == 'cs4 _ \\markup { DOWN }'
