def within_prolated(timepoint, component):
   '''True when both component.offset.prolated.start <= timepoint
      and timepoint < component.offset.prolated.stop; otherwise False.'''


   return component.offset.prolated.start <= timepoint < \
      component.offset.prolated.stop
