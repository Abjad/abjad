from abjad.measure.dynamic.measure import DynamicMeasure


## TODO - The staff promotion here is naive.
##        The promotion assumes that the anonymous measure
##        sits inside an unmodified LilyPond Staff context.
##        In the case that the measure sits inside, say,
##        a LilyPond RhythmicStaff context, then the promotion
##        will be ineffectual.
##
##        What's needed is a type of 'symoblic' promotion
##        that can look into the Abjad score structure and
##        derive the enclosing staff context dynamically.
##        This will be a good extension of _StaffInterface.
##        Probably t.staff.effective should implement this.
 
class AnonymousMeasure(DynamicMeasure):

   def __init__(self, music = None):
      DynamicMeasure.__init__(self, music = music)
      self.meter.stencil = False
      self.meter.promote('stencil', 'Staff')
