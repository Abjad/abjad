from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface


class BeamInterface(_Interface, _FormatContributor):

   def __init__(self, client):
      _Interface.__init__(self, client)
      _FormatContributor.__init__(self)
