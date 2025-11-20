# Programming in Python - An Introduction
This repository contains student solutions to the exercise requirements specified in the [Programming in Python - An Introduction - Kanban Board](https://github.com/orgs/programming-in-python/projects/1/views/1).

The Kanban Board provides configuration guidelines and exercises related to the *INFO 5002: Intro to Python for Information Systems* course at Northeastern University in Boston, MA, taught by [Prof. Andy King](https://andyking.me).

While the source code solutions contained herein (under `exercises` primarily) are expected to be implemented per the guidlines specified in the `DEV` modules within [Programming in Python - An Introduction - Kanban Board](https://github.com/orgs/programming-in-python/projects/1/views/1), the Python code (within `exercises`) should be implemented by the student taking the course.

Pre-defined exercise modules and test modules will contain the requisite copyright and usage license. Students may choose to select their own for work they do exclusively themselves.

## References
The exercises and tests in this repository are based on the tasks specified in the [Programming in Python - An Introduction - Kanban Board](https://github.com/orgs/programming-in-python/projects/1/views/1)

For more information on the Programming in Python - An Introduction course, please see the [README.md](https://github.com/programming-in-python/ipp-exercise-tasks).

For access to the exercise and configuration information for the *Programming in Python - An Introduction* course, please refer to [Programming in Python - An Introduction - Kanban Board](https://github.com/orgs/programming-in-python/projects/1/views/1).

## Directory Structure
The path structure in this repository is designed to be as simple as possible to align with the 10 lab modules specified in [Programming in Python - An Introduction - Kanban Board](https://github.com/orgs/programming-in-python/projects/1/views/1). The student is welcome to make changes to this structure after the course.

### Exercises
- The `exercises` aims to simply call out a package per lab module - that is, `labmodule01` is a package, yet it may contain multiple modules (or Python files). Later packages may have dependencies on earlier packages as exercises get more complex and OO concepts are applied. That is, modules defined in `labmodule03` may be useful (and used in) modules defined in, for example, `labmodule10`. It is not a goal of this course to require such dependencies, this statement is merely an acknowledgement that they may naturally exist. There are no expectations, however, that the reverse will be the case - that is, `labmodule03` should never contain any module or logic that depends upon a later lab module, such as `labmodule10`.
- Exercises path structure (SUBJECT TO CHANGE):

```
./ipp
  ./__init__.py
  ./app
    ./__init__.py
    ./IppTestApp.py
  ./common
    ./__init__.py
    ./ConfigConst.py
    ./ConfigUtil.py
    ./Singleton.py
  ./exercises
    ./__init__.py
    ./labmodule01
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule02
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule03
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule04
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule05
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule06
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule07
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule08
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule09
        ./__init__.py
        ./README.md
        ./{module(s) here}
    ./labmodule10
        ./__init__.py
        ./README.md
        ./README-PROPOSAL.md
        ./{module(s) here}
```

### A Brief FAQ
- Why the extra `ipp` in the path name?
  - This is to avoid possible confusion with other lib's when importing a solution from an earlier exercise into a later one. For instance, importing the `labmodule03` package requires inclusion of the `pip` package, as shown:
  `import ipp.exercises.labmodule03 as labmodule03`
  - While this may seem to run against the principle of simplicity, it does - IMO - improve clarity.

- What are the `README.md` files for in each `labmodule{#}` path?
  - These documentation files are for the student to complete as part of each lab module exercise. The `README.md` contains a template within the file that should be self-explanatory.

- What about the `README-PROPOSAL.md` in `labmodule10`? What is it for?
  - This is the proposal template for the semester project. Students proposing a particular use case as their `labmodule10` semester project implementation should use this template to describe what they want to do, why it's important, and provide some insights into how they plan to implement the solution.

### Tests
- The `tests` path mimics the exercises path. It contains packages for each lab module, although not all lab modules will have tests. The student may choose to add their own test(s) to correspond with exercise implementations in the exercises path.
- Tests path structure (SUBJECT TO CHANGE):

```
./tests
  ./__init__.py
  ./common
    ./__init__.py
    ./test_ConfigUtilCustom.py
    ./test_ConfigUtilDefault.py
    ./DummyCredFile.props
    ./EmptyTestConfig.props
    ./ValidTestConfig.props
  ./labmodule01
    ./__init__.py
    ./{test module(s) here}
  ./labmodule02
    ./__init__.py
    ./{test module(s) here}
  ./labmodule03
    ./__init__.py
    ./{test module(s) here}
  ./labmodule04
    ./__init__.py
    ./{test module(s) here}
  ./labmodule05
    ./__init__.py
    ./{test module(s) here}
  ./labmodule06
    ./__init__.py
    ./{test module(s) here}
  ./labmodule07
    ./__init__.py
    ./{test module(s) here}
  ./labmodule08
    ./__init__.py
    ./{test module(s) here}
  ./labmodule09
    ./__init__.py
    ./{test module(s) here}
  ./labmodule10
    ./__init__.py
    ./{test module(s) here}
```

## Links, Exercises, Updates, Errata, and Clarifications

Please see the following links to access exercises, errata / clarifications, and the e-book:
 - [Programming in Python - Kanban Board](https://github.com/orgs/programming-in-python/projects/1)
 - [Exercise Repository - ipp-exercise-components](https://github.com/orgs/programming-in-python/ipp-exercise-components/)

## How to navigate the directory structure for this repository
This repository is comprised of the following top level paths:
- [config](https://github.com/programming-in-python/ipp-exercise-components/blob/main/config): Contains basic configuration file(s).
- [exercises](https://github.com/programming-in-python/ipp-exercise-components/blob/main/piot): The top level of the 'Programming the IoT, or piot' project source code.
- [tests](https://github.com/programming-in-python/ipp-exercise-components/blob/main/tests): The top level of the 'Programming the IoT, or piot' project tests.

Here are some other files at the top level that are important to review:
- [requirements.txt](https://github.com/programming-in-python/ipp-exercise-components/blob/main/requirements.txt): The core library dependencies - use pip to install.
- [README.md](https://github.com/programming-in-python/ipp-exercise-components/blob/main/README.md): This README.
- [LICENSE](https://github.com/programming-in-python/ipp-exercise-components/blob/main/LICENSE): The repository's LICENSE file.

Lastly, here are some 'dot' ('.{filename}') files pertaining to dev environment setup that you may find useful (or not - if so, just delete them after cloning the repo):
- [.gitignore](https://github.com/programming-in-python/ipp-exercise-components/blob/main/.gitignore): The obligatory .gitignore that you should probably keep in place, with any additions that are relevant for your own cloned instance.

NOTE: The directory structure and all files are subject to change based on feedback I receive, as well as improvements I find to be helpful for overall repo betterment.

# Other things to know

## Pull requests
PR's are currently disabled.

## Updates
Much of this repository's structure, and in particular the pre-modules under the `tests` path, will continue to evolve, so please check back regularly for potential updates. Please note that API changes can - and likely will - occur at any time.

# REFERENCES
This repository has external dependencies on other open source projects.

- [apscheduler](https://github.com/agronholm/apscheduler)
  - Reference: A. Grönholm. APScheduler. (2020) [Online]. Available: https://pypi.org/project/APScheduler/.
- [psutil](https://github.com/giampaolo/psutil)
  - Reference: G. Rodola. Psutil. (2009 – 2020) [Online]. Available: https://psutil.readthedocs.io/en/latest/.
- [numpy](https://numpy.org/)
  - Reference: NumPy. NumPy. (2020) [Online]. Available: https://numpy.org/.
- [matplotlib](https://matplotlib.org/)
  - Reference: [J. D. Hunter, "Matplotlib: A 2D Graphics Environment", Computing in Science & Engineering, vol. 9, no. 3, pp. 90-95, 2007.](https://ieeexplore.ieee.org/document/4160265)
  - DOI: https://doi.org/10.5281/zenodo.592536
- [Sense-Emu](https://sense-emu.readthedocs.io/en/v1.1/)
  - Reference: The Raspberry Pi Foundation. Sense HAT Emulator. (2016) [Online]. Available: https://sense-emu.readthedocs.io/en/v1.0/.
- [pisense](https://pisense.readthedocs.io/en/release-0.2/#)
  - Reference: D. Jones. Pisense. (2016 – 2018) [Online]. Available: https://pisense.readthedocs.io/en/release-0.2/.
- [requests](https://github.com/psf/requests)
  - Reference: Python Software Foundation. Requests. (2025) [Online]. Available: https://github.com/psf/requests.

Additional Library References (for in-class examples not currently used in assignments; e.g., Computer Vision examples):

- [paho-mqtt](https://www.eclipse.org/paho/)
  - Reference: Eclipse Foundation, Inc. Eclipse Paho™ MQTT Python Client. (2020) [Online]. Available: https://github.com/eclipse/paho.mqtt.python.
- [imutils](https://pypi.org/project/imutils/)
  - Reference: A. Rosebrock. imutils. (2020) [Online]. Available: https://pypi.org/project/imutils/.
- [opencv-python](https://pypi.org/project/opencv-python/)
  - Reference: O. Heinisuo. opencv-python. (2020) [Online]. Available: https://pypi.org/project/opencv-python/.
- [opencv-python-headless](https://pypi.org/project/opencv-python-headless/)
  - Reference: O. Heinisuo. opencv-python. (2020) [Online]. Available: https://pypi.org/project/opencv-python-headless/.
- [opencv-contrib-python](https://pypi.org/project/opencv-contrib-python/)
  - Reference: O. Heinisuo. opencv-python. (2020) [Online]. Available: https://pypi.org/project/opencv-contrib-python/.
- [rtsp](https://pypi.org/project/rtsp/)
  - Reference: M. Stewart. rtsp. (2020) [Online]. Available: https://pypi.org/project/rtsp/.

NOTE: This list will be updated as others are incorporated.

# IMPORTANT NOTES
This repository is under active development.

## IPP-DOC-LIC

*Documentation - Usage and License*

This project's associated [written instructions and non-source code documentation](https://github.com/orgs/programming-in-python/projects/1) - including this `README.md` file, all [Issues](https://github.com/programming-in-python/ipp-exercise-tasks/issues), and the Notes, Instructions and Cards contained within this [Kanban Board](https://github.com/orgs/programming-in-python/projects/1) - are available under the following license:

 - Documentation: Copyright &copy; 2025 by [Andrew D. King](https://andyking.me). Licensed under <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/ " target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-NC-SA 4.0 <img height="24" style="!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img height="24" style="!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img height="24" style="!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/nc.svg?ref=chooser-v1"><img height="24" style="!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1"></a>
 - See [LICENSE](https://github.com/programming-in-python/ipp-exercise-tasks/blob/main/LICENSE) for details.

*Source Code Solutions and Examples - Usage and License*

This project's associated [written instructions](https://github.com/orgs/programming-in-python/projects/1) and [Issues](https://github.com/programming-in-python/ipp-exercise-tasks/issues) documents contain sample source codes representing examples and solutions. Unless otherwise represented, these inline source codes (Python) are available under the following license:

 - Inline Source Codes: Copyright &copy; 2025 [Andrew D. King](https://andyking.me). Licensed under [The MIT License](https://opensource.org/licenses/MIT)
 - See [LICENSE-CODE](https://github.com/programming-in-python/ipp-exercise-tasks/blob/main/LICENSE-CODE) for details.

Please refer to the referenced [ipp-exercise-components](https://github.com/programming-in-python/ipp-exercise-components) repository for its respective usage licenses, including any external dependencies and associated references.

*NOTE*

If any code samples or other technology this work contains or describes is subject to open source licenses or the intellectual property rights of others, it is your responsibility to ensure that your use thereof complies with such licenses and/or rights.

For addition information on code references used in this board, see [IPP-DOC-REF](https://github.com/programming-in-python/ipp-exercise-tasks/issues/4).


