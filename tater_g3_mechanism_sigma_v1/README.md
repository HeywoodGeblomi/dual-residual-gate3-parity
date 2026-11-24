# Tater track: Gate 3 mechanism and σ_Δ notes

Author: Heywood Geblomi. Status: exploratory. Not a claim that the Dual Residual core works.

The Dual Residual core at commit `ba2ea57` ([HeywoodGeblomi/dual-residual](https://github.com/HeywoodGeblomi/dual-residual), `dual_residual.hpp`) failed Gate 3. Gate 3 asks for stability under a one-sample shift. All of the work in this folder uses DS1 only. DS1 is MIT-BIH Arrhythmia from PhysioNet, MLII lead, with `dataset_v1` labels. DS2 is sealed and was never opened. Raw MIT-BIH records are not in this folder.

Absolute paths inside the files (`/workspace/...`) refer to the machine where the work was produced. They are left unchanged so the hashes stay valid.

## Why ba2ea57 flips

`G3_MECHANISM_v1.md`, `probe.cpp`, and `probe_out.txt` explain the flip.

`detail::compute` takes events as the sign crossings of `stream > 0`. Those crossings alternate up and down. It keeps `events[0::2]`, which all go one direction, then splits them even and odd again. So σ_Δ is exactly 0 whenever the window's first sign is ≤ 0, and the core returns None. Otherwise σ_Δ is a tie-share difference between alternating down-crossings. The decision is gated by the window's first step.

That accounts for the one-sample-shift flip rates on DS1: 33.1% at N=1024 and 28.4% at N=4096.

## σ_Δ-only variants

`sigma_tinker_v1/` holds six σ_Δ-only variants tried on DS1 (T1v01–T1v06). Every try is logged in `sigma_tinker_v1/VARIANTS_LOG.md`. The table is in `sigma_tinker_v1/SUMMARY.md` and `sigma_tinker_v1/table.md`. Per-try scores are in `sigma_tinker_v1/results/`. The four constants (0.04 / 0.005 / 0.1 / 0.2) and the decision table are unchanged.

All six fail at least one bar. All flip at most 3.1% at N=1024, and 20–50% at N=4096, because of the stride-8 decimation at N=4096. The closest, T1v06 (plateau parity), passes every bar at N=1024 only. T1v00 is the unmodified core, reproduced as a harness check.

## Core v2 preregistration

`core_v2_prereg_tater_v1/` holds a preregistration for four candidates that change both the sampling and σ_Δ: lag-not-decimate and block-mean decimation, each paired with T1v05 or T1v06. See `core_v2_prereg_tater_v1/PREREG.md`.

It was written about 00:14 ET on 2026-11-24 (the header in `PREREG.md` says ~00:15 ET), before any DS1 run. `PREREG.md` sha256 is `26953107f6caae4c26506f9637ac8a2a0c15696534aa3abe92a021a533647fdb`, recorded in `core_v2_prereg_tater_v1/PREREG.sha`. Errata 1 (`core_v2_prereg_tater_v1/PREREG_ERRATA_1.md`) was also written before any DS1 run. Results are pending. Across all tracks, at most one frozen candidate gets a single DS2 shot.

## Python port

`bridge_v1/variants.py` is a bit-exact Python port of the ba2ea57 core. The same folder holds a synthetic comparison against a clean-room reference (`run_bridge.py`, `core_cli.cpp`, `bridge_results_v1.json`). Hashes for those files are in `bridge_v1/BRIDGE_v1.sha256`.

## Check the record

`README.md` is not in the manifest. From this folder:

```
sha256sum -c MANIFEST.sha256
```
