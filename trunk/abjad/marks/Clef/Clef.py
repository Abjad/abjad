from abjad.core import _Abjad


class Clef(_Abjad):

   def __init__(self, name = 'treble'):
      #self.name = name
      super(Clef, self).__setattr__('name', name)

   ## OVERLOADS ##

   def __delattr__(self, *args):
      raise AttributeError('%s objects are read-only.' % self.__class__.__name__)

   def __eq__(self, arg):
      return arg == self.name
   
   def __repr__(self):
      return 'Clef("%s")' % self.name

   def __setattr__(self, attribute, value):
      raise AttributeError('%s objects are read-only.' % self.__class__.__name__)

   def __str__(self):
      return self.name

   ## PRIVATE ATTRIBUTES ##

   _clef_name_to_middle_c_position = { 'treble': -6, 'alto': 0,
      'tenor': 2, 'bass':6, }

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\clef "%s"' % self.name

   @property
   def middle_c_position(self):
      return self._clef_name_to_middle_c_position[self.name]
