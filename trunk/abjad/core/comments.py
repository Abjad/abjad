from abjad.core.abjadcore import _Abjad


class _Comments(_Abjad):
   
   def __init__(self):
      self.before = [ ]
      self.after = [ ]
      self.right = [ ]

   ## PRIVATE ATTRIBUTES ##

   @property
   def _after(self):
      result = [ ]
      result.extend(['% ' + x for x in self.after])
      return result

   @property
   def _before(self):
      result = [ ]
      result.extend(['% ' + x for x in self.before])
      return result

   @property
   def _right(self):
      result = [ ]
      result.extend(['% ' + x for x in self.right])
      return result
