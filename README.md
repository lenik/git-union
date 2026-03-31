# git-union

**git-union** merges multiple git repositories into a **single monorepo**.
Each source repository is placed into a subdirectory, while preserving commit
history by replaying commits into a new repository.

Good for:

- migrating multi-repo projects into a monorepo
- consolidating historical projects
- cleaning up a collection of related repositories

## Features

- Accepts repository arguments as:
  - `repo_path` (subdirectory is the repository basename)
  - `name=repo_path` (subdirectory uses explicit `name`)
- Creates a fresh repository at `MONO-DIR` (`MONO-DIR/.git`).
- Replays commits while preserving, per commit:
  - commit message
  - author/committer name and email
  - author/committer timestamps
- Optional `--sort` mode to interleave commits by author time while preserving
  commit order inside each source repository.

## Installation

This repository currently provides a standalone executable script `git-union`.

- From the repo:

```bash
chmod +x ./git-union
sudo install -m 0755 ./git-union /usr/local/bin/git-union
```

- With Debian packaging:

```bash
dpkg-buildpackage -us -uc
sudo dpkg -i ../git-union_*.deb
```

## Usage

```bash
git-union [OPTIONS] MONO-DIR REPOS...
```

### Arguments

#### `MONO-DIR`

The output directory to create. It **must not already exist**.

After running, it becomes a new git repository:

```text
MONO-DIR/.git
```

#### `REPOS...`

Each repo can be provided as:

- `repo_path` (subdir is basename, e.g. `foo/`)
- `name=repo_path` (subdir is explicit `name/`)

### Options

- `-s`, `--sort` sort by author time with per-repo order preserved
- `-v`, `--verbose` verbose output
- `-q`, `--quiet` minimal output
- `-h`, `--help` help
- `--version` print version

## Examples

Assume:

```text
foo/.git
bar/.git
```

```bash
git-union monodir foo bar
```

This creates:

```text
monodir/
  .git/
  foo/
  bar/
```

## Commit order in `--sort`

`--sort` interleaves commits from multiple repos by **author time**, while
preserving commit order inside each repo.

Given:

```text
repo1: 10 21 45 33 51
repo2:  8 13 31 49
```

Valid outputs include:

```text
mono: 8 10 13 21 31 45 33 49 51   (preferred)
mono: 8 10 13 21 31 45 49 33 51   (also valid)
```

The “wrong” local order `45 -> 33` is preserved because both commits come from
the same source repo. Due to this constraint, multiple valid solutions may
exist; `git-union` tries to pick a result that looks “more sorted”.

## Design goals

- **Simple**: focused on monorepo merge via history replay
- **History preserving**: keep authorship, timestamps, and messages
- **Readable history**: optional cross-repo time interleaving (`--sort`)

## Limitations and notes

- The output is a **linear history** (a single replay stream), not a faithful
  reproduction of original branch topology/merge commits.
- Paths are always rewritten under the chosen repo subdirectory, so filename
  collisions across repos are avoided by construction.
- This tool assumes each input repo has a reachable `HEAD`.

## Tests

Run automated tests:

```bash
python3 -m unittest -v
```

The suite creates temporary git repositories and verifies:

- basic union flow and output layout
- explicit `name=repo_path` mapping behavior
- `--sort` ordering constraints (cross-repo interleave with per-repo order preserved)

Quick manual checks:

```bash
./git-union --help
./git-union --version
```

## License (2026)

Copyright (C) 2026 Lenik (`git-union@bodz.net`)

Licensed under the **GNU Affero General Public License**, version 3 or later
(**AGPL-3.0-or-later**). See `LICENSE`.

### Anti-AI statement (policy)

As an additional **non-binding** project policy statement: the author requests
that this project not be used to train or evaluate machine-learning models
without explicit prior permission. This statement is not intended to add legal
restrictions beyond the AGPL license terms.
