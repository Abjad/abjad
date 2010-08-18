from abjad import *


def test_MarkupInterface__direction_to_format_string_01( ):
   '''Works with markup objects.'''

   t = Note(0, (1, 4))
   t.markup.up.append(markuptools.Markup('foo'))
   assert t.markup._direction_to_format_string('up') == '\\markup { foo }'


def test_MarkupInterface__direction_to_format_string_02( ):
   '''Works with strings.'''

   t = Note(0, (1, 4))
   t.markup.up.append('foo')
   assert t.markup._direction_to_format_string('up') == '\\markup { foo }'


def test_MarkupInterface__direction_to_format_string_03( ):
   '''Works with numbers.'''

   t = Note(0, (1, 4))
   t.markup.up.append(1)
   assert t.markup._direction_to_format_string('up') == '\\markup { 1 }'
