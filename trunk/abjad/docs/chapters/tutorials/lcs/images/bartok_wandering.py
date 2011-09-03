from abjad import *

# create high level framework

piano = PianoStaff([])

upper_staff = Staff([])
lower_staff = Staff([])

piano.append(upper_staff)
piano.append(lower_staff)

m1 = Measure((2, 4), [])
m2 = Measure((3, 4), [])
m3 = Measure((2, 4), [])
m4 = Measure((2, 4), [])
m5 = Measure((2, 4), [])
upper_measures = [m1, m2, m3, m4, m5]
lower_measures = componenttools.copy_components_and_covered_spanners(upper_measures)

upper_staff.extend(upper_measures)
lower_staff.extend(lower_measures)

# add notes to upper measures

upper_measures[0].extend([Note(i, (1, 8)) for i in [9, 7, 5, 4]])
upper_measures[1].extend(notetools.make_notes([2,7,5,4,2], [(1, 4)]+[(1, 8)]*4))
notes = notetools.make_notes([0,2,4,5,4], [(1, 8), (1, 16), (1, 16), (1, 8), (1, 8)])
upper_measures[2].extend(notes)
upper_measures[3].append(Note(2, (1, 2)))
upper_measures[4].append(Note(2, (1, 2)))


# add notes to lower measures

v2 = Voice(notetools.make_notes([-1, 2, 0], [(1, 4), (1, 8), (1, 8)]))
v2[1].dynamics.mark = 'pp'
v2.name ='v2'
lower_measures[0].append(v2)

v2 = Voice(notetools.make_notes([-1, -3, -4, 0, -2],
    [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)]))
v2[3].dynamics.mark = 'mp'
v2.name = 'v2'
lower_measures[1].append(v2)

v2 = Voice(notetools.make_notes([-3, -5, -6, -5, -3],
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
p.is_parallel = True
lower_measures[3].append(p)

v1b= Voice([Note(-1, (1, 2))])
v1b.name = 'v1'
v1b.voice.number = 1
v2b= Voice([Note(-5, (1, 2))])
v2b.name = 'v2'
v2b.voice.number = 2

p = Container([v1b, v2b])
p.is_parallel = True
lower_measures[4].append(p)

# embelish
# upper staff

upper_measures[0][0].dynamics.mark = 'pp'
spannertools.BeamSpanner(upper_measures[0])

upper_measures[1][1].dynamics.mark = 'mp'
spannertools.BeamSpanner(upper_measures[1][1:])

spannertools.BeamSpanner(upper_measures[2][0:3])
spannertools.BeamSpanner(upper_measures[2][3:])

tietools.TieSpanner(upper_staff[-2:])
spannertools.SlurSpanner(upper_staff.leaves[0:5])
spannertools.SlurSpanner(upper_staff.leaves[5:])
CrescendoSpanner(upper_staff.leaves[-7:-2])
DecrescendoSpanner(upper_staff.leaves[-2:])
tx = Text(upper_staff.leaves[-7:])
tx.bound_details__left__text = markuptools.Markup('ritard.')

# lower staff

lower_staff.clef.forced = stafftools.Clef('bass')

tietools.TieSpanner([v1a[0], v1b[0]])

spannertools.BeamSpanner(lower_staff.leaves[1:5])
spannertools.BeamSpanner(lower_staff.leaves[6:10])
spannertools.BeamSpanner(lower_staff.leaves[10:13])

spannertools.SlurSpanner(lower_staff.leaves[1:6])
slr = spannertools.SlurSpanner(lower_staff.leaves[6:13] + [v2a, v2b])
slr.position = 'down'

lower_staff.barline.kind = '||'

print componenttools.is_well_formed_component(piano)
f(piano)
show(piano)
