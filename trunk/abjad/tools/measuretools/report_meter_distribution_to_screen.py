from abjad.tools.measuretools._report_meter_distribution import _report_meter_distribution


def report_meter_distribution_to_screen(expr):
   '''Report meter distribution of `expr` to screen.

   ::

      abjad> measuretools.report_meter_distribution_to_screen(t)
        2/16    62
        3/16    14
        4/16    66
        5/16    57
        6/16    17
        7/16    20
        8/16    16
        9/16    19
        10/16   4

   Return none.
   '''

   return _report_meter_distribution(expr, delivery = 'screen')
