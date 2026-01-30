# Benchmarking principles (R)

Sources
- https://stat.ethz.ch/R-manual/R-devel/library/base/html/system.time.html
- https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Rprof.html
- https://bench.r-lib.org/

Core principles
- Separate macro timing (system.time/proc.time) from microbenchmarks (bench/microbenchmark).
- Run multiple iterations; avoid single-shot timings.
- Control randomness (set.seed) and input sizes; avoid I/O and network.
- Warm up once to reduce JIT/dispatch and cache effects when relevant.
- Report both time and allocation pressure when allocations or GC may dominate.

Sampling profiler caveats
- Smaller intervals perturb results; do not use overly small Rprof intervals.
- CPU vs elapsed: use cpu to isolate compute bottlenecks; elapsed includes waiting time.

Reproducibility checklist
- Record platform details (R version, OS, CPU), and key package versions.
- Keep the same inputs across alternatives; verify result equivalence.
- Prefer relative comparisons with confidence intervals or distributions over single values.
