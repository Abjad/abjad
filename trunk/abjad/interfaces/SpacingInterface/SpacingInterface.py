from abjad.core import _FormatContributor
from abjad.interfaces._Interface import _Interface


class SpacingInterface(_Interface, _FormatContributor):

   def __init__(self, _client):
      _Interface.__init__(self, _client)
      _FormatContributor.__init__(self)
