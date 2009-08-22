from abjad import *


def test_chordtools_split_by_pitch_number_01( ):
   '''Chord split by number only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split_by_pitch_number(t, Pitch('d', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_02( ):
   '''Chord split by number only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split_by_pitch_number(t, Pitch('ef', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('d', 4), ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_03( ):
   '''Chord split by number only; one-note treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split_by_pitch_number(t, Pitch('e', 4))
   assert isinstance(treble, Note)
   assert treble.signature == ((('e', 4), ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_04( ):
   '''Chord split by number only; empty treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split_by_pitch_number(t, Pitch('f', 4))
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_05( ):
   '''Typographically crossed split by number only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.split_by_pitch_number(t, Pitch('f', 4))
   assert isinstance(treble, Chord)
   assert treble.signature == ((('es', 4), ('g', 4)), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ff', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   
   
def test_chordtools_split_by_pitch_number_06( ):
   '''Single note below pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split_by_pitch_number(note, Pitch('f', 4))
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('c', 4), ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_07( ):
   '''Single note at pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split_by_pitch_number(note, Pitch('c', 4))
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_08( ):
   '''Single note above pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split_by_pitch_number(note, Pitch('f', 3))
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_by_pitch_number_09( ):
   '''Rest splits into two new rests.'''
   t = Rest((1, 4))
   treble, bass = chordtools.split_by_pitch_number(t)
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
