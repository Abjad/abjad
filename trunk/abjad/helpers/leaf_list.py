from abjad.chord.chord import Chord
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.leaf.leaf import _Leaf
from abjad.note.note import Note
from abjad.rational.rational import Rational
from abjad.rest.rest import Rest
from abjad.skip.skip import Skip


def leaf_list(leaf_token, duration_token):
   '''Return big-endian list of leaves.
      leaf_token may be a leaf type equal to Note, Rest, Chord or Skip,
      or else a leaf instance of type Note, Rest, Chord or Skip.

      abjad> leaf_list(Rest, (9, 16))
      [Rest(2), Rest(16)]

      See /test/leaf_list_test.py for more examples.'''

   duration_tokens = _duration_token_decompose(duration_token)

   if isinstance(leaf_token, _Leaf):
      leaves = leaf_token * len(duration_tokens)
      for leaf, dt in zip(leaves, duration_tokens):
         #leaf.duration = dt
         #leaf.duration.written = dt
         leaf.duration.written = Rational(*dt)
   elif leaf_token == Note:
      leaves = [leaf_token(None, dt) for dt in duration_tokens]
   elif leaf_token == Chord:
      leaves = [leaf_token([ ], dt) for dt in duration_tokens]
   elif leaf_token in (Rest, Skip):
      leaves = [leaf_token(dt) for dt in duration_tokens]
   else:
      raise ValueError('leaf token must be leaf instance or leaf type.')

   return leaves
