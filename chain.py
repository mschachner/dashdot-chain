"""Chain rewriting utility for dash-dot syntax.

Chains are sequences consisting of digits, centered bullets ("\u2022"), and
dashes.  The :func:`rewrite_step` function applies one rewrite rule at a time
using the following patterns (where ``n`` and ``m`` denote digits)::

    1. ``•0•m`` → ``•(m+1)``
    2. ``-0•`` → ``•``
    3. ``•0-…-0-(k+1)-v•n`` → ``•n-…-n-k-v•n``
    4. ``•(k+1)-v•n`` → ``n`` copies of ``•k-v`` followed by ``•n``

Several runner functions demonstrate different execution modes, including
"abridged" modes that skip repetitive expansions.
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple


@dataclass
class RewriteMatch:
    """Representation of a single rule match."""

    start: int
    rule_id: int
    tokens: List[str]


# Normalize input to use centered bullets
def _normalize(chain: str) -> str:
    """Replace ASCII dots with the centered bullet character."""
    return chain.replace('.', '•')


# Tokenization helpers
def _tokenize(chain: str) -> List[str]:
    """Split a chain into digits, bullet symbols, and dashes."""
    return re.findall(r"\d+|[•-]", chain)


def _detokenize(tokens: List[str]) -> str:
    """Convert a token list back into a chain string."""
    return ''.join(tokens)


def _rule1(tokens: List[str]) -> List[RewriteMatch]:
    """Match Rule 1: ``•0•m → •(m+1)``."""
    n = len(tokens)
    matches: List[RewriteMatch] = []
    for i in range(n - 3):
        if (
            tokens[i] == '•'
            and tokens[i + 1] == '0'
            and tokens[i + 2] == '•'
            and tokens[i + 3].isdigit()
        ):
            m_val = int(tokens[i + 3])
            new = tokens[:i] + ['•', str(m_val + 1)] + tokens[i + 4:]
            matches.append(RewriteMatch(i, 1, new))
    return matches


def _rule2(tokens: List[str]) -> List[RewriteMatch]:
    """Match Rule 2: ``-0• → •``."""
    n = len(tokens)
    matches: List[RewriteMatch] = []
    for i in range(n - 2):
        if tokens[i] == '-' and tokens[i + 1] == '0' and tokens[i + 2] == '•':
            new = tokens[:i] + ['•'] + tokens[i + 3:]
            matches.append(RewriteMatch(i, 2, new))
    return matches


def _rule3(tokens: List[str]) -> List[RewriteMatch]:
    """Match Rule 3 as described in the module summary."""
    n = len(tokens)
    matches: List[RewriteMatch] = []
    for i in range(n):
        if tokens[i] != '•':
            continue
        for j in range(i + 1, n):
            if tokens[j] != '•':
                continue
            inner = tokens[i + 1 : j]
            if len(inner) < 3:
                continue
            zeros = 0
            idx_inner = 0
            while (
                idx_inner + 1 < len(inner)
                and inner[idx_inner] == '0'
                and inner[idx_inner + 1] == '-'
            ):
                zeros += 1
                idx_inner += 2
            if zeros == 0:
                continue
            if idx_inner >= len(inner) or not inner[idx_inner].isdigit():
                continue
            kp1 = int(inner[idx_inner])
            k = kp1 - 1
            if j + 1 >= n or not tokens[j + 1].isdigit():
                continue
            n_val = int(tokens[j + 1])
            v_tokens = inner[idx_inner + 1 :]
            valid_v = True
            for t in range(0, len(v_tokens), 2):
                if not (
                    v_tokens[t] == '-' and t + 1 < len(v_tokens) and v_tokens[t + 1].isdigit()
                ):
                    valid_v = False
                    break
            if not valid_v:
                continue
            prefix = ['•', str(n_val)]
            for _ in range(zeros - 1):
                prefix += ['-', str(n_val)]
            prefix += ['-', str(k)]
            new = tokens[:i] + prefix + v_tokens + ['•', str(n_val)] + tokens[j + 2 :]
            matches.append(RewriteMatch(i, 3, new))
    return matches


def _rule4(tokens: List[str]) -> List[RewriteMatch]:
    """Match Rule 4 as described in the module summary."""
    n = len(tokens)
    matches: List[RewriteMatch] = []
    for i in range(n - 2):
        if tokens[i] == '•' and tokens[i + 1].isdigit():
            k = int(tokens[i + 1]) - 1
            j = i + 2
            v_tokens: List[str] = []
            while j + 1 < n and tokens[j] == '-' and tokens[j + 1].isdigit():
                v_tokens += [tokens[j], tokens[j + 1]]
                j += 2
            if j < n and tokens[j] == '•' and tokens[j + 1].isdigit():
                n_copies = int(tokens[j + 1])
                rep: List[str] = []
                for _ in range(n_copies):
                    rep += ['•', str(k)] + v_tokens
                new = tokens[:i] + rep + ['•', str(n_copies)] + tokens[j + 2 :]
                matches.append(RewriteMatch(i, 4, new))
    return matches


# Core rewrite function: smallest-suffix priority
def rewrite_step(chain: str) -> Optional[str]:
    """Return the next chain after applying one rewrite rule, if any."""
    tokens = _tokenize(chain)
    matches: List[RewriteMatch] = []
    matches.extend(_rule1(tokens))
    matches.extend(_rule2(tokens))
    matches.extend(_rule3(tokens))
    matches.extend(_rule4(tokens))

    if not matches:
        return None

    max_i = max(m.start for m in matches)
    candidates = [m for m in matches if m.start == max_i]
    candidates.sort(key=lambda m: m.rule_id)
    return _detokenize(candidates[0].tokens)

# Standard runners
def run_verbose(chain: str) -> None:
    """Print each intermediate chain produced during rewriting."""

    cur = chain
    print(cur)
    steps = 0
    while True:
        nxt = rewrite_step(cur)
        if nxt is None:
            break
        print(nxt)
        steps += 1
        cur = nxt
    print(f"Total steps: {steps}")

def run_last(chain: str) -> None:
    """Run until no rule applies and print only the final chain."""

    cur = chain
    steps = 0
    while True:
        nxt = rewrite_step(cur)
        if nxt is None:
            print(cur)
            print(f"Total steps: {steps}")
            return
        steps += 1
        cur = nxt

def run_interactive(chain: str) -> None:
    """Like :func:`run_verbose` but waits for input between steps."""

    cur = chain
    print(cur)
    steps = 0
    while True:
        nxt = rewrite_step(cur)
        if nxt is None:
            break
        input()
        print(nxt)
        steps += 1
        cur = nxt
    print(f"Total steps: {steps}")


# Abridged runners with streaming omissions and memoization
def run_abridged(chain: str) -> None:
    """Run with heuristics to omit large expansions while streaming output."""

    cur = chain
    print(cur)
    steps = 0
    local_cache: Dict[str, Tuple[str, int]] = {}
    while True:
        old = cur
        tokens = _tokenize(cur)
        # trailing zeros
        m = 0
        idx = len(tokens) - 2
        while idx-1 >= 0 and tokens[idx-1] == '0' and tokens[idx-2] == '•':
            m += 1
            idx -= 2
        if m >= 5 and idx >= 0 and tokens[idx] == '•' and tokens[-1].isdigit():
            n_val = int(tokens[-1])
            new_chain = ''.join(tokens[:idx] + ['•', str(n_val + m)])
            local_cache[old] = (new_chain, m)
            print(f"({m} lines omitted)")
            print(new_chain)
            steps += m
            cur = new_chain
            continue
        # suffix •1•n skip
        if (len(tokens) >= 4 and tokens[-4] == '•' and tokens[-3] == '1' and
                tokens[-2] == '•' and tokens[-1].isdigit()):
            n_val = int(tokens[-1])
            skip = n_val + 1
            if skip >= 5:
                new_chain = ''.join(tokens[:-4] + ['•', str(2 * n_val)])
                local_cache[old] = (new_chain, skip)
                print(f"({skip} lines omitted)")
                print(new_chain)
                steps += skip
                cur = new_chain
                continue
        # suffix •2•n skip (n*2^n + 1)
        if (len(tokens) >= 4 and tokens[-4] == '•' and tokens[-3] == '2' and
                tokens[-2] == '•' and tokens[-1].isdigit()):
            n_val = int(tokens[-1])
            skip = n_val * (2 ** n_val) + 1
            if skip >= 5:
                result_val = n_val * (2 ** n_val)
                new_chain = ''.join(tokens[:-4] + ['•', str(result_val)])
                local_cache[old] = (new_chain, skip)
                print(f"({skip} lines omitted)")
                print(new_chain)
                steps += skip
                cur = new_chain
                continue
        # previously cached
        if cur in local_cache:
            new_chain, skip = local_cache[cur]
            print(f"({skip} lines omitted)")
            print(new_chain)
            steps += skip
            cur = new_chain
            continue
        # normal step
        nxt = rewrite_step(cur)
        if nxt is None:
            break
        local_cache[old] = (nxt, 1)
        print(nxt)
        steps += 1
        cur = nxt
    print(f"Total steps: {steps}")


def interactive_abridged(chain: str) -> None:
    """Interactive variant of :func:`run_abridged`."""

    cur = chain
    print(cur)
    steps = 0
    local_cache: Dict[str, Tuple[str, int]] = {}
    while True:
        old = cur
        tokens = _tokenize(cur)
        # trailing zeros
        m = 0
        idx = len(tokens) - 2
        while idx-1 >= 0 and tokens[idx-1] == '0' and tokens[idx-2] == '•':
            m += 1
            idx -= 2
        if m >= 5 and idx >= 0 and tokens[idx] == '•' and tokens[-1].isdigit():
            n_val = int(tokens[-1])
            new_chain = ''.join(tokens[:idx] + ['•', str(n_val + m)])
            local_cache[old] = (new_chain, m)
            print(f"({m} lines omitted)")
            print(new_chain)
            steps += m
            cur = new_chain
            continue
        # suffix •1•n
        if (len(tokens) >= 4 and tokens[-4] == '•' and tokens[-3] == '1' and
                tokens[-2] == '•' and tokens[-1].isdigit()):
            n_val = int(tokens[-1])
            skip = n_val + 1
            if skip >= 5:
                new_chain = ''.join(tokens[:-4] + ['•', str(2 * n_val)])
                local_cache[old] = (new_chain, skip)
                print(f"({skip} lines omitted)")
                print(new_chain)
                steps += skip
                cur = new_chain
                continue
        # suffix •2•n
        if (len(tokens) >= 4 and tokens[-4] == '•' and tokens[-3] == '2' and
                tokens[-2] == '•' and tokens[-1].isdigit()):
            n_val = int(tokens[-1])
            skip = n_val * (2 ** n_val) + 1
            if skip >= 5:
                result_val = n_val * (2 ** n_val)
                new_chain = ''.join(tokens[:-4] + ['•', str(result_val)])
                local_cache[old] = (new_chain, skip)
                print(f"({skip} lines omitted)")
                print(new_chain)
                steps += skip
                cur = new_chain
                continue
        # cached
        if cur in local_cache:
            new_chain, skip = local_cache[cur]
            print(f"({skip} lines omitted)")
            print(new_chain)
            steps += skip
            cur = new_chain
            continue
        # normal step
        nxt = rewrite_step(cur)
        if nxt is None:
            break
        input()
        print(nxt)
        steps += 1
        cur = nxt
    print(f"Total steps: {steps}")

# CLI interface
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3 or sys.argv[1] not in (
            'step', 'run', 'interactive', 'last',
            'run_abridged', 'interactive_abridged'):
        print(
            "Usage: python chain.py"
            " [step|run|interactive|last|run_abridged|interactive_abridged] '<chain>'"
        )
        sys.exit(1)
    mode, raw = sys.argv[1], sys.argv[2]
    chain = _normalize(raw)
    if mode == 'step':
        out = rewrite_step(chain)
        print(out if out else "(no rule applies)")
    elif mode == 'run':
        run_verbose(chain)
    elif mode == 'interactive':
        run_interactive(chain)
    elif mode == 'last':
        run_last(chain)
    elif mode == 'run_abridged':
        run_abridged(chain)
    else:
        interactive_abridged(chain)

