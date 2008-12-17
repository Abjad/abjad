from abjad.core.parser import _Parser
from abjad.spanner.spanner import _Spanner


class Override(_Spanner):

   def __init__(self, music, *args):
      _Spanner.__init__(self, music)
      if len(args) == 3:
         self._context = None
         self._grob, self._attribute, self._value  = args
      elif len(args) == 4:
         self._context, self._grob, self._attribute, self._value  = args
      else:
         raise ValueError('need 3 or 4 args, not %s.' % len(args))
      self._parser = _Parser( )

   def __repr__(self):
      if self._context:
         return 'Override([%s], %s, %s, %s, %s)' % (self._summary, 
            self._context, self._grob, self._attribute, self._value)
      else:
         return 'Override([%s], %s, %s, %s)' % (self._summary, 
            self._grob, self._attribute, self._value)

   def _prependContext(self, expr):
      if self._context:
         return '%s.%s' % (self._context, expr)
      else:
         return expr

   def _prependCounter(self, expr):
      if len(self) == 1:
         return r'\once ' + expr
      else:
         return expr

   def _before(self, leaf):
      if self._isMyFirstLeaf(leaf) and self._attribute and self._value:
         grob = self._prependContext(self._grob)
         attribute = self._parser.formatAttribute(self._attribute)
         value = self._parser.formatValue(self._value)
         result = r'\override %s %s = %s' % (grob, attribute, value)
         result = self._prependCounter(result)
         return [result]
      else:
         return [ ]

   def _after(self, leaf):
      if self._isMyLastLeaf(leaf) and \
         not self._isMyOnlyLeaf(leaf) and self._attribute:
         grob = self._prependContext(self._grob)
         attribute = self._parser.formatAttribute(self._attribute)
         result = r'\revert %s %s' % (grob, attribute)
         return [result]
      else:
         return [ ]
