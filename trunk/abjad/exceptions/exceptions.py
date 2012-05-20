class AssignabilityError(Exception):
    '''Duration can not be assigned to note, rest or chord.
    '''
    pass

class ClefError(Exception):
    '''General clef error.
    '''
    pass

class ContainmentError(Exception):
    '''General containment error.
    '''
    pass

class ContextContainmentError(Exception):
    '''Context can not contain other context.
    '''
    pass

class ContiguityError(Exception):
    '''Input is not contiguous.
    '''
    pass

class CyclicNodeError(Exception):
    '''Node is in cyclic relationship.
    '''
    pass

class DurationError(Exception):
    '''General duration error.
    '''
    pass

class ExtraMarkError(Exception):
    '''More than one mark is found for single-mark operation.
    '''
    pass

class ExtraNoteHeadError(Exception):
    '''More than one note head found for single-note head operation.
    '''
    pass

class ExtraPitchError(Exception):
    '''More than one pitch found for single-pitch operation.
    '''
    pass

class ExtraSpannerError(Exception):
    '''More than one spanner found for single-spanner operation.
    '''
    pass

class ImpreciseTempoError(Exception):
    '''TempoMark is imprecise.
    '''
    pass

class InputSpecificationError(Exception):
    '''Input is badly formed.
    '''
    pass

class InstrumentError(Exception):
    '''General instrument error.
    '''
    pass

class IntervalError(Exception):
    '''General pitch interval error.
    '''
    pass

class LilyPondParserError(Exception):
    '''Can not parse input.
    '''
    pass

class LineBreakError(Exception):
    '''General link break error.
    '''
    pass

class MarkError(Exception):
    '''General mark error.
    '''
    pass

class MeasureContiguityError(Exception):
    '''Measures must be contiguous.
    '''
    pass

class MeasureError(Exception):
    '''General measure error.
    '''
    pass

class MissingComponentError(Exception):
    '''No component found.
    '''
    pass

class MissingInstrumentError(Exception):
    '''No instrument found.
    '''
    pass

class MissingMarkError(Exception):
    '''No mark found.
    '''
    pass

class MissingMeasureError(Exception):
    '''No measure found.
    '''
    pass

class MissingNoteHeadError(Exception):
    '''No note head found.
    '''
    pass

class MissingPitchError(Exception):
    '''No pitch found.
    '''
    pass

class MissingSpannerError(Exception):
    '''No spanner found.
    '''
    pass

class MissingTempoError(Exception):
    '''No tempo found.
    '''
    pass

class MusicContentsError(Exception):
    '''General container contents error.
    '''
    pass

class NegativeDurationError(Exception):
    '''Component duration must be positive.
    '''
    pass

class NonbinaryTimeSignatureConversionError(Exception):
    '''Nonbinary time signature has no binary equivalent.
    '''
    pass

class NonbinaryTimeSignatureSuppressionError(Exception):
    '''Suppressing nonbinary time signature will miscalculate duration of measure contents.
    '''
    pass

class NoteHeadError(Exception):
    '''General note head error.
    '''
    pass

class OverfullContainerError(Exception):
    '''Container contents duration is greater than container target duration.
    '''
    pass

class ParallelError(Exception):
    '''Parallel containers must contain contexts only.
    '''
    pass

class PartitionError(Exception):
    '''General partition error.
    '''
    pass

class PitchError(Exception):
    '''General pitch error.
    '''
    pass

class SpacingError(Exception):
    '''General spacing error.
    '''
    pass

class SpannerError(Exception):
    '''General spanner error.
    '''
    pass

class SpannerPopulationError(Exception):
    '''Spanner contents incorrect.

    Spanner may be missing component it is assumed to have.

    Spanner may have a component it is assumed not to have.
    '''
    pass

class StaffContainmentError(Exception):
    '''Staves must not contain staff groups, scores or other staves.
    '''
    pass

class TempoError(Exception):
    '''General tempo error.
    '''
    pass

class TieChainError(Exception):
    '''General tie chain error.
    '''
    pass

class TonalHarmonyError(Exception):
    '''General tonal harmony error.
    '''
    pass

class TupletError(Exception):
    '''Geneal tuplet error.
    '''
    pass

class TupletFuseError(Exception):
    '''Tuplets must carry same multiplier and be same type in order to fuse correctly.
    '''
    pass

class TimeSignatureAssignmentError(Exception):
    '''Can not assign time signature to dynamic measure.
    '''
    pass

class TimeSignatureError(Exception):
    '''General time signature error.
    '''
    pass

class TypographicWhitespaceError(Exception):
    '''Whitespace after leaf confuses LilyPond timekeeping.
    '''
    pass

class UnboundedTimeIntervalError(Exception):
    '''Time interval has no bounds.
    '''
    pass

class UnderfullContainerError(Exception):
    '''Container contents duration is less than container target duration.
    '''
    pass

class UndefinedSpacingError(Exception):
    '''No spacing value found.
    '''
    pass

class VoiceContainmentError(Exception):
    '''Voice must not contain staves, staff groups or scores.
    '''
    pass

class WellFormednessError(Exception):
    '''Score not well formed.
    '''
    pass
