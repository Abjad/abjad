class DurationError(Exception):
   '''Any type of duration error.'''
   pass

class ImproperlyFilledMeasureError(Exception):
   '''Measure contents duration does not equal measure meter duration.'''
   pass

class AssignabilityError(DurationError):
   '''Fraction like 5/16 or 9/16 can not be assigned
      to a single, untied note, rest or chord.'''
   pass

class ContextContainmentError(Exception):
   '''Only certain types of context should contain
      other types of context.'''
   pass

class ContiguityError(Exception):
   '''Input is not contiguous.'''
   pass

class ExtraSpannerError(Exception):
   '''Operation assumes presence of a single spanner,
      but more than one spanner is present.'''
   pass

class MissingSpannerError(Exception):
   '''Operation assumes presence of spanner,
       but spanner is missing.'''
   pass

class NegativeDurationError(DurationError):
   '''Component durations must be positive.'''
   pass

class NonbinaryMeterConversionError(Exception):
   '''Nonbinary meter has no binary equivalent.'''
   pass

class NonbinaryMeterSuppressionError(Exception):
   '''Trying to suppress nonbinary meter;
      this will cause prolated duration of measure contents
      to calculate incorrectly.'''
   pass

class OverfullMeasureError(ImproperlyFilledMeasureError):
   '''Measure contents duration is greater than measure meter duration.'''
   pass

class SpannerError(Exception):
   '''General spanner error.'''
   pass

class StaffContainmentError(ContextContainmentError):
   '''Staves must contain only voices and lower-level components.
      Staves must not contain staff groups, scores or other staves.'''
   pass

class TieChainError(Exception):
   '''General tie chain error.'''
   pass

class UnderfullMeasureError(ImproperlyFilledMeasureError):
   '''Measure contents duration is less than measure meter duration.'''
   pass

class VoiceContainmentError(ContextContainmentError):
   '''Voice must contain only lower-level components.
      Lower-level components include leaves, tuplets, measures, etc.
      Voice must not contain higher-level components.
      Higher-level components import stave, staff groups, scores, etc.'''
   pass
