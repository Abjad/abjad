from abjad.component.slots import _ComponentFormatterSlotsInterface


class _LeafFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
#   ## OLD ##
#
#   @property
#   def slot_1(self):
#      result = [ ]
#      formatter = self.formatter
#      leaf = formatter.leaf
#      result.extend(formatter._grace_body)
#      result.extend(['% ' + x for x in leaf.comments.before])
#      result.extend(leaf.directives.before)
#      result.extend(leaf.interfaces.overrides)
#      result.extend(leaf.spanners.before)
#      result.extend(leaf.interfaces.before)
#      return tuple(result)
#
#   @property
#   def slot_3(self):
#      result = [ ]
#      formatter = self.formatter
#      leaf = formatter.leaf
#      result.extend(['% ' + x for x in leaf.comments.opening])
#      result.extend(leaf.directives.opening)
#      result.extend(leaf.interfaces.opening)
#      result.extend(formatter._agrace_opening)
#      return tuple(result)
#
#   @property
#   def slot_4(self):
#      return tuple(self.formatter._leaf_body)
#
#   @property
#   def slot_5(self):
#      result = [ ]
#      formatter = self.formatter
#      leaf = formatter.leaf
#      result.extend(formatter._agrace_body)
#      result.extend(leaf.directives.closing)
#      result.extend(leaf.interfaces.closing)
#      result.extend(['% ' + x for x in leaf.comments.closing])
#      return tuple(result)
#
#   @property
#   def slot_7(self):
#      result = [ ]
#      formatter = self.formatter
#      leaf = formatter.leaf
#      result.extend(leaf.interfaces.after)
#      result.extend(leaf.spanners.after)
#      result.extend(leaf.directives.after)
#      result.extend(['% ' + x for x in leaf.comments.after])
#      return tuple(result)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_1(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(formatter, '_grace_body'))
      result.append(self.wrap(leaf.comments, 'before'))
      result.append(self.wrap(leaf.directives, 'before'))
      result.append(self.wrap(leaf.interfaces, 'overrides'))
      result.append(self.wrap(leaf.spanners, 'before'))
      result.append(self.wrap(leaf.interfaces, 'before'))
      return tuple(result)

   @property
   def slot_3(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(leaf.comments, 'opening'))
      result.append(self.wrap(leaf.directives, 'opening'))
      result.append(self.wrap(leaf.interfaces, 'opening'))
      result.append(self.wrap(formatter, '_agrace_opening'))
      return tuple(result)

   @property
   def slot_4(self):
      result = [ ]
      result.append(self.wrap(self.formatter, '_leaf_body'))
      return tuple(result)

   @property
   def slot_5(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(formatter, '_agrace_body'))
      result.append(self.wrap(leaf.directives, 'closing'))
      result.append(self.wrap(leaf.interfaces, 'closing'))
      result.append(self.wrap(leaf.comments, 'closing'))
      return tuple(result)

   @property
   def slot_7(self):
      result = [ ]
      formatter = self.formatter
      leaf = formatter.leaf
      result.append(self.wrap(leaf.interfaces, 'after'))
      result.append(self.wrap(leaf.spanners, 'after'))
      result.append(self.wrap(leaf.directives, 'after'))
      result.append(self.wrap(leaf.comments, 'after'))
      return tuple(result)
