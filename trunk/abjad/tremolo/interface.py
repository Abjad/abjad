from .. core.interface import _Interface

class TremoloInterface(_Interface):

   def __init__(self, client, subdivision = None):
      _Interface.__init__(self, client, 'Tremolo')
      self._subdivision = subdivision

   ### ACCESSORS ###

   def clear(self):
      self._subdivision = None

   def setSubdivision(self, subdivision):
      self._subdivision = subdivision

   def __repr__(self):
      if self._subdivision:
         return 'Tremolo(%s)' % self._subdivision
      else:
         return 'Tremolo( )'

   ### FORMATTING ###

   @property
   def body(self):
      if self._subdivision:
         return ':' + str(self._subdivision)
      else:
         return ''
