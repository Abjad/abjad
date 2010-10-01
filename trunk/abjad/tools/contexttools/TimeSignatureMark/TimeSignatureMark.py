from abjad.tools import durtools
from abjad.tools import mathtools
from abjad.tools.contexttools.Mark import Mark
from fractions import Fraction


class TimeSignatureMark(Mark):
   '''.. versionadded:: 1.1.2

   The Abjad model of a time signature.
   '''

   _format_slot = 'opening'

   #__slots__ = ('_denominator', '_duration', '_format', '_format_slot', '_multiplier',
   #   '_is_nonbinary', '_numerator', '_partial', )

   def __init__(self, *args, **kwargs):
      from abjad.components import Staff
      target_context = kwargs.get('target_context', None)
      Mark.__init__(self, target_context = target_context)
      if self.target_context is None:
         self._target_context = Staff
      ## initialize numerator and denominator from *args
      if len(args) == 1 and isinstance(args[0], type(self)):
         meter = args[0]
         numerator, denominator = meter.numerator, meter.denominator
      elif len(args) == 1 and isinstance(args[0], Fraction):
         numerator, denominator = args[0].numerator, args[0].denominator
      elif len(args) == 1 and isinstance(args[0], tuple):
         numerator, denominator = args[0][0], args[0][1]
      elif len(args) == 2 and all([isinstance(x, int) for x in args]):
         numerator, denominator = args[0], args[1]
      else:
         raise TypeError('invalid %s meter initialization.' % str(args))
      #object.__setattr__(self, '_numerator', numerator)
      #object.__setattr__(self, '_denominator', denominator)
      self._numerator = numerator
      self._denominator = denominator

      ## initialize partial from **kwargs
      partial = kwargs.get('partial', None)
      if not isinstance(partial, (type(None), Fraction)):
         raise TypeError
      #object.__setattr__(self, '_partial', partial)
      self._partial = partial
      if partial is not None:
         self._partial_repr_string = ', partial = %s' % repr(self._partial)
      else:
         self._partial_repr_string = ''

      ## initialize suppress from kwargs
      suppress = kwargs.get('suppress', None)
      if not isinstance(suppress, (bool, type(None))):
         raise TypeError
      self.suppress = suppress

      ## initialize derived attributes
      #object.__setattr__(self, '_duration', Fraction(numerator, denominator))
      #object.__setattr__(self, '_format', r'\time %s/%s' % (numerator, denominator))
      _multiplier = durtools.positive_integer_to_implied_prolation_multipler(self.denominator)
      #object.__setattr__(self, '_multiplier', _multiplier)
      #object.__setattr__(self, '_is_nonbinary', not mathtools.is_power_of_two(self.denominator))
      self._duration = Fraction(numerator, denominator)
      self._format = r'\time %s/%s' % (numerator, denominator)
      self._multiplier = _multiplier
      self._is_nonbinary = not mathtools.is_power_of_two(self.denominator)

      self._contents_repr_string = '%s/%s' % (self.numerator, self.denominator)

   ## OVERLOADS ##

   def __call__(self, *args):
      from abjad.components.Measure import Measure
      Mark.__call__(self, *args)
      if isinstance(self._start_component, Measure):
         if self._start_component._explicit_meter is not None:
            self._start_component._explicit_meter.detach_mark( )
         self._start_component._explicit_meter = self
      return self

   def __copy__(self, *args):
      return type(self)(self.numerator, self.denominator, 
         partial = self.partial, target_context = self.target_context)

   ## TODO: can this be removed bc defined on Mark superclass?
   __deepcopy__ = __copy__

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         return self.numerator == arg.numerator and self.denominator == arg.denominator
      elif isinstance(arg, tuple):
         return self.numerator == arg[0] and self.denominator == arg[1]
      else:
         return False

   def __ge__(self, arg):
      if isinstance(arg, type(self)):
         return self.duration >= arg.duration
      else:
         raise TypeError
   
   def __gt__(self, arg):
      if isinstance(arg, type(self)):
         return self.duration > arg.duration
      else:
         raise TypeError
   
   def __le__(self, arg):
      if isinstance(arg, type(self)):
         return self.duration <= arg.duration
      else:
         raise TypeError
   
   def __lt__(self, arg):
      if isinstance(arg, type(self)):
         return self.duration < arg.duration
      else:
         raise TypeError
   
   def __ne__(self, arg):
      return not self == arg

   def __nonzero__(self):
      return True
   
   def __repr__(self):
      return '%s(%s, %s%s)%s' % (self.__class__.__name__, self.numerator, 
         self.denominator, self._partial_repr_string, self._attachment_repr_string)

   def __str__(self):
      return '%s/%s' % (self.numerator, self.denominator)

   ## PUBLIC ATTRIBUTES ##

   @property
   def denominator(self):
      '''Integer denominator of meter.'''
      return self._denominator

   @property
   def duration(self):
      '''Fraction duration of meter.'''
      return self._duration

   @property
   def format(self):
      '''LilyPond input format of meter.'''
      if self.suppress:
         return [ ]
      elif self.partial is None:
         return self._format
      else:
         result = [ ]
         result.append(self._format)
         duration_string = durtools.assignable_rational_to_lilypond_duration_string(self.partial)
         partial_directive = r'\partial %s' % duration_string
         result.append(partial_directive)
         return result

   @property
   def multiplier(self):
      '''Fraction prolation multiplier of meter.'''
      return self._multiplier

   @property
   def numerator(self):
      '''Integer numerator of meter.'''
      return self._numerator

   @property
   def is_nonbinary(self):
      '''Boolean indicator of nonbinary meter.'''
      return self._is_nonbinary

   @property
   def partial(self):
      '''Fraction partial-measure pickup prior to meter.'''
      return self._partial
