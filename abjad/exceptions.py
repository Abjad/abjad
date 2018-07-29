"""
Custom exceptions.
"""

class AssignabilityError(Exception):
    r'''Duration can not be assigned to note, rest or chord.
    '''
    pass


class ExtraSpannerError(Exception):
    r'''More than one spanner found for single-spanner operation.
    '''
    pass


class ImpreciseMetronomeMarkError(Exception):
    r'''MetronomeMark is imprecise.
    '''
    pass


class LilyPondParserError(Exception):
    r'''Can not parse input.
    '''
    pass


class MissingMeasureError(Exception):
    r'''No measure found.
    '''
    pass


class MissingMetronomeMarkError(Exception):
    r'''No metronome mark found.
    '''
    pass


class MissingSpannerError(Exception):
    r'''No spanner found.
    '''
    pass


class OverfullContainerError(Exception):
    r'''Container contents duration is greater than container target duration.
    '''
    pass


class ParentageError(Exception):
    r'''A parentage error.
    '''
    pass


class PersistentIndicatorError(Exception):
    r'''Persistent indicator already attached at same context.
    '''
    pass


class SchemeParserFinishedError(Exception):
    r'''SchemeParser has finished parsing.
    '''
    pass


class UnboundedTimeIntervalError(Exception):
    r'''Time interval has no bounds.
    '''
    pass


class UnderfullContainerError(Exception):
    r'''Container contents duration is less than container target duration.
    '''
    pass


class WellformednessError(Exception):
    r'''Score not well formed.
    '''
    pass
