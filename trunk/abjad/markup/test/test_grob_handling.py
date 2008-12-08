from abjad import *


def test_markup_grob_handling_01( ):
   '''Grob override with up-markup.'''
   t = Note(0, (1, 4))
   t.markup.up.append(12)
   t.markup.color  = 'red'
   assert t.format == "\\once \\override TextScript #'color = #red\nc'4 ^ \\markup { 12 }"
   r'''
   \once \override TextScript #'color = #red
   c'4 ^ \markup { 12 }
   '''


def test_markup_grob_handling_02( ):
   '''Grob override with down-markup.'''
   t = Note(0, (1, 4))
   t.markup.down.append(12)
   t.markup.color  = 'red'
   assert t.format == "\\once \\override TextScript #'color = #red\nc'4 _ \\markup { 12 }"
   r'''
   \once \override TextScript #'color = #red
   c'4 _ \markup { 12 }
   '''


def test_markup_grob_handling_03( ):
   '''Grob override with no markup.'''
   t = Note(0, (1, 4))
   t.markup.color = 'red'
   assert t.format == "\\once \\override TextScript #'color = #red\nc'4"
   r'''
   \once \override TextScript #'color = #red
   c'4
   '''
   

def test_markup_grob_handling_04( ):
   '''Staff padding grob override.'''
   t = Note(0, (1, 4))
   t.markup.down.append(12)
   t.markup.staff_padding = 4
   assert t.format == "\\once \\override TextScript #'staff-padding = #4\nc'4 _ \\markup { 12 }"
   r'''
   \once \override TextScript #'staff-padding = #4
   c'4 _ \markup { 12 }
   '''
