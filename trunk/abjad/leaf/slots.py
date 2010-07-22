from abjad.component.slots import _ComponentFormatterSlotsInterface


class _LeafFormatterSlotsInterface(_ComponentFormatterSlotsInterface):

   def __init__(self, client):
      _ComponentFormatterSlotsInterface.__init__(self, client)
      
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
      result.append(self.wrap(leaf.interfaces, 'settings'))
      result.append(self.wrap(leaf.spanners, '_before'))
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
      result.append(self._wrap_preceding_measure_bar_line_reverts( ))
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
      result.append(self.wrap(leaf.spanners, '_after'))
      result.append(self.wrap(leaf.directives, 'after'))
      result.append(self.wrap(leaf.comments, 'after'))
      return tuple(result)

   ## PRIVATE METHODS ##

   def _wrap_preceding_measure_bar_line_reverts(self):
      from abjad.measure import _Measure
      from abjad.tools import iterate
      from abjad.tools import parenttools
      leaf = self.formatter._client
      #containing_measure = leaf.parentage.first(_Measure)
      containing_measure = parenttools.get_first(leaf, _Measure)
      if containing_measure is None:
         return [('Special', 'reverts'), [ ]]
      if leaf is not containing_measure.leaves[0]:
         return [('Special', 'reverts'), [ ]]
      prev_measure = iterate.get_prev_measure_from_component(containing_measure)
      if prev_measure is None:
         return [('Special', 'reverts'), [ ]]
      bar_line_reverts = [ ]
      bar_line_reverts.extend(prev_measure.bar_line._reverts)
      bar_line_reverts.extend(prev_measure.span_bar._reverts)
      return [('Special', 'reverts'), bar_line_reverts]
