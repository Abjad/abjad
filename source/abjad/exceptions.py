"""
Exceptions.
"""


class AssignabilityError(Exception):
    """
    Duration can not be assigned to note, rest or chord.
    """

    pass


class ImpreciseMetronomeMarkError(Exception):
    """
    Metronome mark is imprecise.
    """

    pass


class LilyPondParserError(Exception):
    """
    Can not parse input.
    """

    pass


class MissingContextError(Exception):
    """
    No context found.
    """

    pass


class MissingMetronomeMarkError(Exception):
    """
    No metronome mark found.
    """

    pass


class ParentageError(Exception):
    """
    A parentage error.
    """

    pass


class PersistentIndicatorError(Exception):
    """
    Persistent indicator already attached at same context.
    """

    pass


class SchemeParserFinishedError(Exception):
    """
    Scheme parser has finished parsing.
    """

    pass


class UnboundedTimeIntervalError(Exception):
    """
    Time interval has no bounds.
    """

    pass


class WellformednessError(Exception):
    """
    Score not well formed.
    """

    pass
