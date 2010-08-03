from abjad import *


## TODO: Externalize numbering code to a tools module. ##

def test__LeafFormatter_number_01( ):
   '''_LeafFormatterNumberInterface can contribute markup.'''

   t = Staff(macros.scale(8))
   #t[0].formatter.number.self = 'markup'
   t[0]._formatter.number.self = 'markup'

   r'''
   \new Staff {
           c'8 ^ \markup { 0 }
           d'8
           e'8
           f'8
           g'8
           a'8
           b'8
           c''8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 ^ \\markup { 0 }\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n\tc''8\n}"


def test__LeafFormatter_number_02( ):
   '''_LeafFormatterNumberInterface can contribute LilyPond comments.'''

   t = Staff(macros.scale(8))
   #t[0].formatter.number.self = 'comment'
   t[0]._formatter.number.self = 'comment'

   r'''
   \new Staff {
           c'8 % leaf 0
           d'8
           e'8
           f'8
           g'8
           a'8
           b'8
           c''8
   }
   '''

   assert t.format == "\\new Staff {\n\tc'8 % leaf 0\n\td'8\n\te'8\n\tf'8\n\tg'8\n\ta'8\n\tb'8\n\tc''8\n}"
