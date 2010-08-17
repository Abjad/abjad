from abjad.components._Leaf import _Leaf
#from abjad.components.Skip._SkipInitializer import _SkipInitializer


class Skip(_Leaf):

   def __init__(self, *args, **kwargs):
      from abjad.tools.skiptools._initialize_skip import _initialize_skip
      #self._initializer = _SkipInitializer(self, _Leaf, *args)
      _initialize_skip(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)
      
   ## OVERLOADS ##

   def __len__(self):
      return 0

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.duration)

   def __str__(self):
      return 's%s' % self.duration

   ## PUBLIC ATTRIBUTES ##
  
   @property
   def _body(self):
      '''String representation of body of skip at format-time.
         Return list like all other format-time contributions.'''
      result = [ ]
      result.append('s%s' % self.duration)
      return result

   @property
   def pairs(self):
      return ( )

   @property
   def pitches(self):
      return ( )
