from abjad.container.slots import _ContainerFormatterSlotsInterface


class _ContextFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)
      
   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      result = [ ]
      formatter = self.formatter
      context = formatter.context
      brackets_open = context.brackets.open
      overrides = context.interfaces.overrides
      if overrides:
         result.append(formatter.INVOCATION + ' \with {')
         result.extend(['\t' + x for x in overrides])
         result.append('} %s' % brackets_open)
      else:
         result.append(formatter.INVOCATION + ' %s' % brackets_open)
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      context = self.formatter.context
      result.extend(['% ' + x for x in context.comments.opening])
      result.extend(context.directives.opening)
      result.extend(context.interfaces.opening)
      result = ['\t' + x for x in result]
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      context = self.formatter.context
      result.extend(context.interfaces.closing)
      result.extend(context.directives.closing)
      result.extend(['% ' + x for x in context.comments.closing])
      result = ['\t' + x for x in result]
      return tuple(result)
