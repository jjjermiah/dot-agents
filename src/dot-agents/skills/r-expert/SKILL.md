---
name: r-expert
description: |
  Core R programming skill for all R code, package development, and data science workflows. Use when writing R functions, building packages, using tidyverse (dplyr, ggplot2, purrr), creating Shiny apps, working with R Markdown/Quarto, or doing data analysis—e.g., "write an R function", "refactor this R code", "create a Shiny dashboard", "set up package tests", "debug R errors".
---

# R Expert Skill

## Purpose

Provide production-grade R code, package development guidance, and data science workflows. Leverage Context7 for up-to-date package documentation and modern R best practices.

## Complementary Skills

Load additional skills when needed, in combination with r-expert:

- **r-testing** - When writing/fixing/reviewing R tests and test fixtures
- **r-benchmarking** - When measuring performance, timing, profiling, or memory allocation
- **r-error-handling** - When implementing structured error handling and custom conditions
- **r-rlang-programming** - When using metaprogramming, NSE, tidy evaluation, or rlang APIs

## Core Workflow

1. Identify the task type (data manipulation, visualization, package dev, etc.)
2. Use Context7 for package-specific APIs (see [references/r-context7-mappings.md](references/r-context7-mappings.md))
3. Apply modern tidyverse patterns
4. Ensure reproducibility and best practices

## Package Documentation

Use Context7 to get accurate, current documentation for R packages:

```
# Tidyverse core
/tidyverse/dplyr       # Data manipulation
/tidyverse/ggplot2     # Visualization  
/tidyverse/tidyr       # Data reshaping
/tidyverse/purrr       # Functional programming
/tidyverse/readr        # Data import

# Development
/r-lib/devtools         # Package development
/r-lib/usethis          # Project setup
/r-lib/testthat         # Testing

# See full list in references/r-context7-mappings.md
```

## Code Style

- Use `package::function()` for clarity
- Prefer tidyverse for data manipulation
- Snake_case for functions and variables
- Explicit returns only when early exit needed
- 80-100 character line limits

## Essential Patterns

### Data Pipeline

```r
data <- raw_data |>
  dplyr::filter(year >= 2020) |>
  dplyr::mutate(
    total = price * quantity,
    category = forcats::fct_lump(category, n = 5)
  ) |>
  dplyr::group_by(region) |>
  dplyr::summarise(
    revenue = sum(total, na.rm = TRUE),
    .groups = "drop"
  )
```

### Safe File Operations

```r
# Use withr for temporary state
withr::with_tempfile("tmp", {
  readr::write_csv(data, tmp)
  processed <- readr::read_csv(tmp, show_col_types = FALSE)
})
```

### Package Structure

```
my-package/
├── DESCRIPTION          # Package metadata
├── NAMESPACE           # Auto-generated exports
├── R/                  # Source code
│   ├── utils.R         # Internal helpers
│   └── main-feature.R  # Main functionality
├── tests/
│   └── testthat/       # Tests
├── man/                # Documentation (auto)
└── README.Rmd          # Package README
```

## References (Load on Demand)

- **[references/r-context7-mappings.md](references/r-context7-mappings.md)** - Load when querying Context7 for R package documentation; contains library ID mappings for tidyverse, Shiny, testing, ML, and database packages
