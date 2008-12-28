#from abjad.component.component import _Component
#from abjad.core.abjadcore import _Abjad
#from abjad.helpers.hasname import hasname
#from abjad.helpers.instances import instances
#from abjad.rational.rational import Rational
#from copy import copy as python_copy
from abjad.core.grobhandler import _GrobHandler
from abjad.spanner.spanner import Spanner


class _GrobHandlerSpanner(Spanner, _GrobHandler):

   def __init__(self, grob, music = None):
      Spanner.__init__(self, music)
      _GrobHandler.__init__(self, grob)

   ### PRIVATE METHODS ###

   def _after(self, component):
      result = [ ]
      if self._isMyLastLeaf(component):
         result.extend(self._grobReverts)
      return result

   def _before(self, component):
      result = [ ]
      if self._isMyFirstLeaf(component):
         result.extend(self._grobOverrides)
      return result
