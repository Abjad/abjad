import os

import abjad

configuration = abjad.Configuration()

path_1 = os.path.join(configuration.abjad_directory, "test_1.ly")
path_2 = os.path.join(configuration.abjad_directory, "test_2.ly")

lines = [
    r'\language "english"',
    "",
    r"\new Staff {",
    "    c'4",
    "    d'4",
    "    e'4",
    "    f'4",
]


def test_iox_compare_files_01():
    """
    Is true when lines are exactly the same.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = first_lines[:]
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert abjad.iox._compare_lys(path_1, path_2)


def test_iox_compare_files_02():
    """
    Is true when version strings differ.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = [r'\version "2.19.8"'] + lines
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert abjad.iox._compare_lys(path_1, path_2)


def test_iox_compare_files_03():
    """
    Is true when comments differ.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = ["% 2014-01-01 05:43:01", r'\version "2.19.8"'] + lines
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert abjad.iox._compare_lys(path_1, path_2)


def test_iox_compare_files_04():
    """
    False when any other lines differ.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = [r'\version "2.19.7"'] + lines
        second_lines = [r'\version "2.19.8"'] + lines + ["foo"]
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert not abjad.iox._compare_lys(path_1, path_2)


### TEXT FILES ###

path_1 = os.path.join(configuration.abjad_directory, "test_1.py")
path_2 = os.path.join(configuration.abjad_directory, "test_2.py")


def test_iox_compare_files_05():
    """
    Is true when lines are exactly the same.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = first_lines[:]
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert abjad.iox._compare_text_files(path_1, path_2)


def test_iox_compare_files_06():
    """
    Is true when white space differs.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'", "", "", "print 'goodbye'", ""]
        second_lines = ["", "print 'hello'", "print 'goodbye'"]
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert abjad.iox._compare_text_files(path_1, path_2)


def test_iox_compare_files_07():
    """
    False when any other lines differ.
    """

    with abjad.FilesystemState(remove=[path_1, path_2]):
        first_lines = ["print 'hello'"]
        second_lines = ["print 'goodbye'"]
        with open(path_1, "w") as file_pointer:
            file_pointer.write("\n".join(first_lines))
        with open(path_2, "w") as file_pointer:
            file_pointer.write("\n".join(second_lines))
        assert not abjad.iox._compare_text_files(path_1, path_2)
