from abjad.core import _Abjad


class KeySignature(_Abjad):

   def __init__(self, tonic, mode):
      from abjad.tools import pitchtools
      from abjad.tools import tonalitytools
      #self._tonic = pitchtools.NamedPitchClass(tonic)
      #self._mode = tonalitytools.Mode(mode)
      _tonic = pitchtools.NamedPitchClass(tonic)
      _mode = tonalitytools.Mode(mode)
      super(KeySignature, self).__setattr__('_tonic', _tonic)
      super(KeySignature, self).__setattr__('_mode', _mode)

   ## OVERLOADS ##

   def __delattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __eq__(self, arg):
      if isinstance(arg, KeySignature):
         if self.tonic == arg.tonic:
            if self.mode == arg.mode:
               return True
      return False

   def __ne__(self, arg):
      return not self == arg

   def __repr__(self):
      return '%s("%s", "%s")' % (self.__class__.__name__, self.tonic, self.mode)

   def __setattr__(self, *args):
      raise AttributeError('%s objects are immutable.' % self.__class__.__name__)

   def __str__(self):
      return '%s-%s' % (self.tonic, self.mode)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      return r'\key %s \%s' % (self.tonic, self.mode)

   @property
   def mode(self):
      '''Read-only mode.'''
      return self._mode

   @property
   def name(self):
      if self.mode.mode_name_string == 'major':
         tonic = self.tonic.name.upper( )   
      else:
         tonic = self.tonic.name
      return '%s %s' % (tonic, self.mode.mode_name_string)

   @property
   def tonic(self):
      '''Read-only tonic.'''
      return self._tonic
