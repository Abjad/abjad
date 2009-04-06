from abjad.core.parser import _Parser
from abjad.override.format import _OverrideSpannerFormatInterface
from abjad.spanner.spanner import Spanner


class Override(Spanner):

   def __init__(self, music, *args):
      Spanner.__init__(self, music)
      if len(args) == 3:
         self._context = None
         self._grob, self._attribute, self._value  = args
      elif len(args) == 4:
         self._context, self._grob, self._attribute, self._value  = args
      else:
         raise ValueError('need 3 or 4 args, not %s.' % len(args))
      self._format = _OverrideSpannerFormatInterface(self)
      self._parser = _Parser( )

   ## OVERLOADS ##

   def __repr__(self):
      if self._context:
         return 'Override([%s], %s, %s, %s, %s)' % (self._summary, 
            self._context, self._grob, self._attribute, self._value)
      else:
         return 'Override([%s], %s, %s, %s)' % (self._summary, 
            self._grob, self._attribute, self._value)

   ## PRIVATE METHODS ##

   def _prependContext(self, expr):
      if self._context:
         return '%s.%s' % (self._context, expr)
      else:
         return expr

   def _prependCounter(self, expr):
      if len(self.leaves) == 1:
         return r'\once ' + expr
      else:
         return expr
