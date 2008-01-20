from .. core.interface import _Interface

class StemInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Stem', ['Stem'])
