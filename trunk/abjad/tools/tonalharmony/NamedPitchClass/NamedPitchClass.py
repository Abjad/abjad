from abjad.pitch import Pitch


class NamedPitchClass(object):
   '''.. versionadded:: 1.1.2

   Named pitch-class ranging over c, cqs, cs, ..., bf, bqf, b. 
   '''

   def __init__(self, name):
      if not self._is_acceptable_name(name):
         raise ValueError('unknown pitch-class name %s' % name)
      self._name = name

   ## OVERLOADS ##

   def __eq__(self, arg):
      if isinstance(arg, NamedPitchClass):
         return self.name == arg.name
      return False

   def __hash__(self):
      return hash(repr(self))

   def __ne__(self, arg):
      return not self == arg
   
   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self.name)

   def __str__(self):
      return '%s' % self.name

   ## PRIVATE METHODS ##

   def _is_acceptable_name(self, name):
      return name in (
         'c', 'cf', 'cs', 'cqf', 'cqs', 'ctqf', 'ctqs', 'cff', 'css',
         'd', 'df', 'ds', 'dqf', 'dqs', 'dtqf', 'dtqs', 'dff', 'dss',
         'e', 'ef', 'es', 'eqf', 'eqs', 'etqf', 'etqs', 'eff', 'ess',
         'f', 'ff', 'fs', 'fqf', 'fqs', 'ftqf', 'ftqs', 'fff', 'fss',
         'g', 'gf', 'gs', 'gqf', 'gqs', 'gtqf', 'gtqs', 'gff', 'gss',
         'a', 'af', 'as', 'aqf', 'aqs', 'atqf', 'atqs', 'aff', 'ass',
         'b', 'bf', 'bs', 'bqf', 'bqs', 'btqf', 'btqs', 'bff', 'bss')

   ## PUBLIC ATTRIBUTES ##

   @property
   def name(self):
      '''Read-only name of pitch-class.'''
      return self._name

   @property
   def pitch_class(self):
      '''Read-only numeric pitch-class.'''
      pitch = Pitch(self.name, 4)
      pitch_class = pitch.pitch_class
      return pitch_class

   ## PUBLIC METHODS ##

   def transpose(self, mdi):
      '''Transpose pitch class by melodic diatonic interval.'''
      ## TODO: implement ##
      raise Exception(NotImplemented)
