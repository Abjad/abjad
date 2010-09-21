from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface


class _MeasureFormatterSlotsInterface(_ContainerFormatterSlotsInterface):

   def __init__(self, client):
      _ContainerFormatterSlotsInterface.__init__(self, client)

   ## PUBLIC ATTRIBUTES ##

   @property
   def slot_2(self):
      '''Optional class-level start comments in LilyPond output.

      .. versionchanged:: 1.1.1
         Measures now format { } and << >> like other containers.
      '''
      result = [ ]
      formatter = self._client
      measure = formatter._client
## FIXME ##
#      contribution = formatter.number._measure_contribution
#      if contribution == 'comment':
#         contributor = (formatter.number, '_measure_contribution')
#         contributions = ['%% start measure %s' % measure.number]
#         result.append([contributor, contributions])
      brackets = _ContainerFormatterSlotsInterface.slot_2.fget(self) 
      result.extend(brackets)
      return tuple(result)

   @property
   def slot_3(self):
      r'''This is the slot where LilyPond grob \override commands live.
      Measure need to override the default container behavior for slot 3
      assembly in order to push bar_line overrides to slot 5, later in
      the format string. Otherwise, measure contents of slot 3 is just
      like generic container contents of slot 3.
      '''
      from abjad.tools.formattools._get_opening_slot_format_contributions import \
         _get_opening_slot_format_contributions
      from abjad.tools.formattools._get_context_setting_format_contributions import \
         _get_context_setting_format_contributions
      result = [ ]
      measure = self.formatter.container
      result.append(self.wrap(measure.comments, 'opening'))
      result.append(self.wrap(measure.directives, 'opening'))
      #result.append(self.wrap(measure.interfaces, 'overrides'))
      result.append(self._wrap_measure_interface_overrides( ))

      #result.append(self.wrap(measure.interfaces, 'opening'))
      #result.append(self.wrap(measure.interfaces, 'settings'))
      result.append([('opening', 'opening'),
         _get_opening_slot_format_contributions(self._client._client)])
      result.append([('settings', 'settings'),
         _get_context_setting_format_contributions(self._client._client)])

      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_5(self):
      r'''Just like container slot 5. But with any LilyPond BarLine
      \override strings included FIRST THING so as to appear PRIOR TO
      any LilyPond BarLine \revert strings that may appear later.
      '''
      from abjad.tools.formattools._get_closing_slot_format_contributions import \
         _get_closing_slot_format_contributions
      result = [ ]
      measure = self.formatter.container
      result.append(self._wrap_bar_line_interface_overrides( ))

      #result.append(self.wrap(measure.interfaces, 'closing'))
      result.append([('closing', 'closing'),
         _get_closing_slot_format_contributions(self._client._client)])

      #result.append(self.wrap(measure.interfaces, 'reverts'))
      result.append(self._wrap_measure_interface_reverts( ))
      result.append(self.wrap(measure.directives, 'closing'))
      result.append(self.wrap(measure.comments, 'closing'))
      self._indent_slot_contributions(result)
      return tuple(result)

   @property
   def slot_6(self):
      '''Sequential or parallel close brackets.
      Also Optional class-level stop comments in LilyPond output.

      .. versionchanged:: 1.1.1
         Measures now format { } and << >> like other containers.
      '''
      result = [ ]
      formatter = self._client
      measure = formatter._client
      brackets = _ContainerFormatterSlotsInterface.slot_6.fget(self)
      result.extend(brackets)
## FIXME ##
#      contribution = formatter.number._measure_contribution
#      if contribution == 'comment':
#         contributor = (formatter.number, '_measure_contribution')
#         contributions = ['%% stop measure %s' % measure.number]
#         result.append([contributor, contributions])
      return tuple(result)

   ## PRIVATE METHODS ##

   ## FIXME: make work with new grob override pattern ##
   def _wrap_bar_line_interface_overrides(self):
      measure = self.formatter.container
      bar_line_overrides = [ ]
      #bar_line_overrides.extend(measure.bar_line._overrides)
      #bar_line_overrides.extend(measure.span_bar._overrides)
      ## FIXME ##
      #bar_line_overrides.extend(measure.override.bar_line._overrides)
      #bar_line_overrides.extend(measure.override.span_bar._overrides)
      return [('BarLine / SpanBar', 'overrides'), bar_line_overrides]
      
   def _wrap_measure_interface_overrides(self):
      '''To allow filtering out of BarLine overrides.'''
      from abjad.tools.formattools._get_grob_override_format_contributions import \
         _get_grob_override_format_contributions

      #result = self.wrap(self.formatter.container.interfaces, 'overrides')
      result = [('overrides', 'overrides'),
         _get_grob_override_format_contributions(self._client._client)]

      override_list = result[-1]
      override_list = [x for x in override_list 
         if 'BarLine' not in x and 'SpanBar' not in x]
      result[-1] = override_list
      return result

   def _wrap_measure_interface_reverts(self):
      '''To allow filtering out of BarLine reverts.
      '''
      from abjad.tools.formattools._get_grob_revert_format_contributions import \
         _get_grob_revert_format_contributions

      #result = self.wrap(self.formatter.container.interfaces, 'reverts')
      result = [('reverts', 'reverts'),
         _get_grob_revert_format_contributions(self._client._client)]

      override_list = result[-1]
      override_list = [x for x in override_list 
         if 'BarLine' not in x and 'SpanBar' not in x]
      result[-1] = override_list
      return result
