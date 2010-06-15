from abjad import *


def test_KeySignatureInterface_effective_01( ):
   '''Force a key signature.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   key_signature = KeySignature('c', 'major')
   t.key_signature.forced = key_signature

   r'''
   \new Staff {
           \key c \major
           c'8
           d'8
           e'8
           f'8
   }
   '''

   assert t.key_signature.effective == KeySignature('c', 'major')
   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\t\\key c \\major\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"

   
def test_KeySignatureInterface_effective_02( ):
   '''There is no default key signature.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   assert t.key_signature.effective is None
