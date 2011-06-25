from abjad.tools import durtools


def is_meter_token(expr):
   '''True when `expr` has the form of an Abjad meter token::

      abjad> from abjad.tools import metertools

   ::
   
      abjad> metertools.is_meter_token(contexttools.TimeSignatureMark(3, 8))
      True

   ::

      abjad> metertools.is_meter_token(Duration(3, 8))
      True

   ::

      abjad> metertools.is_meter_token((3, 8))        
      True

   Otherwise false::

      abjad> metertools.is_meter_token('text')
      False

   Return boolean.
   '''
   from abjad.tools import contexttools

   if isinstance(expr, contexttools.TimeSignatureMark):
      return True
   elif isinstance(expr, durtools.Duration):
      return True
   elif durtools.is_duration_pair(expr):
      return True
   else:
      return False
