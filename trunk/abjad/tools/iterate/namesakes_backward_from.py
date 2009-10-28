def namesakes_backward_from(component):
   r'''.. versionadded:: 1.1.2

   Yield right-to-left namesakes of `component` starting
   from `component`. ::

      abjad> container = Container(Staff(construct.run(2)) * 2)
      abjad> container.parallel = True
      abjad> container[0].name = 'staff 1'
      abjad> container[1].name = 'staff 2'
      abjad> score = Score([ ])
      abjad> score.parallel = False
      abjad> score.extend(container * 2)
      abjad> pitchtools.diatonicize(score)
      abjad> print score.format
      \new Score {
              <<
                      \context Staff = "staff 1" {
                              c'8
                              d'8
                      }
                      \context Staff = "staff 2" {
                              e'8
                              f'8
                      }
              >>
              <<
                      \context Staff = "staff 1" {
                              g'8
                              a'8
                      }
                      \context Staff = "staff 2" {
                              b'8
                              c''8
                      }
              >>
      }

   ::

      abjad> for staff in iterate.namesakes_backward_from(score[-1][0]):
      ...     print staff.format
      ... 
      \context Staff = "staff 1" {
              g'8
              a'8
      }
      \context Staff = "staff 1" {
              c'8
              d'8
      }
   '''

   cur_component = component

   while cur_component is not None:
      yield cur_component
      cur_component = cur_component._navigator._prevNamesake

      #if not backward:
      #   cur_component = cur_component._navigator._nextNamesake
      #else:
      #   cur_component = cur_component._navigator._prevNamesake
