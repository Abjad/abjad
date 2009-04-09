from abjad import *


def test_chordtools_split_01( ):
   '''Chord split by number only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('d', 4), attr = 'number')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_02( ):
   '''Chord split by number only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('ef', 4), attr = 'number')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('d', 4), ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_03( ):
   '''Chord split by number only; one-note treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('e', 4), attr = 'number')
   assert isinstance(treble, Note)
   assert treble.signature == ((('e', 4), ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_04( ):
   '''Chord split by number only; empty treble.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('f', 4), attr = 'number')
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_05( ):
   '''Chord split by altitude only; empty bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('d', 4), attr = 'altitude')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('d', 4), ('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_split_06( ):
   '''Chord split by altitude only; one-note bass.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('e', 4), attr = 'altitude')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ef', 4), ('e', 4)), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('d', 4), ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   

def test_chordtools_split_07( ):
   '''Chord split by altitude is accidental agnostic.'''
   t = Chord([('d', 4), ('ef', 4), ('e', 4)], (1, 4))
   treble1, bass1 = chordtools.split(t, Pitch('e', 4), attr = 'altitude')
   treble2, bass2 = chordtools.split(t, Pitch('ef', 4), attr = 'altitude')
   assert treble1.signature == treble2.signature
   assert bass1.signature == bass2.signature


def test_chordtools_split_08( ):
   '''Typographically crossed split by number only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('f', 4), attr = 'number')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('es', 4), ('g', 4)), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('ff', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
   
   
def test_chordtools_split_09( ):
   '''Typographically crossed split by altitude only.'''
   t = Chord([('d', 4), ('es', 4), ('ff', 4), ('g', 4)], (1, 4))
   treble, bass = chordtools.split(t, Pitch('f', 4), attr = 'altitude')
   assert isinstance(treble, Chord)
   assert treble.signature == ((('ff', 4), ('g', 4)), (1, 4))
   assert isinstance(bass, Chord)
   assert bass.signature == ((('d', 4), ('es', 4)), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_10( ):
   '''Single note below pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split(note, Pitch('f', 4), attr = 'number')
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Note)
   assert bass.signature == ((('c', 4), ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_11( ):
   '''Single note at pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split(note, Pitch('c', 4), attr = 'number')
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_12( ):
   '''Single note above pitch number split point.'''
   note = Note(0, (1, 4))
   treble, bass = chordtools.split(note, Pitch('f', 3), attr = 'number')
   assert isinstance(treble, Note)
   assert treble.signature == ((('c', 4), ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert note is not treble
   assert note is not bass
   assert treble is not bass


def test_chordtools_split_13( ):
   '''Spanned chord DOES NOT copy spanner to resultant split parts.'''
   staff = Staff(Chord([2, 4, 5], (1, 4)) * 3)
   Beam(staff)
   t = staff[1]
   treble, bass = chordtools.split(t, Pitch('e', 4), attr = 'altitude')
   assert isinstance(treble, Chord)
   assert len(treble.spanners.attached) == 0
   assert isinstance(bass, Note)
   assert len(bass.spanners.attached) == 0
   assert t is not treble
   assert t is not bass
   assert treble is not bass


def test_chordtools_split_14( ):
   '''Rest splits into two new rests.'''
   t = Rest((1, 4))
   treble, bass = chordtools.split(t)
   assert isinstance(treble, Rest)
   assert treble.signature == (( ), (1, 4))
   assert isinstance(bass, Rest)
   assert bass.signature == (( ), (1, 4))
   assert t is not treble
   assert t is not bass
   assert treble is not bass
