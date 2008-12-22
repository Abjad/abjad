from abjad import *
from abjad.checks import HairpinsIntermarked
from abjad.checks import HairpinsShort


def test_hairpin_01( ):
   '''Hairpins span adjacent leaves.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[ : 4])

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_hairpins_02( ):
   '''Hairpins spanning a single leaf are allowed but not well-formed.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[0 : 1])
   checker = HairpinsShort( )

   assert not checker.check(t)
   assert t.format == "\\new Staff {\n\tc'8 \\< \\!\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \< \!
           cs'8
           d'8
           ef'8 
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_hairpins_03( ):
   '''Hairpins and dynamics apply separately.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[ : 4])
   t[0].dynamics = 'p'
   t[3].dynamics = 'f'

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8\n\tef'8 \\fX\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \pX \<
           cs'8
           d'8
           ef'8 \fX
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_hairpins_04( ):
   '''Internal marks are allowed but not well-formed.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[ : 4])
   t[2].dynamics = 'p'
   checker = HairpinsIntermarked( )

   assert not checker.check(t)
   assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8 \\pX\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8 \pX
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_hairpins_05( ):
   '''Apply back-to-back hairpins separately.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t[0].dynamics = 'p'
   Crescendo(t[0 : 3])
   t[2].dynamics = 'f'
   Decrescendo(t[2 : 5])
   t[4].dynamics = 'p'
   Crescendo(t[4 : 7])
   t[6].dynamics = 'f'

   assert t.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8 \\fX \\>\n\tef'8\n\te'8 \\pX \\<\n\tf'8\n\tfs'8 \\fX\n\tg'8\n}"
   assert check(t)

   r'''
   \new Staff {
           c'8 \pX \<
           cs'8
           d'8 \fX \>
           ef'8
           e'8 \pX \<
           f'8
           fs'8 \fX
           g'8
   }
   '''


def test_hairpins_06( ):
   '''Hairpins format rests.'''

   t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(t[ : ])

   assert t.format == "\\new Staff {\n\tr8 \\<\n\tr8\n\tr8\n\tr8\n\te'8\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
   assert check(t)

   r'''
   \new Staff {
           r8 \<
           r8
           r8
           r8
           e'8
           f'8
           fs'8
           g'8 \!
   }
   '''


def test_hairpins_07( ):
   '''Trim hairpins format only notes and chords.'''

   t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(t[ : ], trim = True)

   assert t.format == "\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n\te'8 \\<\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
   assert check(t)

   '''
   r\new Staff {
           r8
           r8
           r8
           r8
           e'8 \<
           f'8
           fs'8
           g'8 \!
   }
   '''


def test_hairpins_08( ):
   '''Trim hairpins format only notes and chords.'''

   t = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
   Crescendo(t[ : ], trim = True)

   assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\tr8\n\tr8\n\tr8\n\tr8\n}"
   assert check(t)

   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8
           ef'8 \!
           r8
           r8
           r8
           r8
   }
   '''


def test_hairpins_09( ):
   '''
   Trim hairpins with dynamic marks behave as expected;
   TODO change testIntermarkedHairpins to account for trims.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Rest(t[0])
   Rest(t[-1])
   #Hairpin(t, 'p < f', trim = True)
   Hairpin(t.leaves, 'p < f', trim = True)

   assert len(t[0].dynamics.spanner.components) == len(t)
   assert t.format == "\\new Staff {\n\tr8\n\tcs'8 \\< \\pX\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8 \\fX\n\tr8\n}"
   checker = HairpinsIntermarked( )
   assert checker.check(t)

   r'''
   \new Staff {
           r8
           cs'8 \< \pX
           d'8
           ef'8
           e'8
           f'8
           fs'8 \fX
           r8
   }
   '''
