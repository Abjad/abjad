def mirror_base_list_of_rotation_tuples(rotations):
    copied = rotations[1:-1]
    copied.reverse()
    back = copied
    rotations.extend(back)
    return rotations
