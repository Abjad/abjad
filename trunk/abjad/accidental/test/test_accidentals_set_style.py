from abjad import *


def test_accidentals_01( ):
   '''set-accidental-style works in voices.'''

   t = Voice([Note(n, (1, 8)) for n in range(8)])
   t.accidentals = 'forget'

   assert t.format == "\\new Voice {\n\t#(set-accidental-style 'forget)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Voice {
           #(set-accidental-style 'forget)
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''
   

def test_accidentals_02( ):
   '''set-accidental-style works in staves.'''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   t.accidentals = 'forget'

   assert t.format == "\\new Staff {\n\t#(set-accidental-style 'forget)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           #(set-accidental-style 'forget)
           c'8
           cs'8
           d'8
           ef'8
           e'8
           f'8
           fs'8
           g'8
   }
   '''


def test_accidentals_03( ):
   '''set-accidental-style works in tuplets.'''

   t = FixedDurationTuplet((2, 8), Note(0, (1, 8)) * 3)
   t.accidentals = 'forget'

   assert t.format == "\\times 2/3 {\n\t#(set-accidental-style 'forget)\n\tc'8\n\tc'8\n\tc'8\n}"

   r'''
   \times 2/3 {
           #(set-accidental-style 'forget)
           c'8
           c'8
           c'8
   }
   '''


def test_accidentals_04( ):
   '''set-accidental-style works in pure containers.'''

   t = Container([Note(n, (1, 8)) for n in range(8)])
   t.accidentals = 'forget'

   assert t.format == "\t#(set-accidental-style 'forget)\n\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8"

   r'''
        #(set-accidental-style 'forget)
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
   '''


def test_accidentals_05( ):
   '''Use None to clear set-accidental-style.'''

   t = Container([Note(n, (1, 8)) for n in range(8)])
   t.accidentals = 'forget'
   t.accidentals = None

   assert t.format == "\tc'8\n\tcs'8\n\td'8\n\tef'8\n\te'8\n\tf'8\n\tfs'8\n\tg'8"

   r'''
        c'8
        cs'8
        d'8
        ef'8
        e'8
        f'8
        fs'8
        g'8
   '''
