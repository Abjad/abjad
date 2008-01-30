from .. core.interface import _Interface

class _ArticulationsInterface(list, _Interface):

   def __init__(self, client):
      _Interface.__init__(self, client, 'Articulations', ['Articulations'])

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
