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

2. Make your changes in a git branch with the same name and number as the Issue it is assigned to (e.g. Issue `Add Hello World Support #42` => Branch `add-hello-world-support-42`).

3. (Optional) If your contribution adds/modifies `MOE`s functionality, please add appropriate (unit/integration) tests aswell.

4. (Optional) If your contribution requires extra dependencies, please mention it in the Pull Request and update project's depencencies:
    ```bash
      pip freeze > requirements.txt
    ```

---

Special thanks to [athityakumar](https://github.com/athityakumar), this README is in large part based on the one of his [colorls](https://github.com/athityakumar/colorls) project.
