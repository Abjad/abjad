
def diatonic_to_chromatic(num):
   '''
   Map diatonic scale degree to chromatic scale degree.
   Scale degrees are 0 based.
   0 --> 0
   1 --> 2
   2 --> 4
   3 --> 5
   4 --> 7
   etc..
   '''
   assert isinstance(num, int)
   dic = {0:0, 1:2, 2:4, 3:5, 4:7, 5:9, 6:11}
   pclass = num % 7
   octave = num // 7
   return 12 * octave + dic[pclass]

