from abjad.components.Container._ContainerFormatterNumberInterface import \
   _ContainerFormatterNumberInterface
from abjad.components.Container._ContainerFormatterSlotsInterface import \
   _ContainerFormatterSlotsInterface
from abjad.components._Component._ComponentFormatter import _ComponentFormatter


class _ContainerFormatter(_ComponentFormatter):
   '''Encapsulate all container format logic. ::

      abjad> container = Container(macros.scale(4))
      abjad> container.formatter
      <_Container>
   '''

   def __init__(self, client):
      '''Init as type of component formatter.
      Acquire read-only references to number and slots interfaces.'''

      _ComponentFormatter.__init__(self, client)
      self._number = _ContainerFormatterNumberInterface(self)
      self._slots = _ContainerFormatterSlotsInterface(self)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _contents(self):
      '''Read-only list of tabbed lines of content.
      '''
      result = [ ]
      for m in self._client._music:
         result.extend(m.format.split('\n'))
      result = ['\t' + x for x in result]
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def container(self):
      '''Read-only reference to container that this interface serves.
      .. todo:: Make private and remove from public interface.'''

      return self._client

   @property
   def number(self):
      '''Read-only reference to
      :class:`~abjad.components.Container.number._ContainerFormatterNumberInterface`. ::

         abjad> container = Container(macros.scale(4))
         abjad> container.formatter.number
         <_ContainerFormatterNumberInterface>'''

      return self._number

   @property
   def slots(self):
      '''Read-only reference to
      :class:`~abjad.components.Container.slots._ContainerFormatterSlotsInterface`. ::

         abjad> container = Container(macros.scale(4))
         abjad> container.formatter.slots
         <_ContainerFormatterSlotsInterface>'''

      return self._slots
