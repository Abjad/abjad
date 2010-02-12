from abjad import *


def test_Scale___init___01( ):
   '''Init with tonic and mode strings.'''

   scale = tonalharmony.Scale('g', 'major')
   assert scale.key_signature == KeySignature('g', 'major')


def test_Scale___init___02( ):
   '''Init with key signature instance.'''

   key_signature = KeySignature('g', 'major')
   scale = tonalharmony.Scale(key_signature)
   assert scale.key_signature == KeySignature('g', 'major')


def test_Scale___init___03( ):
   '''Init with other scale instance.'''

   scale = tonalharmony.Scale('g', 'major')
   new = tonalharmony.Scale(scale)
   assert new.key_signature == KeySignature('g', 'major')
