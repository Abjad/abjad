from abjad.components._Context import _Context


class Staff(_Context):
   '''Abjad model of one staff in score.'''

   def __init__(self, music = None, **kwargs):
      '''Init staff as type of Abjad context.'''
      _Context.__init__(self, music)
      self.context = 'Staff'
      self._initialize_keyword_values(**kwargs)
