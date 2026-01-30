# Code Review Checklists

Detailed checklists for different types of code reviews.

## General Code Review Checklist

### Correctness
- [ ] Logic implements the intended behavior correctly
- [ ] Edge cases are handled (null, empty, boundary values)
- [ ] Error conditions produce appropriate errors/exceptions
- [ ] Return values match expected types and contracts

### Error Handling
- [ ] Errors are caught at appropriate levels
- [ ] Error messages are clear and actionable
- [ ] Resources are cleaned up in error paths (files, connections, locks)
- [ ] Errors don't expose sensitive information

### Type Safety
- [ ] Types are explicit where needed (no implicit any/dynamic)
- [ ] Type conversions are safe and validated
- [ ] Null/undefined handling is explicit
- [ ] Generic constraints are appropriate

### Maintainability
- [ ] Code follows project conventions and style
- [ ] Naming is clear and consistent
- [ ] Functions/methods have single responsibilities
- [ ] Magic numbers/strings are extracted to constants
- [ ] Complex logic has explanatory comments

### Testing
- [ ] Unit tests cover happy paths
- [ ] Unit tests cover edge cases and error conditions
- [ ] Integration tests verify component interactions
- [ ] Test names clearly describe what they verify
- [ ] Tests are isolated and don't depend on execution order

### Performance
- [ ] No obvious performance bottlenecks (N+1 queries, nested loops)
- [ ] Resources are released promptly (connections, file handles)
- [ ] Caching is used appropriately
- [ ] Algorithms have reasonable time/space complexity

### Security
- [ ] User input is validated and sanitized
- [ ] SQL queries use parameterization (no string concatenation)
- [ ] Authentication/authorization checks are present
- [ ] Sensitive data is not logged
- [ ] Secrets are not hardcoded

## API Review Checklist

### Design
- [ ] Endpoints follow RESTful conventions
- [ ] Resource naming is consistent and intuitive
- [ ] HTTP methods match operations (GET/POST/PUT/DELETE)
- [ ] Status codes are appropriate (200, 201, 400, 404, 500)

### Validation
- [ ] Request body/params are validated
- [ ] Required fields are enforced
- [ ] Field types and formats are validated
- [ ] Validation errors return clear messages

### Security
- [ ] Authentication is required where needed
- [ ] Authorization checks are present
- [ ] Rate limiting is implemented
- [ ] CORS is configured appropriately

### Documentation
- [ ] Endpoint purpose is documented
- [ ] Request/response schemas are defined
- [ ] Error responses are documented
- [ ] Examples are provided

## Database Review Checklist

### Schema
- [ ] Tables/collections are normalized appropriately
- [ ] Indexes are present on frequently queried fields
- [ ] Foreign key relationships are defined
- [ ] Constraints enforce data integrity

### Queries
- [ ] Queries use indexes effectively
- [ ] No N+1 query problems
- [ ] Transactions are used for multi-step operations
- [ ] Connection pooling is configured

### Migrations
- [ ] Migrations are reversible (down scripts)
- [ ] Schema changes are backward compatible
- [ ] Data migrations preserve existing data
- [ ] Migration order is correct

## Frontend Review Checklist

### Component Design
- [ ] Components are appropriately sized
- [ ] Props are well-defined and typed
- [ ] State management is appropriate for scope
- [ ] Side effects are handled properly

### Accessibility
- [ ] Semantic HTML elements are used
- [ ] ARIA labels are present where needed
- [ ] Keyboard navigation works
- [ ] Color contrast meets WCAG standards

### Performance
- [ ] Components don't re-render unnecessarily
- [ ] Large lists are virtualized
- [ ] Images are optimized and lazy-loaded
- [ ] Bundle size is reasonable

### User Experience
- [ ] Loading states are shown
- [ ] Error states are handled gracefully
- [ ] Forms have validation feedback
- [ ] Actions provide confirmation/feedback
