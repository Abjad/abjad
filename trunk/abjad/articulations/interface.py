from .. core.interface import _Interface

class ArticulationsInterface(list, _Interface):

   def __init__(self, client, articulations = [ ]):
      _Interface.__init__(self, client, 'Articulations')
      self.extend(articulations)

   def __repr__(self):
      if len(self):
         return 'Articulations(%s)' % ', '.join(self)
      else:
         return 'Articulations( )'

   @property
   def _right(self):
      result = [ ]
      result.extend(['\\' + x for x in self])
      return result
