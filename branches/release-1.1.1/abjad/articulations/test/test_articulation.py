from abjad import *
import py.test


def test_articulation_01( ):
   '''Articulation formatting.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   assert str(a) == a.format == r'-\staccato'
   assert repr(a) == r'Articulation(-\staccato)'


def test_articulation_02( ):
   '''Articulations have string and direction.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   assert a.string == 'staccato'
   assert a.direction == '-'


def test_articulation_03( ):
   '''String can be set to None'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.string = None
   assert a.string == None
   assert str(a) == ''


def test_articulation_04( ):
   '''Direction can be set to None.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.direction = None
   assert a.direction == '-'
   assert str(a) == r'-\staccato'


def test_articulation_05( ):
   '''Direction can be set to up.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.direction = 'up'
   assert a.direction == '^'
   assert str(a) == r'^\staccato'
   a.direction = '^'
   assert a.direction == '^'
   assert str(a) == r'^\staccato'


def test_articulation_06( ):
   '''Direction can be set to down.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.direction = 'down'
   assert a.direction == '_'
   assert str(a) == r'_\staccato'
   a.direction = '_'
   assert a.direction == '_'
   assert str(a) == r'_\staccato'


def test_articulation_07( ):
   '''Direction can be set to default.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.direction = 'default'
   assert a.direction == '-'
   assert str(a) == r'-\staccato'
   a.direction = '-'
   assert a.direction == '-'
   assert str(a) == r'-\staccato'


def test_articulation_08( ):
   '''Direction can not be set to other.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   py.test.raises(ValueError, "a.direction = 'blah'")
   py.test.raises(AssertionError, "a.direction = 123")


def test_articulation_09( ):
   '''String can be set to any str.'''

   t = Note(0, (1, 4))
   t.articulations.append('staccato')
   a = t.articulations[0]
   a.string = 'staccato'
   assert a.string == 'staccato'
   assert str(a) == r'-\staccato'
   a.string = 'blah'
   assert a.string == 'blah'
   assert str(a) == r'-\blah'
   a.string = 'parangaricutirimicuaro'
   assert a.string == 'parangaricutirimicuaro'
   assert str(a) == r'-\parangaricutirimicuaro'


def test_articulation_10( ):
   '''Shortcut strings are replaced with full word.'''

   t = Note(0, (1, 4))
   t.articulations.append('.')
   a = t.articulations[0]
   assert a.string == '.'
   assert str(a) == r'-\staccato'
   a.string = '-'
   assert a.string == '-'
   assert str(a) == r'-\tenuto'
   a.string = '|'
   assert a.string == '|'
   assert str(a) == r'-\staccatissimo'
