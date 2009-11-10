from abjad.leaf import _Leaf
from abjad.measure.measure import _Measure
from abjad.rational import Rational


class VerticalMoment(object):
   r'''Everything happening at a single moment in musical time.
   '''

   def __init__(self, prolated_offset, governors, components):
      assert isinstance(prolated_offset, Rational)
      assert isinstance(governors, tuple)
      assert isinstance(components, tuple)
      self._prolated_offset = prolated_offset
      self._governors = tuple(governors)
      self._components = tuple(components)

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, VerticalMoment):
         if len(self) == len(expr):
            for c, d in zip(self.components, expr.components):
               if c is not d:
                  return False
            else:
               return True
      return False

   def __len__(self):
      return len(self.components)

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      contents = ', '.join([str(x) for x in self.components])
      return '%s(%s)' % (self.__class__.__name__, contents)

   ## PUBLIC ATTRIBUTES ##

   @property
   def components(self):
      '''Read-only tuple of zero or more components
      happening at vertical moment.

      It is always the case that ``self.components = 
      self.overlap_components + self.start_components``.'''
      return self._components

   @property
   def governors(self):
      '''Read-only tuple of one or more containers
      in which vertical moment is evaluated.'''
      return self._governors

   @property
   def leaves(self):
      '''Read-only tuple of zero or more leaves
      at vertical moment.'''
      result = [ ]
      for component in self.components:
         if isinstance(component, _Leaf):
            result.append(component)
      result = tuple(result)
      return result

   @property
   def measures(self):
      '''Read-only tuplet of zero or more measures
      at vertical moment.'''
      result = [ ]
      for component in self.components:
         if isinstance(component, _Measure):
            result.append(component)
      result = tuple(result)
      return result

   @property
   def prolated_offset(self):
      '''Read-only rational-valued score offset
      at which vertical moment is evaluated.'''
      return self._prolated_offset
   
   @property
   def overlap_components(self):
      '''Read-only tuple of components in vertical moment
      starting before vertical moment, ordered by score index.'''
      result = [ ]
      for component in self.components:
         if component.offset.prolated.start < self.prolated_offset:
            result.append(component)
      result = tuple(result)
      return result

   @property
   def overlap_leaves(self):
      '''Read-only tuple of leaves in vertical moment
      starting before vertical moment, ordered by score index.'''
      result = [x for x in self.overlap_components if isinstance(x, _Leaf)]
      result = tuple(result)
      return result

   @property
   def overlap_measures(self):
      '''Read-only tuple of measures in vertical moment
      starting before vertical moment, ordered by score index.'''
      result = [x for x in self.overlap_components if isinstance(x, _Measure)]
      result = tuple(result)
      return result

   @property
   def start_components(self):
      '''Read-only tuple of components in vertical moment
      starting with at vertical moment, ordered by score index.'''
      result = [ ]
      for component in self.components:
         if component.offset.prolated.start == self.prolated_offset:
            result.append(component)
      result = tuple(result)
      return result

   @property
   def start_leaves(self):
      '''Read-only tuple of leaves in vertical moment
      starting with vertical moment, ordered by score index.'''
      result = [x for x in self.start_components if isinstance(x, _Leaf)]
      result = tuple(result)
      return result
