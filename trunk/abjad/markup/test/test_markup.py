from abjad import *


def test_markup_01( ):
   '''Append integer.'''
   t = Note(0, (1, 4))
   t.markup.down.append(12)
   assert t.format == "c'4 _ \\markup { 12 }"
   r'''
   c'4 _ \markup { 12 }
   '''


def test_markup_02( ):
   '''Append string.'''
   t = Note(0, (1, 4))
   t.markup.down.append('12')
   assert t.format == "c'4 _ \\markup { 12 }"
   r'''
   c'4 _ \markup { 12 }
   '''
   

def test_markup_03( ):
   '''Both up and down.'''
   t = Note(0, (1, 4))
   t.markup.up.append('foo')
   t.markup.down.append('bar')
   assert t.format == "c'4 ^ \\markup { foo } _ \\markup { bar }"
   r'''
   c'4 ^ \markup { foo } _ \markup { bar }
   '''


def test_markup_04( ):
   '''Append string with LilyPond formatting command.'''
   t = Note(0, (1, 4))
   t.markup.up.append(r'\italic { attaca! }')
   assert t.format == "c'4 ^ \\markup { \\italic { attaca! } }"
   r'''
   c'4 ^ \markup { \italic { attaca! } }
   '''
