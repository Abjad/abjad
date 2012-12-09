def make_base_list_of_compressed_rotation_tuples(staff_index_bounds_tuple, rotation_bandwidth):
    lower_bound = staff_index_bounds_tuple[0]
    upper_bound = staff_index_bounds_tuple[1]
    bit_list = range(lower_bound - 1, upper_bound + 1)
    rotations = [bit_list[x:x + rotation_bandwidth] for x in range(0, len(bit_list) - rotation_bandwidth + 1)]
    del(rotations[0][0])
    del(rotations[-1][-1])
    return rotations
