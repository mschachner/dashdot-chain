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
choosing the rightmost possible match.  Below ``n`` and ``k`` denote numbers, while ``v``
denotes a _dash-chain_, i.e., a chain of numbers separated by dashes.

1. **Rule 1** – ``•0•n → •(n+1)``
   The string ``•0`` can be thought of as the successor function.
2. **Rule 2** – ``-0• → •``
   Any zeroes at the end of a dash-chain can be removed.
3. **Rule 3** – ``•0-…-0-(k+1)-v•n → •n-…-n-k-v•n``
    where the number of copies of $n$ is the same as the number of copies of 0 in the original chain. This is the _diagonal rule for dashes._
4. **Rule 4** – ``•(k+1)-v•n`` is replaced with ``n`` copies of ``•k-v``
   followed by ``•n``. The _diagonal rule for dots._

### Magnitude

Dash-dot chains model a sort of fast-growing hierarchy of functions. In particular:
- The chain ``•0•n`` reduces to ``•(n+1)``;
- The chain ``•1•n`` reduces to ``•2n``;
- The chain ``•2•n`` reduces to ``•(n*2^n)``;
- etc.

Even the small chain ``•3•3`` reduces to $\bullet 402653184 \times 2^{402653184}$, a number with over 120 million decimal digits.

Introducing dashes leads to even more rapid growth; the chain ``•0-1•n`` reduces by design to ``•n•n`` and thus has growth on the order of the Ackermann function.

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
