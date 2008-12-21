from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname


class _ComponentSpannerAggregator(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      self._spanners = [ ]

   ### PRIVATE METHODS ###

   def _filter(self, result, classname = None, selector = None):
      if classname is not None:
         result = [p for p in result if hasname(p, classname)]
      if selector is not None:
         result = filter(selector, result)
      return result

   ### PUBLIC METHODS ###

   def mine(self, classname = None, selector = None):
      result = self._spanners[ : ]
      return self._filter(result, classname, selector)
