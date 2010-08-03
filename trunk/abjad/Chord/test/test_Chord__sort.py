from abjad import *


def test_Chord__sort_01( ):
   '''Pitches manifestly different and sorted at initialization.'''
   t = Chord([Pitch('c', 4), Pitch('d', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('c', 4)
   assert t.pitches[1].pair == ('d', 4)


def test_Chord__sort_02( ):
   '''Pitches manifestly different but NOT sorted at initialization.'''
   t = Chord([Pitch('d', 4), Pitch('c', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('c', 4)
   assert t.pitches[1].pair == ('d', 4)


def test_Chord__sort_03( ):
   '''Pitches different only by accidentals but sorted at initialization.'''
   t = Chord([Pitch('c', 4), Pitch('cs', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude == t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('c', 4)
   assert t.pitches[1].pair == ('cs', 4)
   

def test_Chord__sort_04( ):
   '''Pitches different only by accidentals and NOT sorted at initialization.'''
   t = Chord([Pitch('cs', 4), Pitch('c', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude == t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('c', 4)
   assert t.pitches[1].pair == ('cs', 4)
   

def test_Chord__sort_05( ):
   '''Pitches enharmonically equivalent but sorted at initialization.'''
   t = Chord([Pitch('cs', 4), Pitch('df', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number == t.pitches[1].number
   assert t.pitches[0].pair == ('cs', 4)
   assert t.pitches[1].pair == ('df', 4)


def test_Chord__sort_06( ):
   '''Pitches enharmonically equivalent and NOT sorted in initialziation.'''
   t = Chord([Pitch('df', 4), Pitch('cs', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number == t.pitches[1].number
   assert t.pitches[0].pair == ('cs', 4)
   assert t.pitches[1].pair == ('df', 4)


def test_Chord__sort_07( ):
   '''Pitches typographically crossed but sorted at initialization.'''
   t = Chord([Pitch('css', 4), Pitch('dff', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('css', 4)
   assert t.pitches[1].pair == ('dff', 4)


def test_Chord__sort_08( ):
   '''Pitches typographically crossed and NOT sorted at initialization.'''
   t = Chord([Pitch('dff', 4), Pitch('css', 4)], (1, 4))
   assert len(t.pitches) == 2
   assert t.pitches[0].altitude != t.pitches[1].altitude
   assert t.pitches[0].number != t.pitches[1].number
   assert t.pitches[0].pair == ('css', 4)
   assert t.pitches[1].pair == ('dff', 4)
