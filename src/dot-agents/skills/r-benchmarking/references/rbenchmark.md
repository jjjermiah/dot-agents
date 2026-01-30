# rbenchmark package

Source
- https://cran.r-project.org/package=rbenchmark

Purpose
- Wrapper around system.time that runs multiple expressions with controlled replications.
- Returns a data.frame of timings for each expression.

Notes
- Single function: benchmark().
- Useful for simple comparative timing when you do not need memory/GC metrics.
