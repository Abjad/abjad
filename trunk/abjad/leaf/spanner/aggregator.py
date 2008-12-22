from abjad.helpers.hasname import hasname
from abjad.component.spanner.aggregator import _ComponentSpannerAggregator
from abjad.core.interface import _Interface


class _LeafSpannerAggregator(_ComponentSpannerAggregator):

   ### PRIVATE ATTRIBUTES ###

   @property
   def _after(self):
      result = [ ]
      #for spanner in self:
      for spanner in self.total( ):
         result.extend(spanner._after(self._client))
      return result

   @property
   def _before(self):
      result = [ ]
      #for spanner in self:
      for spanner in self.total( ):
         result.extend(spanner._before(self._client))
      return result

   @property
   def _left(self):
      result = [ ]
      #for spanner in self:
      for spanner in self.total( ):
         result.extend(spanner._left(self._client))   
      return result

   @property
   def _right(self):
      result = [ ]
      #for spanner in self:
      for spanner in self.total( ):
         result.extend(spanner._right(self._client))
      return result

   ### PRIVATE METHODS ####

   def _append(self, spanner):
      if spanner not in self._spanners:
         self._spanners.append(spanner)

   #def _fuseLeft(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fuseLeft(self, grob = None, attribute = None, value = None):
      result = [ ]
      #spanners = self.get(interface, grob, attribute, value)
      spanners = self.get(grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'left'))
      return result

   #def _fuseRight(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fuseRight(self, grob = None, attribute = None, value = None):
      result = [ ]
      #spanners = self.get(interface, grob, attribute, value)
      spanners = self.get(grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'right'))
      return result

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

   #def _getYoungestSpanner(self, 
   #   classname = None, interface = None, 
   #   grob = None, attribute = None, value = None):
   def _getYoungestSpanner(self, 
      classname = None, grob = None, attribute = None, value = None):
      #spanners = self.get(classname, interface, grob, attribute, value)
      spanners = self.get(classname, grob, attribute, value)
      #spanners.sort(lambda x, y: cmp(y[0].offset, x[0].offset))
      spanners.sort(lambda x, y: cmp(y[0].offset.score, x[0].offset.score))
      if spanners:
         return spanners[0]
      else:
         return None

   ### PUBLIC METHODS ###

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

#   def fracture(self, direction = 'both'):
#      result = [ ]
#      client = self._client
#      if direction in ('left', 'both'):
#         for spanner in self.mine( ):
#            result.append(spanner.fracture(spanner.index(client), 'left'))
#      if direction in ('right', 'both'):
#         for spanner in self.mine( ):
#            result.append(spanner.fracture(spanner.index(client), 'right'))
#      return result
         
#   #def fuse(self, 
#   #   interface = None, grob = None, attribute = None, value = None,
#   def fuse(self, grob = None, attribute = None, value = None,
#      direction = 'both'):
#      result = [ ]
#      #if direction == 'left':
#      #   result.extend(self._fuseLeft(interface, grob, attribute, value))
#      #elif direction == 'right':
#      #   result.extend(self._fuseRight(interface, grob, attribute, value))
#      #elif direction == 'both':
#      #   result.extend(self._fuseLeft(interface, grob, attribute, value))
#      #   result.extend(self._fuseRight(interface, grob, attribute, value))
#      if direction == 'left':
#         result.extend(self._fuseLeft(grob, attribute, value))
#      elif direction == 'right':
#         result.extend(self._fuseRight(grob, attribute, value))
#      elif direction == 'both':
#         result.extend(self._fuseLeft(grob, attribute, value))
#         result.extend(self._fuseRight(grob, attribute, value))
#      return result

   def fuse(self, direction = 'both', klass = None):
      result = [ ]
      ### TODO - iterate over my spanners only once
      if direction in ('left', 'both'):
         for spanner in self.mine(klass):
            result.append(spanner.fuse(direction = 'left'))
      if direction in ('right', 'both'):
         for spanner in self.mine(klass):
            result.append(spanner.fuse(direction = 'right'))
      return result

   ### TODO - remove or reimplement get( )
   ###        Do we need t.spanners.above.get( ), t.spanners.mine.get( ),
   ###        etc.?

   ###        Or maybe just t.spanners.above(**kwargs)
   ###        and t.spanners.mine(**kwargs)?

   def get(self, classname = None, grob = None, attribute = None, value = None):
      #result = self[ : ]
      result = self.mine( )
      if classname:
          result = [
            spanner for spanner in result
            if hasname(spanner, classname)]
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

   def last(self, classname = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname = classname, 
         grob = grob, attribute = attribute, value = value)
      if spanners:
         return spanners[-1]
      else:
         return None

   def total(self, classname = None, selector = None):
      result = [ ]
      parentage = self._client._parentage._iparentage
      for component in parentage:
         result.extend(component.spanners._spanners)
      return self._filter(result, classname, selector)
