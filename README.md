# assorted-pre-commit-hooks / gitignore

[pre-commit] hook to sanitise [Git] [ignore] files.

The hook ensures that:

* All `.gitignore` entries are sorted and free of trailing whitespace.

* No `.gitignore` entry refers to a parent directory.

* If a `.gitignore` is a path, it is checked whether there is a `.gitignore`
  file within a directory of that path that the entry can be moved to. For
  example, an entry `test/data/*.tmp` in the top-level `.gitignore` will be
  moved to `test/data/.gitignore` (and modified to just `*.tmp`) if such a file
  exists.

To use the hook, add the following to `.pre-commit-hooks.yaml`:

```
repos:
  - repo: https://github.com/assorted-pre-commit-hooks/gitignore
    rev: # see repository for latest tag
    hooks:
      - id: gitignore
```

[pre-commit]:   https://pre-commit.com/
[Git]:          https://git-scm.com/
[ignore]:       https://git-scm.com/docs/gitignore
