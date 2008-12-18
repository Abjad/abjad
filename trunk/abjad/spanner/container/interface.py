from abjad.core.interface import _Interface
from abjad.helpers.hasname import hasname


### TODO - create abstract _SpannerInterface class;
###        derive both this _ContainerSpannerInterface and
###        also _LeafSpannerInterface from _SpannerInterface;

class _ContainerSpannerInterface(_Interface):

   def __init__(self, client):
      _Interface.__init__(self, client)
      # added to hold references to container spanners
      # as opposed to leaf spanners obtained by self.get( )
      self._spanners = [ ]

   ### OVERLOADS ###

   def __contains__(self, expr):
      return expr in self.get( )

   def __delitem__(self, i):
      self.get( )[i]._sever( )

   def __getitem__(self, i):
      return self.get( )[i]

   ### TODO - deprecate getslice ###

   def __getslice__(self, i, j):
      return self.get( )[i : j]

   def __len__(self):
      return len(self.get( ))

   ### PRIVATE METHODS ###

   def _append(self, spanner):
      if spanner not in self._spanners:
         self._spanners.append(spanner)

   #def _fractureLeft(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fractureLeft(self, grob = None, attribute = None, value = None):
      if len(self._client.leaves) > 0:
         #return self._client.leaves[0].spanners.fractureLeft(
         #   interface, grob, attribute, value)
         #return self._client.leaves[0].spanners.fracture(
         #   interface, grob, attribute, value, 'left')
         return self._client.leaves[0].spanners.fracture(
            grob, attribute, value, 'left')
      else:
         return [ ]

   #def _fractureRight(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fractureRight(self, grob = None, attribute = None, value = None):
      if len(self._client.leaves) > 0:
         #return self._client.leaves[-1].spanners.fractureRight(
         #   interface, grob, attribute, value)
         #return self._client.leaves[-1].spanners.fracture(
         #   interface, grob, attribute, value, 'right')
         return self._client.leaves[-1].spanners.fracture(
            grob, attribute, value, 'right')
      else:
         return [ ]

   def _fractureContainerSpannersLeft(self):
      result = [ ]
      for spanner in self._spanners[ : ]:
         result.append(spanner.fracture(spanner.index(self._client), 'left'))
      return result

   def _fractureContainerSpannersRight(self):
      result = [ ]
      for spanner in self._spanners[ : ]:
         result.append(spanner.fracture(spanner.index(self._client), 'right'))
      return result

   #def _fuseLeft(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fuseLeft(self, grob = None, attribute = None, value = None):
      result = [ ]
      left = self._client.leaves[0]
      #spanners = left.spanners.get(interface, grob, attribute, value)
      spanners = left.spanners.get(grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'left'))
      return result

   #def _fuseRight(self, 
   #   interface = None, grob = None, attribute = None, value = None):
   def _fuseRight(self, grob = None, attribute = None, value = None):
      result = [ ]
      right = self._client.leaves[-1]
      #spanners = right.spanners.get(interface, grob, attribute, value)
      spanners = right.spanners.get(grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'right'))
      return result

   ### PUBLIC METHODS ###

#   def die(self, 
#      classname = None, interface = None, 
#      grob = None, attribute = None, value = None):
   def die(self, classname = None, grob = None, attribute = None, value = None):
#      spanners = self.get(classname = classname, interface = interface,
#         grob = grob, attribute = attribute, value = value)
      spanners = self.get(classname = classname, 
         grob = grob, attribute = attribute, value = value)
      for spanner in spanners:
         spanner.die( )

   #def fracture(self, 
   #   interface = None, grob = None, attribute = None, value = None,
   #   direction = 'both'):
   def fracture(self, grob = None, attribute = None, value = None,
      direction = 'both'):
      result = [ ]
      if direction == 'left':
         #result.extend(self._fractureLeft(interface, grob, attribute, value))
         result.extend(self._fractureLeft(grob, attribute, value))
         result.extend(self._fractureContainerSpannersLeft( ))
      elif direction == 'right':
         #result.extend(self._fractureRight(interface, grob, attribute, value))
         result.extend(self._fractureRight(grob, attribute, value))
         result.extend(self._fractureContainerSpannersRight( ))
      elif direction == 'both':
         #result.extend(self._fractureLeft(interface, grob, attribute, value))
         #result.extend(self._fractureRight(interface, grob, attribute, value))
         result.extend(self._fractureLeft(grob, attribute, value))
         result.extend(self._fractureRight(grob, attribute, value))
         result.extend(self._fractureContainerSpannersLeft( ))
         result.extend(self._fractureContainerSpannersRight( ))
      else:
         raise ValueError(
            'direction %s must be left, right or both.' % direction)
      #result.extend(self.fractureLeft(interface, grob, attribute, value))
      #result.extend(self.fractureRight(interface, grob, attribute, value))
      return result

   #def fuse(self, 
   #   interface = None, grob = None, attribute = None, value = None,
   def fuse(self, grob = None, attribute = None, value = None, 
      direction = 'both'):
      result = [ ]
      left, right = self._client.leaves[0], self._client.leaves[-1]
      if direction == 'left':
         #result.extend(
         #   left.spanners.fuse(interface, grob, attribute, value, 'left'))
         result.extend(left.spanners.fuse(grob, attribute, value, 'left'))
      elif direction == 'right':
         #result.extend(
         #   right.spanners.fuse(interface, grob, attribute, value, 'right'))
         result.extend(right.spanners.fuse(grob, attribute, value, 'right'))
      elif direction == 'both':
         #result.extend(
         #   left.spanners.fuse(interface, grob, attribute, value, 'left'))
         result.extend(left.spanners.fuse(grob, attribute, value, 'left'))
         #result.extend(
         #   right.spanners.fuse(interface, grob, attribute, value, 'right'))
         result.extend(right.spanners.fuse(grob, attribute, value, 'right'))
      #result.extend(left.spanners.fuseLeft(interface, grob, attribute, value))
      #result.extend(right.spanners.fuseRight(interface, grob, attribute, value))
      return result

#   def get(self, classname = None, interface = None, 
#      grob = None, attribute = None, value = None):
   def get(self, classname = None, grob = None, attribute = None, value = None):
      result = [ ]
      for l in self._client.leaves:
         spanners = l.spanners.get( )
         for spanner in spanners:
            if spanner not in result:
               result.append(spanner)
      if classname:
         result = [
            spanner for spanner in result
            if hasname(spanner, classname)]
#      if interface:
#         result = [
#            spanner for spanner in result
#            if hasattr(spanner, '_interface') and 
#            spanner._interface == interface]
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
