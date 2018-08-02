# MOE

Morse Over Ethernet

# Overview

Small DIY Raspberry Pi project for hobbyists who want to put their unused boards to good use.

`MOE` is inteded to be lightweight with respect to resource usage so that even the first generation boards can be used.

At its core, `MOE` is a morse machine:
  - It can record a morse message through a button and send it to another `MOE` over the internet.
  - It can play a received morse message through a beeper.

### Goals
- __Cheap__

    The MOE project aims to be as cost effective as possible in terms of operation, i.e not paying for server instances of any kind.

    MOE leverages the Gmail service and its API to deliver and store the messages. The only operational costs are the internet connection and the power consumption of the Raspberry Pi.

- __Modular__

    I/O devices must be added/swapped in a `MOE` without much trouble.

    For example: a printer can be added so that morse messages are printed too, a light can be added so that morse messages are blinked too.

- __Easy to setup__

    The software must be easily installable and well documented so that anyone can modify as they wish.

    The hardware must provide a basic set of downloadable schemas for 3d printing or cardboard-cutting must be available for those who want to dress up their `MOE`.

# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators.
Feel free to open issues and label them accordingly.

Before sending a Pull Request, please make sure that you're assigned the task on a GitHub issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitHub.
- If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.


## Developing MOE

1. Install requirements:

    ```bash
    git clone https://gitlab.com/cegal/MOE.git
    cd MOE
    # activate your python venv
    pip install -r requirements.txt
    ```

2. Make your changes in a git branch with the same name as the Issue it is assigned to (e.g. Issue `Add Hello World Support` => Branch `add-hello-world-support`).

3. (Optional) If your contribution adds/modifies `MOE`s functionality, please add appropriate (unit/integration) tests aswell.

4. (Optional) If your contribution requires extra dependencies, please mention it in the Pull Request and update project's depencencies:
    ```bash
      pip freeze > requirements.txt
    ```

---

Special thanks to [athityakumar](https://github.com/athityakumar), this README is in large part based on the one of his [colorls](https://github.com/athityakumar/colorls) project.
