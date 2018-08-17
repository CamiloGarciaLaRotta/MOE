# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators.
Feel free to open issues and label them accordingly.

Before sending a Pull Request, please make sure that you're assigned the task on a GitLab issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitLab.

- If no relevant issue exists, open a new issue and get it assigned to yourself on GitLab.

## Git Workflow

This project follows a simple Git Workflow [[1](https://gist.github.com/jbenet/ee6c9ac48068889b0912)][[2](https://www.atlassian.com/blog/git/simple-git-workflow-simple)]:

- Branch off the latest master and name the branch `<descriptive_name>-<issue_number>`
    ```bash
    git clone https://gitlab.com/cegal/MOE.git
    cd MOE
    # activate your python venv
    pip install -r requirements.txt

    git checkout -b add-hello-world-support-42
    ```
- Keep your branch up to date by rebasing on top of master
    ```bash
    git fetch origin
    git rebase origin/master
    ```
- When you are done, push your branch and open a  Pull Request in GitLab
    ```bash
    git push -u origin add-hello-world-support-42
    ```
- Once the Pull Request is approved, perform an explicit merge
    ```bash
    git checkout master
    git pull origin master
    git merge --no-ff add-hello-world-support-42
    ```

## Pull Request Checklist
- In order to keep a homogenious naming convention, you have to name your implementations of **Reader**, **Writer** and **Mailer** with a name ending in `-er` (:

- You may find useful my configuration file for [VSCode](https://gitlab.com/cegal/MOE/snippets/1745921) and [editorconfig](https://gitlab.com/cegal/MOE/snippets/1745923).

- It is highly recommended that you use the root [Makefile](https://gitlab.com/cegal/MOE/blob/master/Makefile) as **git pre-commit hook**, as it will do everything all for you (linting, testing, documentation)
    ```bash
    #.git/hooks/pre-commit
    #!/bin/sh

    make validate
    ```
    then `chmod +x .git/hooks/pre-commit`

- Your code must pass the linting (Pylint, Flake8), as well as remove trailing whitespace of all files.

- If your contribution adds/modifies `MOE`s functionality, please add appropriate tests.

- Please add appropriate documentation to your code in [Google Style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

- If your contribution requires extra dependencies, please mention it in the Pull Request and update project's depencencies: `pip freeze > requirements.txt`

# Vulnerabilities

If you find any vulnerabilities, **please** open an Issue and add the label `Vulnerability`. It will be handled as top priority issue.
