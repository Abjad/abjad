from abjad.core.abjadcore import _Abjad


class _ContextContainmentSignature(_Abjad):

   def __init__(self):
      self.voice = None 
      self.staff = None
      self.score = None
      self.root = None

   ## OVERLOADS ##

   def __eq__(self, arg):
      return isinstance(arg, _ContextContainmentSignature) and \
         self.voice == arg.voice and \
         self.staff == arg.staff and \
         self.score == arg.score and \
         self.root == arg.root
