from collections import Iterable
from numbers import Number
from abjad.core import _Immutable


class QEvent(_Immutable):

   __slots__ = ('_offset', '_duration', '_value')

   def __new__(klass, offset, duration, value):
      self = object.__new__(klass)
      assert isinstance(offset, Number)
      assert isinstance(duration, Number) and 0 < duration
      assert isinstance(value, (Number, Iterable, type(None)))
      if isinstance(value, Iterable):
         assert all([isinstance(x, Number) for x in value])
         object.__setattr__(self, '_value', tuple(sorted(set(value))))
      else:
         object.__setattr__(self, '_value', value)
      object.__setattr__(self, '_offset', offset)
      object.__setattr__(self, '_duration', duration)
      return self

   def __getnewargs__(self):
      return self.offset, self.duration, self.value

   ## OVERRIDES ##

   def __eq__(self, other):
      if type(self) == type(other):
         if self.offset == other.offset:
            if self.duration == other.duration:
               if self.value == other.value:
                  return True
      return False

   def __repr__(self):
      return '%s(%s)' % (self.__class__.__name__, self._format_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _format_string(self):
      return ', '.join([repr(x) for x in
         [self.offset, self.duration, self.value]])

   ## PUBLIC ATTRIBUTES ##

   @property
   def duration(self):
      return self._duration

   @property
   def offset(self):
      return self._offset

   @property
   def value(self):
      return self._value
