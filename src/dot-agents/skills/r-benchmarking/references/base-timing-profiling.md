# Base timing and profiling (R)

Sources
- https://stat.ethz.ch/R-manual/R-devel/library/base/html/system.time.html
- https://stat.ethz.ch/R-manual/R-devel/library/base/html/proc.time.html
- https://stat.ethz.ch/R-manual/R-devel/library/utils/html/Rprof.html
- https://stat.ethz.ch/R-manual/R-devel/library/utils/html/summaryRprof.html

system.time
- Purpose: return CPU and elapsed time used by an expression.
- Usage: system.time(expr, gcFirst = TRUE)
- Notes: calls proc.time before/after; gcFirst can reduce variability by running gc() first.

proc.time
- Purpose: total user/system CPU time and elapsed time since process start.
- Returns class "proc_time" with user, system, and elapsed components (print shows 3 values).
- Can time code by taking a difference between two proc.time calls.

Rprof
- Purpose: sampling profiler; writes stack traces at a fixed interval.
- Key args: filename, interval (seconds), memory.profiling, gc.profiling, line.profiling, event = "cpu" or "elapsed".
- Notes: interval has lower bounds (typically >= 10ms on Linux, >= 1ms elsewhere). CPU vs elapsed differ; cpu is preferred for bottlenecks on Unix.

summaryRprof
- Purpose: summarize Rprof output (timings, and optionally memory and line profiling).
- Key args: memory = c("none", "both", "tseries", "stats"), lines = c("hide", "show", "both"), chunksize.
- Returns by.self and by.total timing tables; can include memory summaries if enabled.

Practical defaults
- Macro timing: system.time() for coarse end-to-end cost.
- Deep profiling: Rprof(..., interval = 0.01, event = "cpu") then summaryRprof().
- Memory profiling: Rprof(memory.profiling = TRUE) or bench::mark memory tracking.
