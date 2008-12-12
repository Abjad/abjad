from abjad.core.abjadcore import _Abjad


class _Comments(list, _Abjad):
   
   def __init__(self):
      self.before = [ ]
      self.after = [ ]
      self.right = [ ]

   @property
   def _before(self):
      result = [ ]
      result.extend(['% ' + x for x in self.before])
      result.extend(['% ' + x for x in self])
      return result

   @property
   def _after(self):
      result = [ ]
      result.extend(['% ' + x for x in self.after])
      return result

   @property
   def _right(self):
      result = [ ]
      result.extend(['% ' + x for x in self.right])
      return result
