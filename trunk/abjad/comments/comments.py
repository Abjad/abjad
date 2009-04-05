from abjad.core.abjadcore import _Abjad


class _UserComments(_Abjad):
   
   def __init__(self):
      self._after = [ ]
      self._before = [ ]
      self._closing = [ ]
      self._opening = [ ]
      self._right = [ ]

   ## PUBLIC ATTRIBUTES ##

   @property
   def after(self):
      return self._after

   @property
   def before(self):
      return self._before

   @property
   def closing(self):
      return self._closing

   @property
   def opening(self):
      return self._opening

   @property
   def right(self):
      return self._right
