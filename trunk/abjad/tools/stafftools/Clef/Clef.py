from abjad.core import _StrictComparator
from abjad.core import _Immutable


class Clef(_StrictComparator, _Immutable):

   __slots__ = ('_name', )

   def __init__(self, name = 'treble'):
      object.__setattr__(self, '_name', name)

   ## OVERLOADS ##

   def __eq__(self, arg):
      return arg == self.name
   
   def __repr__(self):
      return "%s('%s')" % (self.__class__.__name__, self.name)

   def __str__(self):
      return self.name

   ## PRIVATE ATTRIBUTES ##

   _clef_name_to_middle_c_position = { 'treble': -6, 'alto': 0, 'tenor': 2, 'bass': 6, }

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\clef "%s"' % self.name

   @property
   def middle_c_position(self):
      return self._clef_name_to_middle_c_position[self.name]

   @property
   def name(self):
      return self._name
