#!/usr/bin/env python3
"""Small deterministic forecast math helpers for Hermes prediction work."""

from __future__ import annotations

import argparse
import json
import math
from typing import Iterable

EPS = 1e-12


def parse_prob(raw: str | float) -> float:
    if isinstance(raw, float):
        p = raw
    else:
        s = str(raw).strip()
        if s.endswith("%"):
            p = float(s[:-1]) / 100.0
        else:
            p = float(s)
            if p > 1 and p <= 100:
                p /= 100.0
    if not 0 <= p <= 1:
        raise argparse.ArgumentTypeError(f"probability must be in [0,1] or percent, got {raw!r}")
    return p


def clamp_for_log(p: float) -> float:
    return min(max(p, EPS), 1 - EPS)


def odds(p: float) -> float:
    p = min(max(p, EPS), 1 - EPS)
    return p / (1 - p)


def probability_from_odds(o: float) -> float:
    return o / (1 + o)


def emit(data: dict) -> int:
    print(json.dumps(data, indent=2, sort_keys=True))
    return 0


def cmd_beta_prior(args: argparse.Namespace) -> int:
    if args.n < 0 or args.k < 0 or args.k > args.n:
        raise SystemExit("Require 0 <= k <= n")
    p = (args.k + args.alpha) / (args.n + args.alpha + args.beta)
    return emit({"method": "beta_prior", "k": args.k, "n": args.n, "alpha": args.alpha, "beta": args.beta, "p": p, "odds": odds(p)})


def cmd_bayes(args: argparse.Namespace) -> int:
    prior = parse_prob(args.prior)
    post_odds = odds(prior)
    lrs = [float(x) for x in args.lr]
    for lr in lrs:
        if lr <= 0:
            raise SystemExit("Likelihood ratios must be positive")
        post_odds *= lr
    posterior = probability_from_odds(post_odds)
    return emit({"method": "bayes_lr", "prior": prior, "prior_odds": odds(prior), "likelihood_ratios": lrs, "posterior_odds": post_odds, "posterior": posterior})


def cmd_normalize(args: argparse.Namespace) -> int:
    weights = [float(x) for x in args.weights]
    if not weights or any(w < 0 for w in weights):
        raise SystemExit("Weights must be nonnegative and nonempty")
    total = sum(weights)
    if total <= 0:
        raise SystemExit("At least one weight must be positive")
    probs = [w / total for w in weights]
    labels = args.labels or [f"scenario_{i+1}" for i in range(len(probs))]
    if len(labels) != len(probs):
        raise SystemExit("--labels length must match --weights length")
    return emit({"method": "normalize", "items": [{"label": label, "weight": w, "probability": p} for label, w, p in zip(labels, weights, probs)], "sum": sum(probs)})


def cmd_delta(args: argparse.Namespace) -> int:
    forecast = parse_prob(args.forecast)
    market = parse_prob(args.market)
    delta = forecast - market
    return emit({"method": "market_delta", "forecast": forecast, "market": market, "delta": delta, "absolute_delta": abs(delta), "direction": "above_market" if delta > 0 else "below_market" if delta < 0 else "equal"})


def cmd_brier(args: argparse.Namespace) -> int:
    p = parse_prob(args.p)
    outcome = int(args.outcome)
    if outcome not in (0, 1):
        raise SystemExit("Outcome must be 0 or 1")
    score = (p - outcome) ** 2
    return emit({"method": "brier", "p": p, "outcome": outcome, "score": score})


def cmd_log_score(args: argparse.Namespace) -> int:
    p = clamp_for_log(parse_prob(args.p))
    outcome = int(args.outcome)
    if outcome not in (0, 1):
        raise SystemExit("Outcome must be 0 or 1")
    score = -math.log(p if outcome else 1 - p)
    return emit({"method": "log_score", "p": p, "outcome": outcome, "score": score, "natural_log": True})


def main() -> int:
    parser = argparse.ArgumentParser(description="Forecast math helpers: priors, Bayesian LR updates, normalization, deltas, and scores")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("beta-prior", help="Smoothed base rate (k + alpha) / (n + alpha + beta)")
    p.add_argument("--k", type=float, required=True, help="Observed successes")
    p.add_argument("--n", type=float, required=True, help="Observed cases")
    p.add_argument("--alpha", type=float, default=1.0)
    p.add_argument("--beta", type=float, default=1.0)
    p.set_defaults(func=cmd_beta_prior)

    p = sub.add_parser("bayes", help="Apply likelihood ratios to a prior probability")
    p.add_argument("--prior", required=True, help="Prior probability 0-1 or percent")
    p.add_argument("--lr", action="append", required=True, help="Likelihood ratio; repeat for multiple evidence items")
    p.set_defaults(func=cmd_bayes)

    p = sub.add_parser("normalize", help="Normalize mutually exclusive scenario weights")
    p.add_argument("--weights", nargs="+", required=True)
    p.add_argument("--labels", nargs="*", default=None)
    p.set_defaults(func=cmd_normalize)

    p = sub.add_parser("delta", help="Compare forecast probability to market probability")
    p.add_argument("--forecast", required=True)
    p.add_argument("--market", required=True)
    p.set_defaults(func=cmd_delta)

    p = sub.add_parser("brier", help="Binary Brier score")
    p.add_argument("--p", required=True)
    p.add_argument("--outcome", required=True)
    p.set_defaults(func=cmd_brier)

    p = sub.add_parser("log-score", help="Binary negative log score, natural log")
    p.add_argument("--p", required=True)
    p.add_argument("--outcome", required=True)
    p.set_defaults(func=cmd_log_score)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
