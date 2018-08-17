# Contribution guidelines

I am completely open to suggestions, criticism, and collaborators.
Feel free to open issues and label them accordingly.

Before sending a Pull Request, please make sure that you're assigned the task on a GitLab issue.

- If a relevant issue already exists, discuss on the issue and get it assigned to yourself on GitLab.

- If no relevant issue exists, open a new issue and get it assigned to yourself on GitLab.

## Git Workflow

This project follows a simple Git Workflow [**[1](https://gist.github.com/jbenet/ee6c9ac48068889b0912)**][**[2](https://www.atlassian.com/blog/git/simple-git-workflow-simple)**]:

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

- Your code must pass the Pylint and Flake8 linters, as well as remove trailing whitespace of all Python files. You may find useful my configuration file for **[VSCode](https://gitlab.com/cegal/MOE/snippets/1745921)** and **[editorconfig](https://gitlab.com/cegal/MOE/snippets/1745923)**.


- If your contribution adds/modifies `MOE`s functionality, please add appropriate (unit/integration) test.
Tests can be found under `/test`.

- If your contribution adds/modifies `MOE`s functionality, please add appropriate documentation to your code in **[Google Style](https://github.com/google/styleguide/blob/gh-pages/pyguide.md)**. Documentation can be found under `/docs`.  
If no new files have been added, you can simply call `make html` to verify the generated docs. If new files were added you can add them to the documentation with `sphinx-apidoc -o docs/source <PATH TO THE FILE>`.

- If your contribution requires extra dependencies, please mention it in the Pull Request and update project's depencencies: `pip freeze > requirements.txt`

# Vulnerabilities

If you find any vulnerabilities, **please** open an Issue and add the label `Vulnerability`. It will be handled as top priority issue.
