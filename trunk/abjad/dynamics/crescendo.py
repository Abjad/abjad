from hairpin import _Hairpin

class Crescendo(_Hairpin):

   def __init__(self, leaves, fit = None):
      _Hairpin.__init__(self, leaves, fit = fit)
      self._shape = '<'

   @property
   def _body(self):
      return '<'
