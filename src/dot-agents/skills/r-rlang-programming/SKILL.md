---
name: r-rlang-programming
description: rlang metaprogramming for tidy evaluation and non-standard evaluation (NSE) in R. Use when building data-masking APIs, wrapping dplyr/ggplot2/tidyr functions with {{ !! !!! operators, implementing quosures and dynamic dots, or designing tidyverse-style DSLs—e.g., "tidy eval wrapper function", "embrace operator usage", "NSE programming patterns", "custom select helpers".
---

# rlang Programming Skill

## Purpose

Provide production-grade rlang metaprogramming guidance for R packages and functions that manipulate code, names, environments, conditions, or evaluation.

**Before proceeding:** Announce which rlang concepts you're using: "I'm using rlang for [tidy eval / error handling / code construction / environments]". This maintains clarity as we work through metaprogramming together.

## Core Concepts

### 1. Defusal and Injection

Code is data. Defuse (capture) it, manipulate it, inject (insert) it elsewhere. **You MUST understand defusal before using tidy eval**: every {{ !! !!! operation depends on it.

```r
# Defuse user argument
my_summarise <- function(data, var) {
  dplyr::summarise(data, mean = mean({{ var }}))
}

# {{ defuses and injects in one step
mtcars %>% my_summarise(mpg)
```

**Key operators:**
- `{{` - Embrace (defuse + inject)
- `!!` - Inject single expression
- `!!!` - Inject list of expressions (splice)
- `enquo()` - Defuse function argument
- `expr()` - Defuse local expression

**Reference:** `references/defusal-injection.md` for complete defusal/injection patterns

### 2. Tidy Evaluation

Programming with data frames where columns are variables:

```r
# Data-masking: columns as variables
with(mtcars, mean(cyl + am))

# Wrapping requires injection
mean_by <- function(data, by, var) {
  data %>%
    dplyr::group_by({{ by }}) %>%
    dplyr::summarise(avg = mean({{ var }}))
}
```

**Key concepts:**
- Data mask: Environment where columns become variables
- Embracing: `{{` for passing arguments through
- Pronouns: `.data$col` and `.env$var` for disambiguation
- Name injection: `"{name}" := value` and `"mean_{{ var }}"`

**Reference:** `references/tidy-evaluation.md` for complete tidy eval patterns

### 3. Structured Conditions

Better errors, warnings, and messages:

```r
check_positive <- function(x, arg = caller_arg(x), call = caller_env()) {
  if (x < 0) {
    cli::cli_abort(
      c(
        "{.arg {arg}} must be positive",
        "x" = "You provided {x}"
      ),
      call = call
    )
  }
}

my_function <- function(value) {
  check_positive(value)
}

my_function(-5)
#> Error in `my_function()`:
#> ! `value` must be positive
#> ✖ You provided -5
```

**Key functions:**
- `abort()` - Structured errors with bullet lists
- `warn()` / `inform()` - Warnings and messages
- `caller_env()` - Show user's function in error
- `caller_arg()` - Get user's argument name
- `try_fetch()` - Modern error catching with chaining

**Reference:** `references/conditions-errors.md` for complete error handling

### 4. Environments

Explicit scoping and evaluation control:

```r
# Create evaluation context
eval_context <- function(data, code) {
  ctx <- new_environment(data, parent = caller_env())
  eval_tidy(code, env = ctx)
}

# Use
data <- list(x = 1:10, y = 11:20)
eval_context(data, quo(mean(x + y)))
```

**Key functions:**
- `env()` - Create environment
- `env_bind()` / `env_get()` - Manage bindings
- `caller_env()` / `current_env()` - Stack navigation
- `local_bindings()` - Temporary changes

**Reference:** `references/environments.md` for environment manipulation

### 5. Symbols and Calls

Programmatic code construction:

```r
# Build expressions from data
col_name <- "mpg"
condition <- call2(">", sym(col_name), 20)

# Inject into dplyr
mtcars %>% dplyr::filter(!!condition)

# Build multiple columns
cols <- syms(c("mpg", "cyl", "hp"))
mtcars %>% dplyr::select(!!!cols)
```

**Key functions:**
- `sym()` / `syms()` - String to symbol
- `call2()` - Build function calls
- `expr()` / `exprs()` - Create expressions
- `call_modify()` - Modify call arguments

**Reference:** `references/symbols-calls.md` for code construction

### 6. Function Arguments

Robust argument handling:

```r
my_function <- function(method = c("fast", "accurate"), ...) {
  # Validate enumeration
  method <- arg_match(method)
  
  # No unexpected arguments
  check_dots_empty()
  
  # Continue with validated inputs
}
```

**Key functions:**
- `arg_match()` - Validate against allowed values
- `check_dots_empty()` / `check_dots_used()` - Validate `...`
- `list2()` - Collect dynamic dots with injection
- `caller_arg()` - Get user's argument name

**Reference:** `references/function-arguments.md` for argument patterns

## Essential Patterns

### Wrapping Data-Masking Functions

**Always use embracing ({{) when wrapping dplyr/ggplot2 functions. No exceptions.**

```r
# Single variable
my_filter <- function(data, condition) {
  dplyr::filter(data, {{ condition }})
}

# Multiple variables with ...
my_select <- function(data, ...) {
  dplyr::select(data, ...)
}

# Named output with name injection
summarise_var <- function(data, var) {
  dplyr::summarise(data, "mean_{{ var }}" := mean({{ var }}))
}
```

### Error Helpers

**You MUST include `call = caller_env()` in every error helper. Errors showing the helper instead of the user's function = failed user experience. Every time.**

```r
# Standard pattern for all validation functions
check_type <- function(x, 
                       type, 
                       arg = caller_arg(x), 
                       call = caller_env()) {
  if (!inherits(x, type)) {
    cli::cli_abort(
      "{.arg {arg}} must be a {.cls {type}}",
      call = call,
      class = "my_package_type_error"
    )
  }
}

# Set call once for whole function
my_function <- function(x, y) {
  local_error_call(current_env())
  
  if (x < 0) abort("x must be positive")
  if (y < 0) abort("y must be positive")
  # Both show correct error call
}
```

### Dynamic Code Construction

```r
# Build filter from user input
build_filter <- function(col, op, value) {
  call2(op, sym(col), value)
}

filter_expr <- build_filter("age", ">", 18)
dplyr::filter(df, !!filter_expr)

# Combine multiple conditions
conditions <- list(
  expr(age > 18),
  expr(status == "active")
)

# Combine with & (using base Reduce instead of purrr)
combined <- Reduce(function(x, y) call2("&", x, y), conditions)
dplyr::filter(df, !!combined)
```

### Capturing and Forwarding

```r
# Capture multiple arguments
my_group_summarise <- function(data, ..., var) {
  # ... goes to group_by unchanged
  # var needs embracing for summarise
  data %>%
    dplyr::group_by(...) %>%
    dplyr::summarise(mean = mean({{ var }}))
}

mtcars %>% my_group_summarise(cyl, am, var = mpg)
```

### Optional Arguments

```r
# Optional grouping
summarise_optional_group <- function(data, var, by = NULL) {
  if (!missing(by)) {
    data <- dplyr::group_by(data, {{ by }})
  }
  dplyr::summarise(data, mean = mean({{ var }}))
}
```

## Common Mistakes and Solutions

### Forgetting to Embrace

```r
# WRONG - looks for variable named "var"
my_fn <- function(data, var) {
  dplyr::filter(data, var > 10)
}

# RIGHT - injects user's expression
my_fn <- function(data, var) {
  dplyr::filter(data, {{ var }} > 10)
}
```

### Missing Caller Context in Errors

```r
# WRONG - shows check_positive() in error
check_positive <- function(x) {
  if (x < 0) abort("Must be positive")
}

# RIGHT - shows user's function
check_positive <- function(x, call = caller_env()) {
  if (x < 0) abort("Must be positive", call = call)
}
```

### Using `=` with Computed Names

```r
# WRONG - creates column named "name"
name <- "result"
dplyr::mutate(df, name = value)

# RIGHT - uses := for computed names
dplyr::mutate(df, "{name}" := value)
dplyr::mutate(df, !!name := value)
```

### Mixing Defusal Styles

```r
# WRONG - enquo() already defuses, don't use {{ too
my_fn <- function(data, var) {
  var_quo <- enquo(var)
  dplyr::filter(data, {{ var_quo }} > 10)
}

# RIGHT - either use enquo + !!, or just {{
my_fn <- function(data, var) {
  var_quo <- enquo(var)
  dplyr::filter(data, !!var_quo > 10)
}

# OR (simpler)
my_fn <- function(data, var) {
  dplyr::filter(data, {{ var }} > 10)
}
```

## Testing rlang Code

```r
test_that("function handles bare names", {
  result <- my_summarise(mtcars, mpg)
  expect_equal(result$mean, mean(mtcars$mpg))
})

test_that("function handles expressions", {
  result <- my_summarise(mtcars, mpg + cyl)
  expect_equal(result$mean, mean(mtcars$mpg + mtcars$cyl))
})

test_that("error shows correct call", {
  expect_snapshot(error = TRUE, {
    my_function(-5)
  })
})

test_that("error has correct class", {
  expect_error(
    my_function(invalid),
    class = "my_pkg_type_error"
  )
})
```

## Migration from Base R

| rlang | Base R | Why rlang? |
|-------|--------|------------|
| `enquo(x)` | `substitute(x)` | Quosures capture environment |
| `!!` | `bquote(.(x))` | Consistent syntax |
| `!!!` | `do.call()` | Inline splicing |
| `abort()` | `stop()` | Structured messages, classes, chaining |
| `eval_tidy()` | `eval()` | Data mask + quosure support |
| `env()` | `new.env()` | Cleaner API |
| `caller_env()` | `parent.frame()` | Explicit intent |

## Decision Tree

**Does your function accept bare column names for data-masking?**
- Yes → Use `{{`, load `references/tidy-evaluation.md`
- No → Continue

**Are you building/manipulating R expressions programmatically?**
- Yes → Use `expr()`, `call2()`, `!!`, load `references/symbols-calls.md`
- No → Continue

**Do you need custom evaluation contexts or environment control?**
- Yes → Use `env()`, `eval_tidy()`, load `references/environments.md`
- No → Continue

**Are you implementing structured error handling for a package?**
- Yes → Use `abort()`, `caller_env()`, load `references/conditions-errors.md`
- No → Continue

**Do you need dynamic dots with splicing/injection?**
- Yes → Use `list2()`, `!!!`, load `references/function-arguments.md`
- No → **Base R is probably sufficient**

## Key Principles

1. **Embrace for functions** - Use `{{` when wrapping data-masking functions. Always. No exceptions.
2. **Caller context for errors** - `call = caller_env()` is mandatory in every helper. Errors must show the user's call, never the helper's.
3. **Classes for conditions** - All package errors must have classes. Never use bare `stop()` in production code.
4. **Quosures for hygiene** - Preserve environment context with `enquo()`. Defusals without environments fail in complex pipelines.
5. **Test thoroughly** - Tidy eval and metaprogramming have subtle edge cases. Test with bare names, expressions, and programmatic construction.
6. **Document NSE** - Make clear when arguments use defusal/injection. Users cannot guess which arguments are data-masked.
7. **Fail informatively** - Structured errors help users fix problems. Bullet lists in `abort()` are required, not optional.

## Quick Reference

### Most Common Functions

**Tidy eval:**
- `{{` - Defuse and inject function argument
- `enquo()` / `enquos()` - Defuse arguments manually
- `!!` / `!!!` - Inject expressions
- `.data$col` / `.env$var` - Disambiguate

**Errors:**
- `abort()` - Throw structured error
- `caller_env()` - Get caller's environment for call context
- `caller_arg()` - Get caller's argument name
- `local_error_call()` - Set call context once

**Code construction:**
- `sym()` / `syms()` - String to symbol(s)
- `call2()` - Build function call
- `expr()` / `exprs()` - Create expression(s)

**Arguments:**
- `arg_match()` - Validate enumeration
- `list2()` - Collect dynamic dots
- `check_dots_empty()` - No extra arguments

**Environments:**
- `env()` - Create environment
- `env_bind()` / `env_get()` - Manage bindings
- `current_env()` / `caller_env()` - Stack navigation

## References (Load on Demand)

- **[references/tidy-evaluation.md](references/tidy-evaluation.md)** - Load when wrapping dplyr/ggplot2/tidyr or implementing data-masked APIs
- **[references/defusal-injection.md](references/defusal-injection.md)** - Load when capturing expressions or using `{{`, `!!`, `!!!` operators
- **[references/conditions-errors.md](references/conditions-errors.md)** - Load when implementing structured error handling with `abort()`
- **[references/environments.md](references/environments.md)** - Load when manipulating environments or evaluation contexts
- **[references/function-arguments.md](references/function-arguments.md)** - Load when using `arg_match()`, `list2()`, or validating arguments
- **[references/symbols-calls.md](references/symbols-calls.md)** - Load when programmatically constructing R expressions

Each reference contains detailed patterns, examples, and edge cases.
