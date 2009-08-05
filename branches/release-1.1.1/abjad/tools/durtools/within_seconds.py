def within_seconds(timepoint, component):
   '''True when both component.offset.seconds.start <= timepoint
      and timepoint < component.offset.seconds.stop; otherwise False.'''


   return component.offset.seconds.start <= timepoint < \
      component.offset.seconds.stop
