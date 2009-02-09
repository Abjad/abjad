class AssignabilityError(Exception):
   pass

class ContiguityError(Exception):
   pass

class ImproperlyFilledMeasureError(Exception):
   pass

class NonbinaryMeterSuppressionError(Exception):
   pass

class OverfullMeasureError(ImproperlyFilledMeasureError):
   pass

class UnderfullMeasureError(ImproperlyFilledMeasureError):
   pass
