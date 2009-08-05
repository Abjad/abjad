from abjad import *

## create high level framework

piano = PianoStaff([ ])

upper_staff = Staff([ ])
lower_staff = Staff([ ])

piano.append(upper_staff)
piano.append(lower_staff)

m1 = RigidMeasure((2, 4), [ ])
m2 = RigidMeasure((3, 4), [ ])
m3 = RigidMeasure((2, 4), [ ])
m4 = RigidMeasure((2, 4), [ ])
m5 = RigidMeasure((2, 4), [ ])
upper_measures = [m1, m2, m3, m4, m5]
lower_measures = clone.covered(upper_measures)

upper_staff.extend(upper_measures)
lower_staff.extend(lower_measures)

## add notes to upper measures

upper_measures[0].extend([Note(i, (1, 8)) for i in [9, 7, 5, 4]])
upper_measures[1].extend(construct.notes([2,7,5,4,2], [(1, 4)]+[(1, 8)]*4))
notes = construct.notes([0,2,4,5,4], [(1, 8), (1, 16), (1, 16), (1, 8), (1, 8)])
upper_measures[2].extend(notes)
upper_measures[3].append(Note(2, (1, 2)))
upper_measures[4].append(Note(2, (1, 2)))


## add notes to lower measures

v2 = Voice(construct.notes([-1, 2, 0], [(1, 4), (1, 8), (1, 8)]))
v2[1].dynamics.mark = 'pp'
v2.name ='v2'
lower_measures[0].append(v2)

v2 = Voice(construct.notes([-1, -3, -4, 0, -2], 
   [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)]))
v2[3].dynamics.mark = 'mp'
v2.name = 'v2'   
lower_measures[1].append(v2)

v2 = Voice(construct.notes([-3, -5, -6, -5, -3], 
   [(1, 8), (1, 8), (1, 8), (1, 16), (1, 16)]))
v2.name = 'v2'   
lower_measures[2].append(v2)


v1a= Voice([Note(-1, (1, 2))])
v1a.name = 'v1'
v1a.voice.number = 1
v2a= Voice([Note(-1, (1, 4)), Note(-3, (1, 4))])
v2a.name = 'v2'
v2a.voice.number = 2
p = Container([v1a, v2a])
p.parallel = True
lower_measures[3].append(p)

v1b= Voice([Note(-1, (1, 2))])
v1b.name = 'v1'
v1b.voice.number = 1
v2b= Voice([Note(-5, (1, 2))])
v2b.name = 'v2'
v2b.voice.number = 2

p = Container([v1b, v2b])
p.parallel = True
lower_measures[4].append(p)

## embelish
## upper staff

upper_measures[0][0].dynamics.mark = 'pp'
Beam(upper_measures[0])

upper_measures[1][1].dynamics.mark = 'mp'
Beam(upper_measures[1][1:])

Beam(upper_measures[2][0:3])
Beam(upper_measures[2][3:])

Tie(upper_staff[-2:])
Slur(upper_staff.leaves[0:5])
Slur(upper_staff.leaves[5:])
Crescendo(upper_staff.leaves[-7:-2])
Decrescendo(upper_staff.leaves[-2:])
tx = Text(upper_staff.leaves[-7:])
tx.bound_details__left__text = Markup('ritard.')

## lower staff 

lower_staff.clef.forced = Clef('bass')

Tie([v1a[0], v1b[0]])

Beam(lower_staff.leaves[1:5])
Beam(lower_staff.leaves[6:10])
Beam(lower_staff.leaves[10:13])

Slur(lower_staff.leaves[1:6])
slr = Slur(lower_staff.leaves[6:13] + [v2a, v2b])
slr.position = 'down'

lower_staff.barline.kind = '||'

print check.wf(piano)
f(piano)
show(piano)

#ps = PianoStaff([ ])
#
#s = Staff([ ])
#m = RigidMeasure((2, 4), [Note(i, (1, 8)) for i in [9, 7, 5, 4]])
#m[0].dynamics.mark = 'pp'
#Beam(m)
#s.append(m)
#m = RigidMeasure((3, 4), construct.notes([2,7,5,4,2], [(1, 4)]+[(1, 8)]*4))
#m[1].dynamics.mark = 'mp'
#Beam(m[1:])
#s.append(m)
#m = RigidMeasure((2, 4), 
#   construct.notes([0,2,4,5,4], [(1, 8), (1, 16), (1, 16), (1, 8), (1, 8)]))
#Beam(m[0:3])
#Beam(m[3:])
#s.append(m)
#m = RigidMeasure((2, 4), [Note(2, (1, 2))])
#s.append(m)
#m = RigidMeasure((2, 4), [Note(2, (1, 2))])
#s.append(m)
#Tie(s[-2:])
#Slur(s.leaves[0:5])
#Slur(s.leaves[5:])
#Crescendo(s.leaves[-7:-2])
#Decrescendo(s.leaves[-2:])
#ts = Text(s.leaves[-7:])
#ts.bound_details__left__text = Markup('ritard.')
#
#ps.append(s)
#
#s = Staff([ ])
#s.clef.forced = Clef('bass')
#v2 = Voice(construct.notes([-1, 2, 0], [(1, 4), (1, 8), (1, 8)]))
#v2[1].dynamics.mark = 'pp'
#v2.name ='v2'
#m = RigidMeasure((2, 4), [v2])
#s.append(m)
#v2 = Voice(construct.notes([-1, -3, -4, 0, -2], 
#   [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)]))
#v2[3].dynamics.mark = 'mp'
#v2.name = 'v2'   
#m = RigidMeasure((3, 4), [v2])
#s.append(m)
#v2 = Voice(construct.notes([-3, -5, -6, -5, -3], 
#   [(1, 8), (1, 8), (1, 8), (1, 16), (1, 16)]))
#v2.name = 'v2'   
#m = RigidMeasure((2, 4), [v2])
#s.append(m)
#v1a= Voice([Note(-1, (1, 2))])
#v1a.name = 'v1'
#v1a.voice.number = 1
#v2a= Voice([Note(-1, (1, 4)), Note(-3, (1, 4))])
#v2a.name = 'v2'
#v2a.voice.number = 2
#p = Container([v1a, v2a])
#p.parallel = True
#m = RigidMeasure((2, 4), [p])
##m = RigidMeasure((2, 4), [v1a, v2a])
#s.append(m)
#v1b= Voice([Note(-1, (1, 2))])
#v1b.name = 'v1'
#v1b.voice.number = 1
#v2b= Voice([Note(-5, (1, 2))])
#v2b.name = 'v2'
#v2b.voice.number = 2
#p = Container([v1b, v2b])
#p.parallel = True
#m = RigidMeasure((2, 4), [p])
##m = RigidMeasure((2, 4), [v1b, v2b])
#s.append(m)
#s.barline.kind = '||'
#Tie([v1a[0], v1b[0]])
#
#Beam(s.leaves[1:5])
#Beam(s.leaves[6:10])
#Beam(s.leaves[10:13])
#
#Slur(s.leaves[1:6])
#slr = Slur(s.leaves[6:13] + [v2a, v2b])
#slr.position = 'down'
#
#ps.append(s)
#print check.wf(ps)
#f(ps)
#show(ps)
