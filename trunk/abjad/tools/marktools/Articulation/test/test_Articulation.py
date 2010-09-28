from abjad import *
import py.test


def test_Articulation_01( ):
   '''Articulations can be initialized from zero, one or two arguments.'''
   a = marktools.Articulation( )
   assert a.string == None
   assert a.direction == '-'
   a = marktools.Articulation('^\\marcato')
   assert a.string == 'marcato'
   assert a.direction == '^'
   a = marktools.Articulation('legato', 'down')
   assert a.string == 'legato'
   assert a.direction == '_'


def test_Articulation_02( ):
   '''Articulation formatting.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato')(t)
   assert str(a) == a.format == r'-\staccato'
   assert repr(a) == r"Articulation('-\staccato')"


def test_Articulation_03( ):
   '''Articulations have string and direction.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato')(t)
   assert a.string == 'staccato'
   assert a.direction == '-'


def test_Articulation_04( ):
   '''String can be set to None'''

   t = Note(0, (1, 4))
   a = marktools.Articulation( )(t)
   assert a.string is None
   assert str(a) == ''


def test_Articulation_05( ):
   '''Direction can be set to None.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato', None)(t)
   assert a.direction == '-'
   assert str(a) == r'-\staccato'


def test_Articulation_06( ):
   '''Direction can be set to up.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato', 'up')(t)
   assert a.direction == '^'
   assert str(a) == r'^\staccato'

   a = marktools.Articulation('staccato', '^')
   assert a.direction == '^'
   assert str(a) == r'^\staccato'


def test_Articulation_07( ):
   '''Direction can be set to down.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato', 'down')(t)
   assert a.direction == '_'
   assert str(a) == r'_\staccato'

   a = marktools.Articulation('staccato', '_')
   assert a.direction == '_'
   assert str(a) == r'_\staccato'


def test_Articulation_08( ):
   '''Direction can be set to default.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato')
   assert a.direction == '-'
   assert str(a) == r'-\staccato'

   a = marktools.Articulation('staccato', '-')
   assert a.direction == '-'
   assert str(a) == r'-\staccato'


def test_Articulation_09( ):
   '''Direction can not be set to other.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('staccato')(t)
   py.test.raises(AttributeError, "a.direction = 'blah'")
   py.test.raises(AttributeError, "a.direction = 123")


def test_Articulation_10( ):
   '''String can be set to any str.'''

   a = marktools.Articulation('staccato')
   assert a.string == 'staccato'
   assert str(a) == r'-\staccato'

   a = marktools.Articulation('blah')
   assert a.string == 'blah'
   assert str(a) == r'-\blah'

   a = marktools.Articulation('parangaricutirimicuaro')
   assert a.string == 'parangaricutirimicuaro'
   assert str(a) == r'-\parangaricutirimicuaro'


def test_Articulation_11( ):
   '''Shortcut strings are replaced with full word.'''

   t = Note(0, (1, 4))
   a = marktools.Articulation('.')(t)
   assert a.string == '.'
   assert str(a) == r'-\staccato'

   a = marktools.Articulation('-')
   assert a.string == '-'
   assert str(a) == r'-\tenuto'

   a = marktools.Articulation('|')
   assert a.string == '|'
   assert str(a) == r'-\staccatissimo'
