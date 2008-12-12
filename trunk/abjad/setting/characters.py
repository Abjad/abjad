from abjad.core.abjadcore import _Abjad


class _Characters(_Abjad):

   def __init__(self, contents = None):
      self.contents = contents

   def __repr__(self):
      return '"%s"' % self.contents
