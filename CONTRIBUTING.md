# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators.
Feel free to open issues and label them accordingly.

Before sending a Pull Request, please make sure that you're assigned the task on a GitHub issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitHub.
- If no relevant issue exists, open a new issue and get it assigned to yourself on GitHub.


## Developing MOE

Please note that in order to keep a homogenious naming convention, you might have to name your implementations of **Reader**, **Writer** and **Mailer** with a name ending in `-er` (:

1. Install requirements:

    ```bash
    git clone https://gitlab.com/cegal/MOE.git
    cd MOE
    # activate your python venv
    pip install -r requirements.txt
    ```


2. Make your changes in a git branch with the same name and number as the Issue it is assigned to (e.g. Issue `Add Hello World Support #42` => Branch `add-hello-world-support-42`).


3. (Optional) If your contribution adds/modifies `MOE`s functionality, please add appropriate (unit/integration) test.
Tests can be found under `/test`.


4. (Optional) If your contribution adds/modifies `MOE`s functionality, please add appropriate documentation in [Google Style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).
Documentation can be found under `/docs`. If no new files have been added, you can simply call `make html` to verify the generated docs. If new files were added you can add them to the documentation with `sphinx-apidoc -o docs/source <PATH TO THE FILE>`.


5. (Optional) If your contribution requires extra dependencies, please mention it in the Pull Request and update project's depencencies:
    ```bash
      pip freeze > requirements.txt
    ```

