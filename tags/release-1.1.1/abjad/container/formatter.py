from abjad.container.number import _ContainerFormatterNumberInterface
from abjad.container.slots import _ContainerFormatterSlotsInterface
from abjad.component.formatter import _ComponentFormatter


class _ContainerFormatter(_ComponentFormatter):
   '''Encapsulate all container format logic. ::

      abjad> container = Container(construct.scale(4))
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
      .. todo:: Return (immutable) tuple instead of (mutable) list..'''

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
      :class:`~abjad.container.number._ContainerFormatterNumberInterface`. ::

         abjad> container = Container(construct.scale(4))
         abjad> container.formatter.number
         <_ContainerFormatterNumberInterface>'''

      return self._number

   @property
   def slots(self):
      '''Read-only reference to
      :class:`~abjad.container.slots._ContainerFormatterSlotsInterface`. ::

         abjad> container = Container(construct.scale(4))
         abjad> container.formatter.slots
         <_ContainerFormatterSlotsInterface>'''

      return self._slots

#   @property
#   def wrapper(self):
#      r'''Read-only string representation of all parts of container
#      format except container contents. ::
#
#         abjad> container = Container(construct.scale(12))
#         abjad> container.notehead.color = 'red'
#         abjad> container.notehead.style = 'harmonic'
#         abjad> container.comments.before.append('Container comments')
#         abjad> print container.formatter.wrapper
#         {
#                 \override NoteHead #'style = #'harmonic
#                 \override NoteHead #'color = #red
#
#                 %%% 12 components omitted %%%
#
#                 \revert NoteHead #'style
#                 \revert NoteHead #'color
#         }
#      '''
#
#      result = [ ]
#      result.extend(self.slots.contributions('slot_1'))
#      result.extend(self.slots.contributions('slot_2'))
#      result.extend(self.slots.contributions('slot_3'))
#      heart = '\t%%%%%% %s components omitted %%%%%%' % len(self.container)
#      result.extend(['', heart, ''])
#      result.extend(self.slots.contributions('slot_5'))
#      result.extend(self.slots.contributions('slot_6'))
#      result.extend(self.slots.contributions('slot_7'))
#      result = '\n'.join(result)
#      return result
