from abjad import *


def test_harmonictools_add_artificial_01( ):
   '''Adds a perfect fourth by default.'''

   t = Note(0, (1, 4))
   t = harmonictools.add_artificial(t)
   assert t.format == "<\n\tc'\n\t\\tweak #'style #'harmonic\n\tf'\n>4"

   r'''<
           c'
           \tweak #'style #'harmonic
           f'
   >4'''


def test_harmonictools_add_artificial_02( ):
   '''Specify other diatonic intervals as a string.'''

   t = Note(0, (1, 4))
   t = harmonictools.add_artificial(t, 'minor third')
   assert t.format == "<\n\tc'\n\t\\tweak #'style #'harmonic\n\tef'\n>4"

   r'''<
           c'
           \tweak #'style #'harmonic
           ef'
   >4'''


def test_harmonictools_add_artificial_03( ):
   '''Works in staves.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   harmonictools.add_artificial(t[2])
   assert t.format == "\\new Staff {\n\tc'8\n\tcs'8\n\t<\n\t\td'\n\t\t\\tweak #'style #'harmonic\n\t\tg'\n\t>8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''\new Staff {
           c'8
           cs'8
           <
                   d'
                   \tweak #'style #'harmonic
                   g'
           >8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }'''
