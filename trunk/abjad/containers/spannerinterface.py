### TODO - create abstract _SpannerInterface class;
###        derive both this _ContainerSpannerInterface and
###        also _LeafSpannerInterface from _SpannerInterface;

from .. helpers.hasname import hasname

class _ContainerSpannerInterface(object):

   def __init__(self, client):
      self._client = client

   def __repr__(self):
      return '_ContainerSpannerInterface(%s)' % len(self)

   ### OVERRIDES ###

   def __contains__(self, expr):
      return expr in self.get( )

   def __getitem__(self, i):
      return self.get( )[i]

   ### TODO - deprecate getslice ###

   def __getslice__(self, i, j):
      return self.get( )[i : j]

   def __delitem__(self, i):
      self.get( )[i]._sever( )

   def __len__(self):
      return len(self.get( ))

   ### SPANNER MANAGEMENT ###

   def get(self, classname = None, interface = None, 
      grob = None, attribute = None, value = None):
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

   def _fuseLeft(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      left = self._client.leaves[0]
      spanners = left.spanners.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'left'))
      return result

   def _fuseRight(self, 
      interface = None, grob = None, attribute = None, value = None):
      result = [ ]
      right = self._client.leaves[-1]
      spanners = right.spanners.get(interface, grob, attribute, value)
      for spanner in spanners[ : ]:
         result.append(spanner.fuse(direction = 'right'))
      return result

   def fuse(self, 
      interface = None, grob = None, attribute = None, value = None,
      direction = 'both'):
      result = [ ]
      left, right = self._client.leaves[0], self._client.leaves[-1]
      if direction == 'left':
         result.extend(
            left.spanners.fuse(interface, grob, attribute, value, 'left'))
      elif direction == 'right':
         result.extend(
            right.spanners.fuse(interface, grob, attribute, value, 'right'))
      elif direction == 'both':
         result.extend(
            left.spanners.fuse(interface, grob, attribute, value, 'left'))
         result.extend(
            right.spanners.fuse(interface, grob, attribute, value, 'right'))
      #result.extend(left.spanners.fuseLeft(interface, grob, attribute, value))
      #result.extend(right.spanners.fuseRight(interface, grob, attribute, value))
      return result

   def _fractureLeft(self, 
      interface = None, grob = None, attribute = None, value = None):
      if len(self._client.leaves) > 0:
         #return self._client.leaves[0].spanners.fractureLeft(
         #   interface, grob, attribute, value)
         return self._client.leaves[0].spanners.fracture(
            interface, grob, attribute, value, 'left')
      else:
         return [ ]

   def _fractureRight(self, 
      interface = None, grob = None, attribute = None, value = None):
      if len(self._client.leaves) > 0:
         #return self._client.leaves[-1].spanners.fractureRight(
         #   interface, grob, attribute, value)
         return self._client.leaves[-1].spanners.fracture(
            interface, grob, attribute, value, 'right')
      else:
         return [ ]

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
            'direction %s must be left, right or both.' % direction)
      #result.extend(self.fractureLeft(interface, grob, attribute, value))
      #result.extend(self.fractureRight(interface, grob, attribute, value))
      return result

   def die(self, 
      classname = None, interface = None, 
      grob = None, attribute = None, value = None):
      spanners = self.get(classname = classname, interface = interface,
         grob = grob, attribute = attribute, value = value)
      for spanner in spanners:
         spanner.die( )
