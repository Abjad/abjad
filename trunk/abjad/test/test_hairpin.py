from abjad import *


def test_hairpin_01( ):
   '''Hairpins span adjacent leaves.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
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
   '''Hairpins may span a single leaf;
      but tester will grumble.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[0 : 1])
   assert not staff.tester.testShortHairpins(ret = True)
   assert staff.format == "\\new Staff {\n\tc'8 \\< \\!\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
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
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   staff[0].dynamics = 'p'
   staff[3].dynamics = 'f'
   assert staff.tester.testAll(ret = True)
   assert staff.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8\n\tef'8 \\fX\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
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
   '''Internal marks are allowed; 
      but tester will grumble.'''
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   Crescendo(staff[ : 4])
   staff[2].dynamics = 'p'
   assert not staff.tester.testIntermarkedHairpins(ret = True)
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8 \\pX\n\tef'8 \\!\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"
   '''
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
   staff = Staff([Note(n, (1, 8)) for n in range(8)])
   staff[0].dynamics = 'p'
   Crescendo(staff[0 : 3])
   staff[2].dynamics = 'f'
   Decrescendo(staff[2 : 5])
   staff[4].dynamics = 'p'
   Crescendo(staff[4 : 7])
   staff[6].dynamics = 'f'
   assert staff.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8 \\fX \\>\n\tef'8\n\te'8 \\pX \\<\n\tf'8\n\tfs'8 \\fX\n\tg'8\n}"
   assert staff.tester.testAll(ret = True)
   '''
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
   staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(staff[ : ])
   assert staff.format == "\\new Staff {\n\tr8 \\<\n\tr8\n\tr8\n\tr8\n\te'8\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
   assert staff.tester.testAll(ret = True)
   '''
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
   staff = Staff(Rest((1, 8)) * 4 + [Note(n, (1, 8)) for n in range(4, 8)])
   Crescendo(staff[ : ], fit = 'trim')
   assert staff.format == "\\new Staff {\n\tr8\n\tr8\n\tr8\n\tr8\n\te'8 \\<\n\tf'8\n\tfs'8\n\tg'8 \\!\n}"
   assert staff.tester.testAll(ret = True)
   '''
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


def test_hairpins_08( ):
   '''Trim hairpins format only notes and chords.'''
   staff = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
   Crescendo(staff[ : ], fit = 'trim')
   assert staff.format == "\\new Staff {\n\tc'8 \\<\n\tcs'8\n\td'8\n\tef'8 \\!\n\tr8\n\tr8\n\tr8\n\tr8\n}"
   assert staff.tester.testAll(ret = True)
   '''
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
   '''Trim hairpins with dynamic marks behave as expected;
      TODO change testIntermarkedHairpins to account for trims.'''
   staff = Staff([Note(n, (1, 8)) for n in range(4)] + Rest((1, 8)) * 4)
   Hairpin(staff.leaves, 'p', '<', 'f', fit = 'trim')
   assert staff.format == "\\new Staff {\n\tc'8 \\pX \\<\n\tcs'8\n\td'8\n\tef'8 \\fX\n\tr8\n\tr8\n\tr8\n\tr8\n}"
   assert not staff.tester.testIntermarkedHairpins(ret = True)
   '''
   \new Staff {
           c'8 \pX \<
           cs'8
           d'8
           ef'8 \fX
           r8
           r8
           r8
           r8
   }
   '''
