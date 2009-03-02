class AssignabilityError(Exception):
   '''Fraction like 5/16 or 9/16 can not be assigned
      to a single, untied note, rest or chord.'''
   pass

class ContiguityError(Exception):
   '''Input is not contiguous.'''
   pass

class ExtraSpannerError(Exception):
   '''Operation assumes presence of a single spanner,
      but more than one spanner is present.'''
   pass

class ImproperlyFilledMeasureError(Exception):
   '''Measure contents duration does not equal measure meter duration.'''
   pass

class MissingSpannerError(Exception):
   '''Operation assumes presence of spanner,
       but spanner is missing.'''
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

class UnderfullMeasureError(ImproperlyFilledMeasureError):
   '''Measure contents duration is less than measure meter duration.'''
   pass
