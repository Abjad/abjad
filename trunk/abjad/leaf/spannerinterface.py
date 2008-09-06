### TODO - create abstract _SpannerInterface class;
###        derive both this _LeafSpannerInterface and
###        also _ContainerSpannerInterface from _SpannerInterface.

from .. helpers.hasname import hasname
from .. core.interface import _Interface
from .. core.parser import _Parser

class _LeafSpannerInterface(object):

   def __init__(self, client):
      self._client = client
      self._parser = _Parser( )
      self._spanners = [ ]

   ### REPR ###

   def __repr__(self):
      if len(self) == 0:
         return '%s( )' % self.__class__.__name__
      else:
         return '%s(%s)' % (self.__class__.__name__, len(self))

   ### OVERRIDES ###

   def __contains__(self, expr):
      return expr in self._spanners

   def __getitem__(self, i):
      return self._spanners[i]

   ### TODO - deprecate getslice in favor of getitem ###

   def __getslice__(self, i, j):
      return self._spanners[i : j]

   ### TODO - implement slice inside delitem ###

   def __delitem__(self, i):
      self._spanners[i]._sever( )

   def __len__(self):
      return len(self._spanners)

   ### HANDLERS ####

   def append(self, spanner):
      if spanner not in self:
         self._spanners.append(spanner)

   def get(self, 
      classname = None, interface = None, 
      grob = None, attribute = None, value = None):
      result = self[ : ]
      if classname:
          result = [
            spanner for spanner in result
            if hasname(spanner, classname)]
      if interface:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_interface') and
            spanner._interface == interface]
      if grob:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_grob') and
            spanner._grob == grob]
      if attribute:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_attribute') and 
            spanner._attribute == attribute]
      if value:
         result = [
            spanner for spanner in result
            if hasattr(spanner, '_value') and
            spanner._value == value]
      return result

   def _getYoungestSpanner(self, 
      classname = None, interface = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname, interface, grob, attribute, value)
      #spanners.sort(lambda x, y: cmp(y.leaves[0].offset, x.leaves[0].offset))
      spanners.sort(lambda x, y: cmp(y[0].offset, x[0].offset))
      if spanners:
         return spanners[0]
      else:
         return None

   def _getNaiveValue(self, grob, attribute):
      spanner = self._getYoungestSpanner(grob = grob, attribute = attribute)
      if spanner:
         return spanner._value
      else:
         return None

   def _getSophisticatedValue(self, grob, attribute):
      '''Get the youngest matching spanner, if any;
         for every leaf *before me* in the spanner,
         check and see if that leaf has another matching spanner;
         if so, check to see if that leaf marks the *end*
         of a matching spanner;
         if so, that means that that leaf *before me* carries
         a \revert and I return no actual value;
         otherwise, if no leaves before me carry a \revert,
         return the value of my youngest matching spanner.
         The restriction against _isMyOnlyLeaf( ) is in there
         because one-time overrides carry no \revert;
         see test_override_overlap.py for examples.'''
      spanner = self._getYoungestSpanner(grob = grob, attribute = attribute)
      if spanner:
         for i in reversed(range(spanner.index(self._client))):
            #cur = spanner.leaves[i]
            cur = spanner[i]
            candidates = cur.spanners.get(grob = grob, attribute = attribute)
            candidates = [x for x in candidates if x is not spanner]
            for candidate in candidates:
               if candidate._isMyLastLeaf(cur) and \
                  not candidate._isMyOnlyLeaf(cur):
                  return None
         return spanner._value
      else:
         return None

   def find(self, grob, attribute):
      return self._getSophisticatedValue(grob, attribute)

   def first(self, classname = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname = classname, 
         grob = grob, attribute = attribute, value = value)
      if spanners:
         return spanners[0]
      else:
         return None

   def last(self, classname = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname = classname, 
         grob = grob, attribute = attribute, value = value)
      if spanners:
         return spanners[-1]
      else:
         return None

   def die(self, 
      classname = None, interface = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname = classname, interface = interface,
         grob = grob, attribute = attribute, value = value)
      for spanner in spanners:
         spanner.die( )

   ### FORMATTING ###

   @property
   def _before(self):
      result = [ ]
      for spanner in self:
         result.extend(spanner._before(self._client))
      return result

   @property
   def _after(self):
      result = [ ]
      for spanner in self:
         result.extend(spanner._after(self._client))
      return result

   @property
   def _left(self):
      result = [ ]
      for spanner in self:
         result.extend(spanner._left(self._client))   
      return result

   @property
   def _right(self):
      result = [ ]
      for spanner in self:
         result.extend(spanner._right(self._client))
      return result

   ### SPANNER MANAGEMENT ###

   def _fractureLeft(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      spanners = self.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         #result.append(spanner.fracture(spanner.index(self), 'left'))
         result.append(spanner.fracture(spanner.index(self._client), 'left'))
      return result

   def _fractureRight(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      spanners = self.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         #result.append(spanner.fracture(spanner.index(self), 'right'))
         result.append(spanner.fracture(spanner.index(self._client), 'right'))
      return result

   def fracture(self, 
      interface = None, grob = None, attribute = None, value = None,
      direction = 'both'):
      result = [ ]
      if direction == 'left':
         result.extend(self._fractureLeft(interface, grob, attribute, value))
      elif direction == 'right': 
         result.extend(self._fractureRight(interface, grob, attribute, value))
      elif direction == 'both':
         result.extend(self._fractureLeft(interface, grob, attribute, value))
         result.extend(self._fractureRight(interface, grob, attribute, value))
      else:
         raise ValueError(
            'direction %s must be left, right or both' % direction)
      return result
         
   def _fuseLeft(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      spanners = self.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'left'))
      return result

   def _fuseRight(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      spanners = self.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'right'))
      return result

   def fuse(self, 
      interface = None, grob = None, attribute = None, value = None,
      direction = 'both'):
      result = [ ]
      if direction == 'left':
         result.extend(self._fuseLeft(interface, grob, attribute, value))
      elif direction == 'right':
         result.extend(self._fuseRight(interface, grob, attribute, value))
      elif direction == 'both':
         result.extend(self._fuseLeft(interface, grob, attribute, value))
         result.extend(self._fuseRight(interface, grob, attribute, value))
      return result
