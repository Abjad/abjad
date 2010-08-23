from abjad.tools.marktools.Mark import Mark


class TimeSignatureMark(Mark):
   '''.. versionadded:: 1.1.2

   Time signature mark.
   '''

   _format_slot = 'opening'

   def __init__(self, numerator, denominator):
      Mark.__init__(self)
      self.numerator = numerator
      self.denominator = denominator

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\time %s/%s' % (self.numerator, self.denominator)
