# Free educational example: how to verify a coding agent's work

This is a **synthetic demonstration** of a simple review method anyone can perform with free tools. It is **not** the Agent Mission Guard product, SDK, installer, or output from a live customer. No external connections, credentials, private code, subscriptions, or downloads beyond this folder are needed.

The fictional mission in [mission.md](mission.md) is frozen before reviewing the four example scenarios. `baseline/` is the original toy website and `scenarios/` has four distinct *pre-created examples*.

## Reproduce the educational results

From this folder:

```sh
python3 replay.py
```

The read-only script uses Python standard library only. It prints file differences and applies exactly four toy static checks. These are the outputs independently reproduced locally before this package was prepared:

| Synthetic fixture | Scope | Declared evidence |
| --- | --- | --- |
| `01-allowed` | PASS | 4/4 |
| `02-out-of-scope` | VIOLATION | 4/4 |
| `03-protected-change` | VIOLATION | 4/4 |
| `04-missing-acceptance` | PASS | 3/4 |

The script doesn't execute a coding agent, make API calls, certify website behavior, or run AMG. It has no network access in its code and never edits files.

To inspect the differences with your **existing free tools**, use for example:

```sh
# Plain diff: exit status 1 means differences were found
# (run from the public-demo directory)
diff -ru baseline scenarios/01-allowed

diff -ru baseline scenarios/04-missing-acceptance
```

Or initialize your own *disposable* Git repository with a copy of `baseline/` and run a normal `git diff` after applying one variant. Git's [official diff reference](https://git-scm.com/docs/git-diff) explains the distinction between comparing the worktree, index and commits.

**Why this lesson matters:** A tool or human can catch a missing CTA anchor with a simple explicit checklist. A second product earns a place only if it makes the process faster or more reliable than the actual existing baseline, without excessive false alarms. We are testing whether a guided local receipt does that. A passing static receipt does not prove a functioning browser experience.

### License and scope

The synthetic example files and educational replay script in this repository are MIT-licensed; see [LICENSE](LICENSE). This license **does not** apply to the separate Agent Mission Guard application, which is not included here. The demonstration is not an installer and does not verify the runtime behavior or security of any website.

### Relationship to Agent Mission Guard

This educational fixture illustrates a manual verification concept. Agent Mission Guard is a separate private prototype under evaluation; the fixture does **not** run the product or establish its accuracy, commercial readiness, customer demand, or supported integrations. There is currently no external download or signup link offered here.
