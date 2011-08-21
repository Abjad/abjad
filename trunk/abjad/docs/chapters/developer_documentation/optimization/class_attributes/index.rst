Class attributes
================


Consider the definition of this class::

   class FooWithInstanceAttribute(object):

      def __init__(self):
         self.constants = (
            'red', 'orange', 'yellow', 'green',
            'blue', 'indigo', 'violet',
            )

1000 objects consume 176k::

   from guppy import hpy
   hp = hpy()
   hp.setrelheap()
   objects = [FooWithInstanceAttribute() for x in range(1000)]
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

   class FooWithSharedClassAttribute(object):

      def __init__(self):
         pass

      self.constants = (
         'red', 'orange', 'yellow', 'green',
         'blue', 'indigo', 'violet',
         )  

1000 objects consume only 36k::

   from guppy import hpy
   hp = hpy()
   hp.setrelheap()
   objects = [FooWithClassAttribute() for x in range(1000)]
   h = hp.heap()
   print h

::

   Partition of a set of 1004 objects. Total size = 36536 bytes.
    Index  Count   %     Size   % Cumulative  % Kind (class / dict of class)
        0   1000 100    32000  88     32000  88 __main__.FooWithClassAttribute
        1      1   0     4132  11     36132  99 list
        2      1   0      348   1     36480 100 types.FrameType
        3      1   0       44   0     36524 100 __builtin__.weakref
        4      1   0       12   0     36536 100 int

Objects that share class attributes between them can consume less memory than objects that don't.
But consider the usual provisions between class attributes and instance
attributes when implementing custom classes.
Class attributes make sense when objects will never modify the attribute in question. 
Class attributes also make sense when objects will modify the attribute in question 
and will desire to change the attribute in question for all other like objects
at the same time. 
Probably best to use instance attributes in most other cases.
