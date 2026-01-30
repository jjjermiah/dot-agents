# Code Review Examples

Sample reviews demonstrating the expected format and level of detail.

## Example 1: Feature Implementation Review

**Context:** Review of user authentication endpoints (Step 3 of project plan)

### Overview
Implementation completes the planned authentication endpoints with JWT tokens. Code quality is generally good with solid error handling. Two important issues need addressing before deployment.

### Findings

**Severity: critical**
- **Location:** `src/auth/login.ts:45`
- **Issue:** JWT secret is hardcoded in source code
- **Rationale:** Exposing secrets in source code creates a security vulnerability, especially if code is pushed to version control
- **Fix:** Move JWT secret to environment variable
  ```typescript
  const secret = process.env.JWT_SECRET;
  if (!secret) throw new Error('JWT_SECRET not configured');
  ```

**Severity: important**
- **Location:** `src/auth/middleware.ts:23-28`
- **Issue:** JWT verification errors return 500 instead of 401
- **Rationale:** Server errors (5xx) indicate internal problems, but invalid/expired tokens are client errors (4xx). This confuses API consumers and monitoring systems.
- **Fix:** Catch JWT verification errors and return 401 Unauthorized
  ```typescript
  try {
    const decoded = jwt.verify(token, secret);
  } catch (err) {
    return res.status(401).json({ error: 'Invalid or expired token' });
  }
  ```

**Severity: important**
- **Location:** `tests/auth/login.test.ts`
- **Issue:** Tests don't verify token expiration behavior
- **Rationale:** Token expiration is critical security functionality. Without tests, regressions could go unnoticed.
- **Fix:** Add test cases for expired tokens and token validation edge cases

**Severity: suggestion**
- **Location:** `src/auth/types.ts:12`
- **Issue:** `LoginResponse` type doesn't include token expiry information
- **Rationale:** Clients need to know when to refresh tokens. Including expiry in the response improves API usability.
- **Fix:** Add `expiresAt` field to `LoginResponse` interface

### Tests / Verification
- Verify JWT secret is loaded from environment variables in all environments
- Run existing test suite and confirm new token expiration tests pass
- Test authentication flow end-to-end with valid, invalid, and expired tokens

## Example 2: Refactoring Review

**Context:** Refactoring of data fetching layer to use React Query

### Overview
The refactoring successfully introduces React Query and removes redundant state management. The implementation follows best practices and improves code maintainability. One important consideration for deployment.

### Findings

**Severity: important**
- **Location:** `src/hooks/useUserData.ts:8`
- **Issue:** Query key doesn't include user ID parameter
- **Rationale:** React Query uses query keys for caching. Without the user ID in the key, different users' data could be incorrectly cached and served.
- **Fix:** Include user ID in query key
  ```typescript
  const query = useQuery(['user', userId], () => fetchUser(userId));
  ```

**Severity: suggestion**
- **Location:** `src/api/client.ts:45`
- **Issue:** Retry logic uses default exponential backoff
- **Rationale:** While defaults work, customizing retry behavior for different error types improves user experience (e.g., don't retry 4xx errors, but do retry 5xx).
- **Fix:** Add custom retry logic based on error type
  ```typescript
  retry: (failureCount, error) => {
    if (error.status >= 400 && error.status < 500) return false;
    return failureCount < 3;
  }
  ```

**Severity: suggestion**
- **Location:** Throughout
- **Issue:** Old fetch functions remain in codebase alongside new React Query hooks
- **Rationale:** Having two data fetching approaches creates confusion and makes maintenance harder.
- **Fix:** Remove old fetch functions once migration is complete and verified

### Tests / Verification
- Verify query keys include all relevant parameters (user ID, filters, etc.)
- Test cache behavior by loading same data twice and confirming no duplicate requests
- Run full test suite to ensure no regressions from refactoring

## Example 3: Bug Fix Review

**Context:** Fix for incorrect date display in reports

### Overview
The fix correctly addresses the timezone conversion issue. Implementation is straightforward and includes appropriate tests.

### Findings

**Severity: suggestion**
- **Location:** `src/utils/dates.ts:23`
- **Issue:** Helper function name `fixDate` is vague
- **Rationale:** Function names should describe what they do, not that they fix something. Future developers won't know what was "broken."
- **Fix:** Rename to `convertToUserTimezone` or `formatDateInTimezone`

**Severity: suggestion**
- **Location:** `tests/utils/dates.test.ts`
- **Issue:** Tests only cover UTC and PST timezones
- **Rationale:** Date handling across timezones is error-prone. Testing more edge cases (especially timezones with unusual offsets) increases confidence.
- **Fix:** Add test cases for:
  - Half-hour offset timezones (e.g., IST +5:30)
  - Daylight saving time transitions
  - Southern hemisphere timezones (seasons inverted)

### Tests / Verification
- Run existing date tests and confirm they pass
- Manually verify date display in reports for different timezone settings
- Test around daylight saving time transition dates

## Key Patterns in Good Reviews

### 1. Context First
Always start with a brief overview that orients the reader to what was reviewed and the general assessment.

### 2. Severity-Based Prioritization
- **Critical:** Must fix before merge/deploy (security, data loss, crashes)
- **Important:** Should fix soon (bugs, poor UX, missing tests, performance issues)
- **Suggestion:** Consider for future (naming, organization, minor improvements)

### 3. Explain the "Why"
Every finding should include rationale explaining why it matters. This helps developers learn and understand priorities.

### 4. Provide Specific Fixes
When possible, show the exact code change needed. This makes fixes faster and ensures clarity.

### 5. Acknowledge Strengths
Mention what was done well, especially in the overview. This balances feedback and reinforces good practices.

### 6. Verification Steps
Include concrete steps to verify the code works as intended and fixes are correct.
