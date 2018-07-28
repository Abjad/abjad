Abjad Packaging Checklist
=========================

Pre-packaging
-------------

- Open a branch for the new release: `release/x.y.z`
- Remove references in the documentation to old events or no-longer-supported
  versions of Python.
- Verify that Abjad can be installed and run on an OSX machine, a Linux
  machine, and a Windows machine. A virtual machine is acceptable for running
  windows.
- Verification includes: 
  - Installation of Abjad and all dependencies, extension packages, and
    third-party tools such as LilyPond and Graphviz.
  - Running the test suite, including mypy.
  - Building the documentation.
  - Sanity checking `show()` and `play()`.
  - Sanity check that the documentation looks acceptable.
  - Running a Jupyter notebook with the IPython extension.
- Fix any errors encountered during verification, push to the branch and
  re-verify on all platforms.

Packaging
---------

- Merge your release branch into master.
- Create a release entry and tag on GitHub.
- Have your PyPI credentials on hand.
- Run `make release`. This will build the package, including the docs, push the
  built package to PyPI and push the docs to our docs server.
- Sanity check that the published release works as expected by installing it
  into a new virtual environment.

Post-release
------------

- Bump the version number in `abjad/_version.py` and push to master.
- Announce on appropriate mailing lists.
