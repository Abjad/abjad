from abjad.components._Context import _Context


class Score(_Context):
   '''Abjad model of the musical score.
   '''

   def __init__(self, music = None, **kwargs):
      _Context.__init__(self, music)
      self.context = 'Score'
      self.parallel = True
      self.scorewide_spacing = None
      self._initialize_keyword_values(**kwargs)
