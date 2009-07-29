def wrapper(container):
   r'''Read-only string representation of all parts of container
   format except container contents. ::

      abjad> container = Container(construct.scale(12))
      abjad> container.notehead.color = 'red'
      abjad> container.notehead.style = 'harmonic'
      abjad> container.comments.before.append('Container comments')
      abjad> print container.formatter.wrapper
      {
              \override NoteHead #'style = #'harmonic
              \override NoteHead #'color = #red

              %%% 12 components omitted %%%

              \revert NoteHead #'style
              \revert NoteHead #'color
      }
   '''

   from abjad.container.container import Container
   assert isinstance(container, Container)

   result = [ ]
   result.extend(container._formatter.slots.contributions('slot_1'))
   result.extend(container._formatter.slots.contributions('slot_2'))
   result.extend(container._formatter.slots.contributions('slot_3'))
   heart = '\t%%%%%% %s components omitted %%%%%%' % len(
      container._formatter.container)
   result.extend(['', heart, ''])
   result.extend(container._formatter.slots.contributions('slot_5'))
   result.extend(container._formatter.slots.contributions('slot_6'))
   result.extend(container._formatter.slots.contributions('slot_7'))
   result = '\n'.join(result)
   return result
