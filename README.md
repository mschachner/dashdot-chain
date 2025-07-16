# Dash-Dot Chain Rewriter

This repository contains a small utility for rewriting *dash‑dot* chains. A
chain is a sequence of digits, centred bullet characters (`•`) and dashes
(`-`). The `chain.py` module provides a set of rewrite rules and a number of
runners that demonstrate different ways to apply them.

## Usage

The module can be executed directly with a mode and an initial chain:

```bash
python chain.py run '•0-0-3-5•2'
```

Available modes are:

- `step` – apply a single rewrite step
- `run` – display every intermediate chain
- `interactive` – as above but waits for Enter between steps
- `last` – only print the final chain
- `run_abridged` – omit large expansions while streaming output
- `interactive_abridged` – interactive variant of the abridged runner

If the script is run without arguments it will prompt for the desired runner
and the starting chain interactively.

## Development

Run the unit tests with:

```bash
pytest
```

The tests cover the core rewrite logic.
