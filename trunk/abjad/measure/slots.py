from abjad.container.slots import _ContainerFormatterSlotsInterface


class _MeasureFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      '''Optional class-level start comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered start comments.
         Set client_class.block to 'number' to print numbered start comments.
         Analagous to close brackets for other types of container.'''
      result = [ ]
      formatter = self._client
      measure = formatter._client
      contribution = formatter.number._measure_contribution
      if contribution == 'comment':
         contributor = (formatter.number, '_measure_contribution')
         contributions = ['%% start measure %s' % measure.number]
         result.append([contributor, contributions])
      return tuple(result)

   @property
   def slot_3(self):
      r'''This is the slot where LilyPond grob \override commands live.
      Measure need to override the default container behavior for slot 3
      assembly in order to push barline overrides to slot 5, later in
      the format string. Otherwise, measure contents of slot 3 is just
      like generic container contents of slot 3.
      '''
      result = [ ]
      measure = self.formatter.container
      result.append(self.wrap(measure.comments, 'opening'))
      result.append(self.wrap(measure.directives, 'opening'))
      #result.append(self.wrap(measure.interfaces, 'overrides'))
      result.append(self._wrap_measure_interface_overrides( ))
      result.append(self.wrap(measure.interfaces, 'opening'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      r'''Just like container slot 5. But with any LilyPond BarLine
      \override strings included FIRST THING so as to appear PRIOR TO
      any LilyPond BarLine \revert strings that may appear later.'''
      result = [ ]
      measure = self.formatter.container
      result.append(self._wrap_barline_interface_overrides( ))
      result.append(self.wrap(measure.interfaces, 'closing'))
      #result.append(self.wrap(measure.interfaces, 'reverts'))
      result.append(self._wrap_measure_interface_reverts( ))
      result.append(self.wrap(measure.directives, 'closing'))
      result.append(self.wrap(measure.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      '''Optional class-level stop comments in LilyPond output.
         Let client_class = self._client.__class__.
         Set client_class.block to True to print unnumbered stop comments.
         Set client_class.block to 'number' to print numbered stop comments.
         Analagous to open brackets for other types of container.'''
      result = [ ]
      formatter = self._client
      measure = formatter._client
      contribution = formatter.number._measure_contribution
      if contribution == 'comment':
         contributor = (formatter.number, '_measure_contribution')
         contributions = ['%% stop measure %s' % measure.number]
         result.append([contributor, contributions])
      return tuple(result)

   ## PRIVATE METHODS ##

   def _wrap_barline_interface_overrides(self):
      measure = self.formatter.container
      barline_interface = measure.barline
      return [(barline_interface, 'overrides'), barline_interface.overrides]
      
   def _wrap_measure_interface_overrides(self):
      '''To allow filtering out of BarLine overrides.'''
      result = self.wrap(self.formatter.container.interfaces, 'overrides')
      override_list = result[-1]
      override_list = [x for x in override_list if 'BarLine' not in x]
      result[-1] = override_list
      return result

   def _wrap_measure_interface_reverts(self):
      '''To allow filtering out of BarLine reverts.'''
      result = self.wrap(self.formatter.container.interfaces, 'reverts')
      override_list = result[-1]
      override_list = [x for x in override_list if 'BarLine' not in x]
      result[-1] = override_list
      return result
