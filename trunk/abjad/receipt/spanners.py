from abjad.core.abjadcore import _Abjad


class SpannersReceipt(_Abjad):
   '''Class to encapsulate pairs describing the spanners
      that used to attach to an Abjad component.'''

   def __init__(self):
      self._pairs = set([ ])
