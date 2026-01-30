# bench package

Sources
- https://bench.r-lib.org/
- https://bench.r-lib.org/reference/mark.html

Purpose
- High precision timing with memory allocation and GC tracking.
- Uses adaptive stopping by default (min_time) and filters GC-heavy iterations.

bench::mark
- Usage: mark(..., min_time = 0.5, iterations = NULL, min_iterations = 1, max_iterations = 10000, check = TRUE, memory = capabilities("profmem"), filter_gc = TRUE, relative = FALSE, time_unit = NULL)
- check = TRUE verifies equivalent results via all.equal; can pass a custom function or FALSE to skip checks.
- memory = TRUE tracks allocations via utils::Rprofmem().
- filter_gc removes iterations with GC unless every iteration GC's.
- Returns a tibble with summary columns: min, median, itr/sec, mem_alloc, gc/sec, n_itr, n_gc, total_time, result, memory, time, gc.

bench::press
- Purpose: run a benchmark grid over multiple parameter values; combines results.
- Structure: press(param1 = ..., param2 = ..., { setup; mark(...) })

When to choose
- Preferred for microbenchmarks where memory and GC behavior matter.
- Use relative = TRUE for ratios; keep time_unit = NULL for human-readable output.
