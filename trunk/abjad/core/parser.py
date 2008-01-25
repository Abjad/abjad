class _Parser(object):

   def formatAttribute(self, attribute):
      result = attribute.replace('_', '-')
      result = "#'%s" % result
      return result

   def formatValue(self, value):
      if value is True:
         return '##t'
      elif value is False:
         return '##f'
      elif self._isConstant(value):
         return '#%s' % value
      elif self._isLilyFunctionName(value):
         return '#%s' % value
      elif isinstance(value, tuple):
         return "#'(%s . %s)" % value
      elif value.__class__.__name__ in ['String', 'Markup']:
         return value
      else:
         return "#'%s" % value
      
   def _isConstant(self, value):
      if isinstance(value, int) or isinstance(value, float) or \
          value in ['up', 'down', 'center', 
         'red', 'blue', 'green', 'black', 'white']:
         return True
      else:
         return False

   def _isLilyFunctionName(self, arg):
      return isinstance(arg, str) and '::' in arg
