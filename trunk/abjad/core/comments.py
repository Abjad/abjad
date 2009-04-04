from abjad.core.abjadcore import _Abjad


class _UserComments(_Abjad):
   
   def __init__(self):
      self._after = [ ]
      self._before = [ ]
      self._right = [ ]

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      return self._after

   @property
   def before(self):
      return self._before

   @property
   def right(self):
      return self._right
