def make_base_list_of_uncompressed_rotation_tuples(staff_index_bounds_tuple, rotation_bandwidth):
    lower_bound = staff_index_bounds_tuple[0]
    upper_bound = staff_index_bounds_tuple[1]
    bit_list = range(lower_bound, upper_bound)
    rotations = [bitList[x:x + rotation_bandwidth] for x in range(len(bitList) - rotation_bandwidth + 1)]
    return rotations
