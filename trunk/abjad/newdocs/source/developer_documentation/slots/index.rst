Using slots
===========


Consider the definition of this class::

   class Foo(object)

      def __init__(self, a, b, c):
         self.a = a
         self.b = b
         self.c = c

1000 objects consume 176k::

   from guppy import hpy
   hp = hpy()
   hp.setrelheap()
   objects = [Foo(1, 2, 3) for x in range(1000)]
   h = hp.heap()
   print h

::

   Partition of a set of 2004 objects. Total size = 176536 bytes.
    Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
        0   1000  50   140000  79    140000  79 dict of __main__.FooWithInstanceAttribute
        1   1000  50    32000  18    172000  97 __main__.FooWithInstanceAttribute
        2      1   0     4132   2    176132 100 list
        3      1   0      348   0    176480 100 types.FrameType
        4      1   0       44   0    176524 100 __builtin__.weakref
        5      1   0       12   0    176536 100 int

But consider the definition of this class::

   class FooWithSlots(object):

      __slots__ = ('a', 'b', 'c')
      def __init__(self, a, b, c):
         self.a = a
         self.b = b
         self.c = c

1000 objects consume only 40k::

   from guppy import hpy
   hp = hpy()
   hp.setrelheap()
   objects = [FooWithSlots(1, 2, 3) for x in range(1000)]
   h = hp.heap()
   print h

::

   Partition of a set of 1004 objects. Total size = 40536 bytes.
    Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
        0   1000 100    36000  89     36000  89 __main__.Bar
        1      1   0     4132  10     40132  99 list
        2      1   0      348   1     40480 100 types.FrameType
        3      1   0       44   0     40524 100 __builtin__.weakref
        4      1   0       12   0     40536 100 int

The example here confirms the Python Reference Manual 3.4.2.4:
"By default, instances of both old and new-style classes have a dictionary 
for attribute storage. This wastes space for objects having very 
few instance variables. The space consumption can become acute when 
creating large numbers of instances."
