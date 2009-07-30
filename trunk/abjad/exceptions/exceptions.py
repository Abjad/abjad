class DurationError(Exception):
   '''Any type of duration error.'''
   pass

class MeasureError(Exception):
   '''General measure error.'''
   pass

class MissingMeasureError(MeasureError):
   '''Operation assumes presence of measure when no measure found.'''
   pass

class ImproperlyFilledMeasureError(MeasureError):
   '''Measure contents duration does not equal measure meter duration.'''
   pass

class AssignabilityError(DurationError):
   '''Fraction like 5/16 or 9/16 can not be assigned
      to a single, untied note, rest or chord.'''
   pass

class ContainmentError(Exception):
   '''General containment error.'''
   pass

class ContextContainmentError(ContainmentError):
   '''Only certain types of context should contain
      other types of context.'''
   pass

class ContiguityError(Exception):
   '''Input is not contiguous.'''
   pass

class MeasureContiguityError(ContiguityError):
   '''Measures must be back to back.
      Should not separated by intervening, noncontained leaves.'''
   pass

class ExtraSpannerError(Exception):
   '''Operation assumes presence of a single spanner,
      but more than one spanner is present.'''
   pass

class InputSpecificationError(Exception):
   '''Malformed specification token passed as input.'''
   pass

class LineBreakError(Exception):
   '''Operation requires line break but none is present.
   Or operation requires no line break but one is present.'''
   pass

class MeterError(Exception):
   '''Any meter error.'''
   pass

class MeterAssignmentError(MeterError):
   '''Can not assign meter to DynamicMeasure.'''
   pass

class MissingSpannerError(Exception):
   '''Operation assumes presence of spanner,
       but spanner is missing.'''
   pass

class MusicContentsError(Exception):
   '''Operation assumes presence of music content when none is there.
      Or operation assumes absences of music content when some is there.'''
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

class NoteHeadError(Exception):
   '''General notehead error.'''
   pass

class ExtraNoteHeadError(Exception):
   '''Operation expects exactly one notehead of a certain type.
   But there is instead more than one notehead of that type.'''
   pass

class MissingNoteHeadError(Exception):
   '''Operation expects exactly one notehead of a certain type.
   But there is no notehead of that type.'''
   pass

class OverfullMeasureError(ImproperlyFilledMeasureError):
   '''Measure contents duration is greater than measure meter duration.'''
   pass

class ParallelError(ContainmentError):
   '''Parallel containers must contain Contexts only. 
   Leaves and other non-Context containers can not be contained directly
   inside a parallel container.'''
   pass

class PartitionError(Exception):
   '''General partition error.'''
   pass

class PitchError(Exception):
   '''General pitch error.'''
   pass

class MissingPitchError(PitchError):
   '''Operation requests pitch of object without pitch.'''
   pass

class ExtraPitchError(PitchError):
   '''Operation assumes presence of a single pitch,
      but more than one pitch is present.'''
   pass

class SpacingError(Exception):
   '''General spacing error.'''
   pass

class UndefinedSpacingError(SpacingError):
   '''Spacing value needed for calculation but unavailable.'''
   pass

class SpannerError(Exception):
   '''General spanner error.'''
   pass

class SpannerPopulationError(SpannerError):
   '''Assumption about contents of spanner is incorrect.
      Spanner may be missing component it is assumed to have.
      Spanner may have a component it is assumed not to have.'''
   pass

class StaffContainmentError(ContextContainmentError):
   '''Staves must contain only voices and lower-level components.
      Staves must not contain staff groups, scores or other staves.'''
   pass

class TieChainError(Exception):
   '''General tie chain error.'''
   pass

class TempoError(Exception):
   '''General tempo error.'''
   pass

class TupletError(Exception):
   '''Geneal tuplet error.'''
   pass

class TupletFuseError(Exception):
   '''Error trying to fuse two tuplets.
      Tuplets must carry same multiplier and be same type.'''
   pass

class TypographicWhitespaceError(Exception):
   '''Whitespace after leaf confuses LilyPond timekeeping.
      Insert whitespace after measure instead.'''
   pass

class UndefinedTempoError(TempoError):
   '''Tempo required for calculation but not yet defined.'''
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

class WellFormednessError(Exception):
   '''Score not well formed.'''
   pass
