from abjad import *
from abjad.checks import IntermarkedHairpinCheck
from abjad.checks import ShortHairpinCheck


def test_Hairpin_01( ):
   '''Hairpins span adjacent leaves.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[:4])

   assert componenttools.is_well_formed_component(t)
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


def test_Hairpin_02( ):
   '''Hairpins spanning a single leaf are allowed but not well-formed.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[0 : 1])
   checker = ShortHairpinCheck( )

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


def test_Hairpin_03( ):
   '''Hairpins and dynamics apply separately.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[ : 4])
   t[0].dynamics.mark = 'p'
   t[3].dynamics.mark = 'f'

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8 \\p \\<\n\tcs'8\n\td'8\n\tef'8 \\f\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \p \<
           cs'8
           d'8
           ef'8 \f
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_Hairpin_04( ):
   '''Internal marks are allowed but not well-formed.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(t[ : 4])
   t[2].dynamics.mark = 'p'
   checker = IntermarkedHairpinCheck( )

   assert not checker.check(t)
   assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8 \\p\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 \<
           cs'8
           d'8 \p
           ef'8 \!
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_Hairpin_05( ):
   '''Apply back-to-back hairpins separately.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t[0].dynamics.mark = 'p'
   Crescendo(t[0 : 3])
   t[2].dynamics.mark = 'f'
   Decrescendo(t[2 : 5])
   t[4].dynamics.mark = 'p'
   Crescendo(t[4 : 7])
   t[6].dynamics.mark = 'f'

   assert t.format == "\\new Staff {\n\tc'8 \\p \\<\n\tcs'8\n\td'8 \\f \\>\n\tef'8\n\te'8 \\p \\<\n\tf'8\n\tfs'8 \\f\n\tg'8\n}"
   assert componenttools.is_well_formed_component(t)

   r'''
   \new Staff {
           c'8 \p \<
           cs'8
           d'8 \f \>
           ef'8
           e'8 \p \<
           f'8
           fs'8 \f
           g'8
   }
   '''


def test_Hairpin_06( ):
   '''Hairpins format rests.'''

   t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(t[ : ])

   assert t.format == "\\new Staff {\n\tr8 \\<\n\tr8\n\tr8\n\tr8\n\te'8\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
   assert componenttools.is_well_formed_component(t)

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


def test_Hairpin_07( ):
   '''Trim hairpins format only notes and chords.'''

   t = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(t[:], trim = True)

   r'''
   \new Staff {
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

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n\te'8 \\<\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"


def test_Hairpin_08( ):
   '''Trim hairpins format only notes and chords.'''

   t = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
   Crescendo(t[ : ], trim = True)

   assert t.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\tr8\n\tr8\n\tr8\n\tr8\n}"
   assert componenttools.is_well_formed_component(t)

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


def test_Hairpin_09( ):
   '''Trim hairpins with dynamic marks behave as expected.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Rest(t[0])
   Rest(t[-1])
   Hairpin(t.leaves, 'p < f', trim = True)

   assert len(t[0].dynamics.spanner.components) == len(t)
   assert t.format == "\\new Staff {\n\tr8\n\tcs'8 \\< \\p\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8 \\f\n\tr8\n}"
   checker = IntermarkedHairpinCheck( )
   assert checker.check(t)

   r'''
   \new Staff {
           r8
           cs'8 \< \p
           d'8
           ef'8
           e'8
           f'8
           fs'8 \f
           r8
   }
   '''
