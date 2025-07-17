# Dash-Dot Chain Rewriter

This repository contains a small utility for rewriting *dash‑dot* chains. A
chain is a sequence of digits, centred bullet characters (`•`) and dashes
(`-`). The `chain.py` module provides a set of rewrite rules and a number of
runners that apply them.

## Dash‑dot notation

The notation is designed for writing extremely large integers.
A chain is manipulated until no rewrite rule applies.  Every valid
chain eventually reduces to a single bullet followed by a number, e.g.
`•42`.

### Rewrite rules

The rewriting system repeatedly applies the following four rules, always
choosing the rightmost possible match.  Below ``n`` and ``m`` denote digits, while ``v``
denotes a _dash-chain_, i.e., a chain of digits separated by dashes.

1. **Rule 1** – ``•0•m → •(m+1)``
   The string ``•0`` can be thought of as the successor function.
2. **Rule 2** – ``-0• → •``
   Any zeroes at the end of a dash-only chain can be removed.
3. **Rule 3** – ``•0-…-0-(k+1)-v•n → •n-…-n-k-v•n``
   The _diagonal rule for dashes._
4. **Rule 4** – ``•(k+1)-v•n`` is replaced with ``n`` copies of ``•k-v``
   followed by ``•n``. The _diagonal rule for dots._

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
