def namesakes_from(component, backwards = False):
   r'''Yield left-to-right namesakes of `component` starting
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

      abjad> for staff in iterate.namesakes_from(score[0][0]):
      ...     print staff.format
      ... 
      \context Staff = "staff 1" {
              c'8
              d'8
      }
      \context Staff = "staff 1" {
              g'8
              a'8
      }

   When ``backwards = True`` yield right-to-left. ::

      abjad> for staff in iterate.namesakes_from(score[-1][0], backwards = True):
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
      if not backwards:
         cur_component = cur_component._navigator._nextNamesake
      else:
         cur_component = cur_component._navigator._prevNamesake
