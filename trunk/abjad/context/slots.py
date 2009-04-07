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
         contributions = [formatter._invocation + r' \with {']
         result.append([(context.brackets, 'open'), contributions])
         contributions = ['\t' + x for x in overrides]
         result.append([(context.interfaces, 'overrides'), contributions])
         contributions = ['} %s' % context.brackets.open[0]]
         result.append([(context.brackets, 'open'), contributions])
      else:
         contributions = [formatter._invocation + 
            ' %s' % context.brackets.open[0]]
         result.append([(context.brackets, 'open'), contributions])
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      context = self.formatter.context
      result.append(self.wrap(context.comments, 'opening'))
      result.append(self.wrap(context.directives, 'opening'))
      result.append(self.wrap(context.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      context = self.formatter.context
      result.append(self.wrap(context.interfaces, 'closing'))
      result.append(self.wrap(context.directives, 'closing'))
      result.append(self.wrap(context.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)
