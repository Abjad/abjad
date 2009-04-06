from abjad.component.slots import _ComponentFormatterSlotsInterface


class _ContainerFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)

   ## PRIVATE METHODS ##

#   def _format_contributor_name(self, contributor):
#      '''Formater contributor name.'''
#      result = [ ]
#      for part in contributor:
#         if isinstance(part, str):
#            result.append(part)
#         else:
#            result.append(part.__class__.__name__)
#      result = '.'.join(result)
#      return result
#
#   def _format_slot(self, label, slot, 
#      verbose = False, output = 'screen'):
#      '''Format slot.'''
#      result = label + '\n'
#      for (contributor, contributions) in slot:
#         if contributions or verbose:
#            result += '\t%s\n' % self._format_contributor_name(contributor)
#            for contribution in contributions:
#               result += '\t\t%s\n' % contribution
#      if output == 'screen':
#         print result
#      else:
#         return result

   def _indent_slot_contributions(self, slot):
      for contributor, contributions in slot:
         if contributions:
            for i, contribution in enumerate(contributions):
               contributions[i] = '\t' + contribution
      
#   ## OLD PUBLIC ATTRIBUTES ##
#
#   @property
#   def slot_1(self):
#      result = [ ]
#      container = self.formatter.container
#      result.extend(['% ' + x for x in container.comments.before])
#      result.extend(container.directives.before)
#      return tuple(result)
#
#   @property
#   def slot_2(self):
#      result = [ ]
#      result.append(self.formatter.container.brackets.open)
#      return tuple(result)
#
#   @property
#   def slot_3(self):
#      result = [ ]
#      container = self.formatter.container
#      result.extend(['% ' + x for x in container.comments.opening])
#      result.extend(container.directives.opening)
#      result.extend(container.interfaces.overrides)
#      result.extend(container.interfaces.opening)
#      result = ['\t' + x for x in result]
#      return tuple(result)
#
#   @property
#   def slot_4(self):
#      return tuple(self.formatter._contents)
#
#   @property
#   def slot_5(self):
#      result = [ ]
#      container = self.formatter.container
#      result.extend(container.interfaces.closing)
#      result.extend(container.interfaces.reverts)
#      result.extend(container.directives.closing)
#      result.extend(['% ' + x for x in container.comments.closing])
#      result = ['\t' + x for x in result]
#      return tuple(result)
#
#   @property
#   def slot_6(self):
#      result = [ ]
#      result.append(self.formatter.container.brackets.close)
#      return tuple(result)
#
#   @property
#   def slot_7(self):
#      result = [ ]
#      container = self.formatter.container
#      result.extend(container.directives.after)
#      result.extend(['% ' + x for x in container.comments.after])
#      return tuple(result)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.comments, 'before'))
      result.append(self.wrap(container.directives, 'before'))
      return tuple(result)

   @property
   def slot_2(self):
      result = [ ]
      result.append(self.wrap(self.formatter.container.brackets, 'open'))
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.comments, 'opening'))
      result.append(self.wrap(container.directives, 'opening'))
      result.append(self.wrap(container.interfaces, 'overrides'))
      result.append(self.wrap(container.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_4(self):
      result = [ ]
      result.append(self.wrap(self.formatter, '_contents'))
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.interfaces, 'closing'))
      result.append(self.wrap(container.interfaces, 'reverts'))
      result.append(self.wrap(container.directives, 'closing'))
      result.append(self.wrap(container.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      result = [ ]
      result.append(self.wrap(self.formatter.container.brackets, 'close'))
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      container = self.formatter.container
      result.append(self.wrap(container.directives, 'after'))
      result.append(self.wrap(container.comments, 'after'))
      return tuple(result)

   ## PUBLIC METHODS ##

   def contributions(self, attr):
      result = [ ]
      for contributor, contributions in getattr(self, attr):
         result.extend(contributions)
      return result

   def report(self, verbose = False, output = 'screen'):
      '''Report format contributions.'''
      result = ''
      for i in range(1, 7 + 1):
         label = 'slot_%s' % i
         attr = label
         result += self._format_slot(
            label, getattr(self, attr), verbose, output = 'string')
      if output == 'screen':
         print result
      else:
         return result
