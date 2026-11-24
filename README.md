# dual-residual-gate3-parity

Author: Heywood Geblomi. Public snapshot built 24 November 2026.

## What this is

Lucas Job 3 work on Dual Residual phase stability and a later exploratory gate-3 fix attempt, plus a synthetic edge comparison of the frozen core against a clean-room reference.

The Dual Residual core itself is not in this repo. It is already public, frozen at commit `ba2ea57`, in [HeywoodGeblomi/dual-residual](https://github.com/HeywoodGeblomi/dual-residual). `core_sha_before.txt` records `dual_residual.hpp` sha256 `64fa3ca2da1655301ab64e4be704bbf34d975b8d690962d8fba93258b6d01ecf` before these runs. Constants were not changed.

Data for the DS1 scores is Purp `dataset_v0` / `dataset_v1` DS1 only (MIT-BIH MLII raw 11-bit integers). DS2 was not read and is not here.

## Recorded results

Official Job 3 DS1 score (`ds1/`, prereg hashed in `ds1/PREREG.sha`, scored once):

- P1 phase stability (flip rate, window vs window shifted by one sample, bar <= 10% at both N): 33.1% at N=1024 and 28.4% at N=4096. MISS.
- P2 mechanism: |sigma_delta| higher on labeled V windows than on None windows, one-sided Mann-Whitney p < 0.01 at both N, and ownership on V windows at least 10 points above a within-window shuffle (seed 7) at both N. Recorded p-values are 0.81 and 0.098. Ownership lifts are about 9.9 points and 10.4 points. P2 MISS.

An earlier exploratory DS1 pass is in `ds1_v1_exploratory/`. It is not the official score.

Gate-3 fix attempt v1 (`gate3_fix_v1/`) was preregistered as exploratory: DS1 had already been used, so no result here can pass the gate. Recorded once:

- Candidate A (PhaseLock majority over offsets, core unchanged): P1 MISS at both N (flip 12.8% and 10.9%).
- Candidate B (a clean-room reference, unmodified): P1 HIT at both N, P2 MISS at both N.

Synthetic edge comparison (`g4_edge/`, seed 20261124, no DS1 or DS2): 639 of 1400 decisions agreed between core `ba2ea57` and a frozen clean-room reference, across five synthetic window kinds and seven lengths. Agreement was 280/280 on strictly monotone no-tie windows, and much lower on tie-heavy windows (7/280). See `g4_edge/edge_results.json`.

## How to check it

The run scripts (`ds1/run.py`, `gate3_fix_v1/run.py`, `g4_edge/edge_diff.py`) were written against local paths and a compiled `libdr.so`. Those binaries and the dataset are not in this repo. To replay, build the public core at `ba2ea57`, point the scripts at a local copy of the DS1 tables, and compare against the checked-in `results.json` files.

```
sha256sum -c ds1/PREREG.sha
sha256sum -c gate3_fix_v1/PREREG.sha
```

## Files left out of this copy

- `core/`: checkout of already-public dual-residual at `ba2ea57`. Use the public repo instead.
- `.venv/`: Python virtualenv, stripped.
- Compiled binaries, not included (binary): `bin/test_*`, `ds1/libdr.so`, `perturb/peek`, `perturb/perturb`.
- Source for the small C++ helpers `perturb/peek.cpp` and `perturb/perturb.cpp` is included.
