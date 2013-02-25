from abjad import *
from random import *

def make_base_list_of_compressed_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth):
	lowerBound = staffIndexBoundsTuple[0]
	upperBound = staffIndexBoundsTuple[1]
	bitList = range(lowerBound - 1, upperBound + 1)
	rotations = [ bitList[x:x+rotationBandwidth] for x in range(0, len(bitList) - rotationBandwidth + 1) ]
	del(rotations[0][0])
	del(rotations[-1][-1])
	return rotations

def make_base_list_of_uncompressed_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth):
	lowerBound = staffIndexBoundsTuple[0]
	upperBound = staffIndexBoundsTuple[1]
	bitList = range(lowerBound, upperBound)
	rotations = [ bitList[x:x+rotationBandwidth] for x in range( len(bitList) - rotationBandwidth + 1) ]
	return rotations

def make_base_list_of_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth, compressedReflections):
	if compressedReflections == True:
		rotations = make_base_list_of_compressed_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth)
	else:
		make_base_list_of_uncompressed_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth)
	return rotations

def mirror_base_list_of_rotation_tuples(rotations):
	copied = rotations[1:-1]
	copied.reverse()
	back = copied
	rotations.extend( back )
	return rotations

def make_mirrored_base_list_of_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth, compressedReflections):
	rotations = make_base_list_of_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth, compressedReflections)
	rotations = mirror_base_list_of_rotation_tuples(rotations)
	return rotations

def make_cyclic_matrix_for_rotation_by_bandwidth(staffIndexBoundsTuple, rotationBandwidth, compressedReflections = True):
	#generalized to any number of staffs and any bandwidth of rotation.
	#if compression is true, range is 0 to 7; then pop off first and last.
	rotations = make_mirrored_base_list_of_rotation_tuples(staffIndexBoundsTuple, rotationBandwidth, compressedReflections)
	matrix = sequencetools.CyclicMatrix(rotations)
	return matrix
	#Each cyclic tuple in the matrix indicates which staffs to place music on.

def choose_pitch_without_repetition(pitch, choices):
	chosen = pitch
	while chosen == pitch:
		candidate = choice(choices)
		if candidate != pitch:
			chosen = candidate
	return chosen

def make_staff_with_random_pitches(choices, numPitches):
	#specific to Windungen
	notes = [ ]
	pitchList = choices
	chosen = choices[-1]
	for x in range(numPitches):
		pitch = choose_pitch_without_repetition(chosen, choices)
		chosen = pitch
		note = Note(pitch, Duration(1,16) )
		notes.append( note )
	staff = Staff(notes)
	return staff

def pair_pitches_with_splits(matrix, splits, phaseOffset):
	splitTuplePairs = [ ]
	for x in range( len(splits) ):
		pair = matrix[x + phaseOffset], splits[x]
		splitTuplePairs.append(pair)
	return splitTuplePairs

def add_split_to_score_by_tuple(split, score, tuple):
	for x,staff in enumerate(score):
		if x in tuple:
			copied = componenttools.copy_components_and_covered_spanners(split)
			score[x].extend(copied[:])
		else:
			duration = sum( [y.written_duration for y in split] )
			duration = Duration( duration )
			leaves = leaftools.make_tied_leaf(Rest, duration)
			score[x].extend( leaves )

def add_splits_to_score_by_tuples(score, splitTuplePairs):
	for pair in splitTuplePairs:
		theTuple = pair[0]
		split = pair[1]
		add_split_to_score_by_tuple(split, score, theTuple)

def fuse_rests_in_beat(beat):
	for group in componenttools.yield_topmost_components_grouped_by_type(beat):
		if isinstance(group[0], Rest):
			leaftools.fuse_leaves( group[:] )

def fuse_rests_in_staff_by_beats(beats):
	for beat in beats:
		fuse_rests_in_beat(beat)

def apply_beam_spanner_to_non_rest_beat(beat):
	if not all( [isinstance(x,Rest) for x in beat] ):
		beamtools.BeamSpanner(beat[:],'up')

def apply_beam_spanner_to_non_rest_beats(beats):
	for beat in beats:
		apply_beam_spanner_to_non_rest_beat(beat)

def beam_and_fuse_beats_in_score_by_durations(score, durations, cyclic=False):
	for staff in score:
		beats = componenttools.split_components_at_offsets(staff.leaves, durations, cyclic=cyclic)
		fuse_rests_in_staff_by_beats(beats)
		beats = componenttools.split_components_at_offsets(staff.leaves, durations, cyclic=cyclic)
		apply_beam_spanner_to_non_rest_beats(beats)

def fuse_consecutive_rests_of_duration_by_duration_threshold(run, duration, durationThreshold):
	toFuse = [x for x in run[:] if x.written_duration == duration]
	runDuration = componenttools.sum_duration_of_components(run[:])
	if durationThreshold <= runDuration:
		leaftools.fuse_leaves(toFuse)

def fuse_large_rests_of_duration_in_bar_by_duration_threshold(bar, duration, durationThreshold):
	for run in componenttools.yield_topmost_components_grouped_by_type(bar):
		fuse_consecutive_rests_of_duration_by_duration_threshold(run, duration, durationThreshold )

def fuse_large_rests_of_duration_in_bars_by_duration_threshold(bars, duration, durationThreshold):
	for bar in bars:
		fuse_large_rests_of_duration_in_bar_by_duration_threshold(bar, duration, durationThreshold )

def fuse_large_rests_of_duration_in_score_by_duration_threshold(score, duration, durationThreshold):
	for staff in score:
		bars = componenttools.split_components_at_offsets(staff.leaves, [Duration(4,4)], cyclic=True, tie_split_notes=False)
		fuse_large_rests_of_duration_in_bars_by_duration_threshold(bars, duration, durationThreshold)

def set_vertical_positioning_pitch_on_rest_in_staff(staff, pitch):
	for rest in iterationtools.iterate_rests_in_expr(staff):
		resttools.set_vertical_positioning_pitch_on_rest(rest, pitch)

def clean_up_rests_in_score(score):
	fuse_large_rests_of_duration_in_score_by_duration_threshold(score, Duration(1,4), Duration(3,4) )
	fuse_large_rests_of_duration_in_score_by_duration_threshold(score, Duration(1,4), Duration(2,4) )
	for staff in score:
		set_vertical_positioning_pitch_on_rest_in_staff(staff, "d")


def rotate_expression_through_adjacent_staffs_at_bandwidth_by_durations(expression, staffIndexBoundsTuple, rotationBandwidth, durations, compressedReflections=True, cyclic=False, phaseOffset= 0):
	matrix = make_cyclic_matrix_for_rotation_by_bandwidth( staffIndexBoundsTuple, rotationBandwidth, compressedReflections=compressedReflections )
	splits = componenttools.split_components_at_offsets(expression.leaves, durations, cyclic=cyclic, tie_split_notes=False)
	splitTuplePairs = pair_pitches_with_splits(matrix, splits, phaseOffset)
	add_splits_to_score_by_tuples(score, splitTuplePairs)
	beam_and_fuse_beats_in_score_by_durations(score, [Duration(1,4)],cyclic=True)
	clean_up_rests_in_score(score)

def make_empty_cello_score(numStaffs):
	score = Score([])
	for x in range(numStaffs):
		score.append( Staff([]) )
		contexttools.ClefMark('bass')(score[x])
		score[x].override.stem.stemlet_length = 2
		score[x].override.beam.damping = "+inf.0"
	return score

score = make_empty_cello_score(12)
pitches = sequencetools.repeat_sequence_to_length([-11, -10, -8], 32)
#rotate_expression_through_adjacent_staffs_at_bandwidth_by_durations(
#    pitches, (0, 12), 4, [Duration(1, 16)], compressedReflections=True, cyclic=True)
#show(score)
