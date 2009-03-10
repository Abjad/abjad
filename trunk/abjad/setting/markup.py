from abjad.core.abjadcore import _Abjad


class Markup(_Abjad):

   def __init__(self, contents):
      self.contents = contents

   ## OVERLOADS ##

   def __repr__(self):
      return 'Markup(%s)' % self.contents

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\markup{%s}' % self.contents
