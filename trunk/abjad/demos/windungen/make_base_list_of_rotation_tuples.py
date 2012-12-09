def make_base_list_of_rotation_tuples(staff_index_bounds_tuple, rotation_bandwidth, compressed_reflections):
    if compressed_reflections == True:
        rotations = make_base_list_of_compressed_rotation_tuples(staff_index_bounds_tuple, rotation_bandwidth)
    else:
        make_base_list_of_uncompressed_rotation_tuples(staff_index_bounds_tuple, rotation_bandwidth)
    return rotations
