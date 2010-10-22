from abjad.components._Context import _Context


class StaffGroup(_Context):

   def __init__(self, music = [ ], **kwargs):
      _Context.__init__(self, music)
      self.is_parallel = True
      self.context = 'StaffGroup'
      self._initialize_keyword_values(**kwargs)
