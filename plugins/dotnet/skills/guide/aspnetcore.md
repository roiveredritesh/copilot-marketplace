# ASP.NET Core

## Dependency injection
- Lifetimes: Singleton for stateless, thread-safe services. Scoped for per-request services (DbContext, unit of work). Transient for light, stateless services.
- Captive dependency: a singleton holding a scoped service (such as a DbContext) is a bug. Enable `ValidateScopes` and `ValidateOnBuild` (on by default in Development).
- `BackgroundService` instances are singletons. Create scopes with `IServiceScopeFactory` for scoped work.
- Inject dependencies. Don't use a service locator (`IServiceProvider.GetService` in business code).

## Middleware order (typical)
`UseExceptionHandler` → `UseHsts` → `UseHttpsRedirection` → `UseStaticFiles` → `UseRouting` → `UseCors` → `UseAuthentication` → `UseAuthorization` → rate limiting / custom → `MapControllers` / `MapXxx`.
The exception handler goes first, CORS sits between routing and auth, and auth comes before the endpoints.

## HTTP clients
- Use `IHttpClientFactory` (named or typed clients). `new HttpClient()` per call exhausts sockets. A single static client without `PooledConnectionLifetime` keeps stale DNS.
- Resilience: `AddStandardResilienceHandler()` (Microsoft.Extensions.Http.Resilience) adds retries, timeouts, and a circuit breaker.
- Always pass a `CancellationToken`. `HttpContext.RequestAborted` flows into action parameters automatically.

## Configuration and options
- `services.AddOptions<T>().BindConfiguration("Section").ValidateDataAnnotations().ValidateOnStart()`, so bad config fails fast.
- `IOptions<T>` is a singleton snapshot, `IOptionsSnapshot<T>` is per request, `IOptionsMonitor<T>` gives change notifications.
- Secrets: user-secrets in development; environment variables or a vault in production. Never commit them in `appsettings.json`.

## Endpoints
- Minimal APIs or controllers are both fine, but keep one style per area. Use `TypedResults` for testable, OpenAPI-friendly results.
- Validate at the boundary (data annotations or FluentValidation) and return `ProblemDetails` (`AddProblemDetails()`).
- Authorization: define policies (`AddAuthorization(o => o.AddPolicy(...))`) and apply them with `[Authorize(Policy=...)]` / `.RequireAuthorization()`. Check resource ownership inside handlers to prevent IDOR.

## Errors and logging
- Global exception handling with `UseExceptionHandler` + `IExceptionHandler` (.NET 8+). Don't try/catch in every action.
- Structured logging with message templates (`_log.LogInformation("Order {OrderId} paid", id)`), not string interpolation. Use `[LoggerMessage]` source generators on hot paths.
- Health checks: `AddHealthChecks()` with a DB check, and separate liveness and readiness endpoints.

## Performance
- Output caching (`AddOutputCache`) for cacheable GETs; `IMemoryCache` or `HybridCache` (.NET 9+) for data.
- Never block on async in the request pipeline. Keep `AllowSynchronousIO` false.
