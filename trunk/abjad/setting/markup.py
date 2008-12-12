from abjad.core.abjadcore import _Abjad


class _Markup(_Abjad):

   def __init__(self, contents):
      self.contents = contents

   def __repr__(self):
      return self.contents
