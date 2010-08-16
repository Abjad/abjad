from abjad import *


def test_MarkupInterface_01( ):
   '''Append integer.'''
   t = Note(0, (1, 4))
   t.markup.down.append(12)
   assert t.format == "c'4 _ \\markup { 12 }"
   r'''
   c'4 _ \markup { 12 }
   '''


def test_MarkupInterface_02( ):
   '''Append string.'''
   t = Note(0, (1, 4))
   t.markup.down.append('12')
   assert t.format == "c'4 _ \\markup { 12 }"
   r'''
   c'4 _ \markup { 12 }
   '''
   

def test_MarkupInterface_03( ):
   '''Both up and down.'''
   t = Note(0, (1, 4))
   t.markup.up.append('foo')
   t.markup.down.append('bar')
   assert t.format == "c'4 ^ \\markup { foo } _ \\markup { bar }"
   r'''
   c'4 ^ \markup { foo } _ \markup { bar }
   '''


def test_MarkupInterface_04( ):
   '''Append string with LilyPond formatting command.'''
   t = Note(0, (1, 4))
   t.markup.up.append(r'\italic { attaca! }')
   assert t.format == "c'4 ^ \\markup { \\italic { attaca! } }"
   r'''
   c'4 ^ \markup { \italic { attaca! } }
   '''


def test_MarkupInterface_05( ):
   '''Extend multiple strings below.'''
   t = Note(0, (1, 4))
   t.markup.down.extend(['1/4', '1/6'])
   assert t.format == "c'4 _ \markup { \column { 1/4 1/6 } }"
   r'''
   c'4 _ \markup { \column { 1/4 1/6 } }
   '''


def test_MarkupInterface_06( ):
   '''Extend multiple strings above.'''
   t = Note(0, (1, 4))
   t.markup.up.extend(['1/4', '1/6'])
   assert t.format == "c'4 ^ \markup { \column { 1/4 1/6 } }"
   r'''
   c'4 ^ \markup { \column { 1/4 1/6 } }
   '''


def test_MarkupInterface_07( ):
   '''Clear all up-markup.'''
   t = Note(0, (1, 4))
   t.markup.up.extend(['A', 'B', 'C'])
   t.markup.up = [ ]
   assert t.format == "c'4"
   r'''
   c'4
   '''


def test_MarkupInterface_08( ):
   '''Clear all down-markup.'''
   t = Note(0, (1, 4))
   t.markup.down.extend(['A', 'B', 'C'])
   t.markup.down = [ ]
   assert t.format == "c'4"
   r'''
   c'4
   '''
