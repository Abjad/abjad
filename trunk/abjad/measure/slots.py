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
         result.append('%% start measure %s' % measure.numbering.measure)
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
         result.append('%% stop measure %s' % measure.numbering.measure)
      return tuple(result)
