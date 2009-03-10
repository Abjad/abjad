from abjad.core.parser import _Parser
from abjad.spanner.spanner import Spanner


## TODO - revive this Setting class;
##        make conform to new pattern;
##        copy liberraly from Override.

class _Setting(Spanner):

   def __init__(self, attribute, value, context = None):
      self.attribute = attribute
      self.value = value
      self.context = context
      self.parser = _Parser( )
      Spanner.__init__(self)

   def prependContext(self, expr):
      if self.context:
         return '%s.%s' % (self.context, expr)
      else:
         return expr

   @property
   def before(self):
      attribute = self.prependContext(self.attribute)
      value = self.parser.formatValue(self.value)
      result = '\set %s = %s' % (attribute, value)
      return result
      
   @property
   def after(self):
      attribute = self.prependContext(self.attribute)
      result = '\unset %s' % attribute
      return result
