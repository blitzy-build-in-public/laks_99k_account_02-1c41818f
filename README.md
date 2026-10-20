# Welcome to Blitzy

## What this repository contains

`hello_world.py` is a one-line program that prints one fixed line to stdout. `hello_world.txt` is a committed literal text file holding that same line 4000 times. The two artefacts are separate: `hello_world.py` never opens, reads or writes `hello_world.txt`.

## Exact invariants

| Artefact | Invariant |
| --- | --- |
| stdout of `python3 hello_world.py` | `Welcome to Blitzy` followed by one LF — 18 bytes, hex `57 65 6c 63 6f 6d 65 20 74 6f 20 42 6c 69 74 7a 79 0a`, exit status 0, nothing on stderr |
| `hello_world.py` | 1 line, 26 characters, 27 bytes — the single statement `print("Welcome to Blitzy")` |
| `hello_world.txt` | `Welcome to Blitzy` on 4000 LF-terminated lines, 72000 bytes, 1 distinct line value, no byte-order mark, no carriage return, no numbering, no padding, no trailing whitespace |

The output line, character for character — 17 characters, capital `W` and capital `B`, single spaces:

```
Welcome to Blitzy
```

## Requirements

* CPython 3.12 or later, with no upper bound. This checkout runs `/usr/bin/python3`, Python 3.13.7.
* Nothing to install. The program and the test module use the standard library alone, so the repository holds no manifest, no lockfile and no third-party dependency, and there is no build step.
* No network access is needed at build, test or run time.
* A POSIX host, with `git` and the POSIX text utilities (`wc`, `sort`, `grep`) for the checks below.

## Run

```sh
python3 hello_world.py
```

stdout is `Welcome to Blitzy` followed by exactly one newline and nothing else, stderr is empty, and the exit status is 0.

## Verify

Every command below is read-only with respect to the deliverable files: none of them writes, moves, truncates or reformats one. The single trace the table leaves in the working tree is the unittest row's: discovery imports `tests/test_hello_world.py`, so CPython may write an ignored `tests/__pycache__/` bytecode cache — `python3 -B` (or `PYTHONDONTWRITEBYTECODE=1`) suppresses even that. No tracked file is modified by any command below.

| Command | Expected result |
| --- | --- |
| `wc -l hello_world.txt` | `4000` |
| `wc -c hello_world.txt` | `72000` |
| `sort -u hello_world.txt \| wc -l` | `1` |
| `grep -c -x -F "Welcome to Blitzy" hello_world.txt` | `4000` |
| `wc -l hello_world.py` | `1` |
| `wc -c hello_world.py` | `27` |
| `python3 hello_world.py \| wc -c` | `18` |
| `python3 -m unittest discover -s tests -p "test_*.py"` | `Ran 2 tests ... OK` |
| `git cat-file blob HEAD:hello_world.txt \| wc -l` | `4000` — the committed bytes, not a checkout-converted working tree |
| `git ls-files` | `.gitignore`, `README.md`, `hello_world.py`, `hello_world.txt`, `tests/test_hello_world.py` — exactly these five paths, in this order, and nothing else |
| `grep -c -x -F -e "__pycache__/" -e "*.py[codz]" .gitignore` | `2` — the two hygiene patterns that keep interpreter caches out of the tracked set |
| `grep -o -e "python3 hello_world.py" -e 4000 -e 72000 README.md \| sort -u \| wc -l` | `3` — the bare digit strings `4000` and `72000` and the run command each appear in this README |

Three further whole-file checks: `head -3 hello_world.txt` and `tail -3 hello_world.txt` must each print three lines reading `Welcome to Blitzy` with no number, tab, quote, indent or trailing space; `grep -c $'\r' hello_world.txt` must print `0` (grep exits 1 when nothing matches, which is the expected outcome here); and `head -c 3 hello_world.txt` must not be a byte-order-mark sequence.

## No generation step exists for `hello_world.txt`

The 4000 lines are literal committed content in the file itself. No script, program, task, build step, install hook, git hook, test or dependency produces them, and the body is not derived by iteration, command substitution, shell expansion or template rendering. `hello_world.py` never opens or writes the file, and `tests/test_hello_world.py` only reads it — no check rewrites the file it inspects.

## Layout

```
.
├── hello_world.py
├── hello_world.txt
├── tests/
│   └── test_hello_world.py
├── README.md
└── .gitignore
```

`tests/` holds only `tests/test_hello_world.py` and needs no `__init__.py`, because the discovery start directory is also the top level; the only thing a run adds there is the ignored `tests/__pycache__/` bytecode cache the Verify section names.
