from abjad.core.abjadcore import _Abjad


class _ContainmentSignature(_Abjad):

   def __init__(self):
      self._root = None
      self._root_str = ''
      self._self = None
      self._score = None
      self._staff = None
      self._voice = None 

   ## OVERLOADS ##

   def __eq__(self, arg):
      return isinstance(arg, _ContainmentSignature) and \
         self._voice == arg._voice and \
         self._staff == arg._staff and \
         self._score == arg._score and \
         self._root == arg._root

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      str = self.__str__( )
      return '<' + ' * '.join(str.split('\n')) + ' >'

   def __str__(self):
      result = [ ]
      result.append(' root: %s (%s)' % (self._root_str, self._root))
      if self._score is not None:
         result.append('score: %s' % self._score)
      else:
         result.append('score: ')
      if self._staff is not None:
         result.append('staff: %s' % self._staff)
      else:
         result.append('staff: ')
      if self._voice is not None:
         result.append('voice: %s' % self._voice)
      else:
         result.append('voice: ')
      result.append(' self: %s' % self._self)
      return '\n'.join(result)
