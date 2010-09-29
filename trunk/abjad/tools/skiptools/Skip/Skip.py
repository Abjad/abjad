from abjad.components._Leaf import _Leaf


class Skip(_Leaf):
   '''The Abjad model of the LilyPond skip.
   '''

   def __init__(self, *args, **kwargs):
      from abjad.tools.skiptools._initialize_skip import _initialize_skip
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
   def _compact_representation(self):
      return 's%s' % self.duration
  
   @property
   def _body(self):
      '''String representation of body of skip at format-time.
         Return list like all other format-time contributions.'''
      result = [ ]
      result.append('s%s' % self.duration)
      return result
