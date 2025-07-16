# Dash-Dot Chain Rewriter

This repository contains a small utility for rewriting *dash‑dot* chains. A
chain is a sequence of digits, centred bullet characters (`•`) and dashes
(`-`). The `chain.py` module provides a set of rewrite rules and a number of
runners that demonstrate different ways to apply them.

## Dash‑dot notation

The notation is designed for writing extremely large integers in a compact
form, in spirit similar to Knuth's up‑arrow or Conway's chained arrow
notation.  A chain is manipulated until no rewrite rule applies.  Every valid
chain eventually reduces to a single bullet followed by a number, e.g.
`•42`, where the resulting integer can be unimaginably large.

### Rewrite rules

The rewriting system repeatedly applies the following four rules, always
choosing the rightmost possible match.  Below ``n`` and ``m`` denote digits.

1. **Rule 1** – ``•0•m → •(m+1)``
   When ``0`` appears between two bullets, the value after the second bullet is
   increased by one.
2. **Rule 2** – ``-0• → •``
   A dash followed by ``0`` and a bullet collapses to just the bullet,
   effectively removing the ``0``.
3. **Rule 3** – ``•0-…-0-(k+1)-v•n → •n-…-n-k-v•n``
   One or more ``-0`` blocks directly after a bullet shift the trailing digit
   ``n`` leftwards over the zeros while decrementing the number ``k+1`` that
   follows them.
4. **Rule 4** – ``•(k+1)-v•n`` is replaced with ``n`` copies of ``•k-v``
   followed by ``•n``.  This duplicates a pattern ``n`` times and therefore
   creates extremely fast growth.

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
