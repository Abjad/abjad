#! /usr/bin/env python
import abjad
import datetime
import subprocess


template = """\
Abjad {abjad_version}
    Build start date: {build_start_date}
    Build complete date:
    MD5 hash of Abjad Github repository: {md5_hash}

    Packaging environment:
        0. workstation description:
        1. uname -v: {kernel_version}
        2. git --version: {git_version}
        3. python --version: {python_version}
        4. pip --version: {pip_version}
        5. py.test --version: {pytest_version}
        6. sphinx-build --version: {sphinx_build_version}
        7. lilypond --version: {lilypond_version}
        8. convert --version: {imagemagick_version}
        9. dot -V: {graphviz_version}

    Python 3.5.2 (OSX) test results:
        1. mainline py.test test results:
        2. mainline doctest test results:
        3. experimental py.test test results:
        4. experimental doctest test results:
        5. sanity check test results:
        6. experimental HTML build results:
        7. mainline HTML build results:

    Python 3.5.2 (Windows) test results:
        1. mainline py.test test results:
        2. mainline doctest test results:
        3. experimental py.test test results:
        4. experimental doctest test results:
        5. sanity check test results:

    Python 2.7.12 (OSX) test results:
        1. mainline py.test test results:
        2. mainline doctest test results:
        3. experimental py.test test results:
        4. experimental doctest test results:
        5. sanity check test results:


"""


def get_abjad_version():
    return abjad.__version__


def get_build_start_date():
    return datetime.date.today().isoformat()


def get_md5_hash():
    command = 'git log -n 1 --pretty=format:"%H"'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    return result.splitlines()[0]


def get_kernel_version():
    command = 'uname -v'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    result = result.splitlines()[0]
    return result.partition(':')[0]


def get_git_version():
    command = 'git --version'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    return result.splitlines()[0]


def get_python_version():
    command = 'python --version'
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pipe.communicate()
    return stdout.decode('utf-8').splitlines()[0]


def get_pip_version():
    command = 'pip -V'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    return result.partition(' from ')[0]


def get_pytest_version():
    command = 'py.test --version'
    pipe = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    _, stderr = pipe.communicate()
    return stderr.decode('utf-8').splitlines()[0].partition(',')[0]


def get_sphinx_build_version():
    command = 'sphinx-build --version'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    return result.splitlines()[0]


def get_lilypond_version():
    command = 'lilypond --version'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    return result.splitlines()[0]


def get_imagemagick_version():
    command = 'convert --version'
    result = subprocess.check_output(command, shell=True).decode('utf-8')
    result = result.splitlines()[0]
    return result.partition('Version: ')[-1]


def get_graphviz_version():
    command = 'dot -V'
    pipe = subprocess.Popen(command, shell=True, stderr=subprocess.PIPE)
    _, stderr = pipe.communicate()
    result = stderr.decode('utf-8').splitlines()[0]
    return result.partition('dot - ')[-1]


abjad_version = get_abjad_version()
build_start_date = get_build_start_date()
md5_hash = get_md5_hash()
kernel_version = get_kernel_version()
git_version = get_git_version()
python_version = get_python_version()
pip_version = get_pip_version()
pytest_version = get_pytest_version()
sphinx_build_version = get_sphinx_build_version()
lilypond_version = get_lilypond_version()
imagemagick_version = get_imagemagick_version()
graphviz_version = get_graphviz_version()


string = template.format(
    abjad_version=abjad_version,
    build_start_date=build_start_date,
    md5_hash=md5_hash,
    kernel_version=kernel_version,
    git_version=git_version,
    python_version=python_version,
    pip_version=pip_version,
    pytest_version=pytest_version,
    sphinx_build_version=sphinx_build_version,
    lilypond_version=lilypond_version,
    imagemagick_version=imagemagick_version,
    graphviz_version=graphviz_version,
    )

print(string)
