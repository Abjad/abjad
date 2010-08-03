from abjad.context import _Context


class Staff(_Context):
   '''*Abjad* model of one staff in score.'''

   def __init__(self, music = None):
      '''Init staff as type of *Abjad* context.'''
      _Context.__init__(self, music)
      self.context = 'Staff'
