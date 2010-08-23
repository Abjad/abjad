from abjad.components._Component import _Component
from abjad.components._Context import _Context
from fractions import Fraction


class Mark(object):
   '''.. versionadded:: 1.1.2

   'Here forward' mark.

   Mark models time signatures, key signatures, clef, dynamics
   and other score symbols that establish a score setting to remain
   in effect until the next occurrence of such a score symbol.
   '''

   __slots__ = ('_context', '_start_component', 'value')

   def __init__(self, value = None):
      self._context = None
      self._start_component = None
      self.value = value

   ## OVERLOADS ##

   def __call__(self, *args):
      if len(args) == 0:
         context = None
         start_component = None
      elif len(args) == 1:
         context = args[0]
         start_component = args[0]
      elif len(args) == 2:
         context = args[0]
         start_component = args[1]
      else:
         raise ValueError('must call mark with 0, 1 or 2 arguments only.')
      if not isinstance(context, (_Context, type(None))):
         raise TypeError('mark attachment context "%s" must be context.' % context)
      if start_component is not None:
         if not isinstance(start_component, _Component):
            raise TypeError('mark start component "%s" must be component.' % start_component)
         if not context in start_component.parentage.improper_parentage:
            raise ValueError('mark start component "%s" must be improper child ' +
               'of mark attachment context "%s".' %
               start_component, context)
      self._bind_context(context)
      self._bind_start_component(start_component)
      return self

   def __delattr__(self, *args):
      raise AttributeError('can not delete %s attributes.' % self.__class__.__name__)

   def __repr__(self):
      return '%s(%s)%s' % (
         self.__class__.__name__, self._contents_repr_string, self._attachment_repr_string)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _attachment_repr_string(self):
      if self.context is not None:
         if self.start_component is not None:
            if self.start_component is not self.context:
               return '**'
         return '*'
      return ''

   @property
   def _contents_repr_string(self):
      if self.value is not None:
         return str(self.value)
      else:
         return ' '

   ## PRIVATE METHODS ##
   
   def _bind_context(self, context):
      self._unbind_context( )
      if context is not None:
         self._context = context
         self.context._marks.append(self)

   def _bind_start_component(self, start_component):
      self._unbind_start_component( )
      if start_component is not None:
         self._start_component = start_component
         self.start_component._marks.append(self)

   def _unbind_context(self):
      if self.context is not None:
         self.context._marks.remove(self)
         self._context = None

   def _unbind_start_component(self):
      if self.start_component is not None:
         self.start_component._marks.remove(self)
         self._start_component = None

   ## PUBLIC ATTRIBUTES ##

   @property
   def context(self):
      return self._context

   @property
   def start_component(self):
      return self._start_component
