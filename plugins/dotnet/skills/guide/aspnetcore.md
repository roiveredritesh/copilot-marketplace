# ASP.NET Core

## Check the version first
- The ASP.NET Core version is the `TargetFramework` (`net8.0` = ASP.NET Core 8). Read it before using an API marked ".NET n+" below. Don't suggest an upgrade just to use one.
- `System.Web` (MVC 5, Web API 2, WebForms) is classic ASP.NET on .NET Framework. None of this file applies; use `dotnet-legacy`.

## Dependency injection
- Lifetimes: Singleton for stateless, thread-safe services. Scoped for per-request services (DbContext, unit of work). Transient for light, stateless services.
- Captive dependency: a singleton holding a scoped service (such as a DbContext) is a bug. Enable `ValidateScopes` and `ValidateOnBuild` (on by default in Development).
- `BackgroundService` instances are singletons. Create scopes with `IServiceScopeFactory` for scoped work.
- Inject dependencies. Don't use a service locator (`IServiceProvider.GetService` in business code).
- `HttpContext` isn't thread-safe and lives only for the request. Don't store it in a field or use it from a background task; copy the values you need first.

## Middleware order (typical)
`UseForwardedHeaders` (behind a proxy) → `UseExceptionHandler` → `UseHsts` → `UseHttpsRedirection` → `UseStaticFiles` → `UseRouting` → `UseCors` → `UseAuthentication` → `UseAuthorization` → `UseAntiforgery` / `UseRateLimiter` / `UseOutputCache` / custom → `MapControllers` / `MapXxx`.
The exception handler goes first so it catches everything after it. CORS sits between routing and auth, and auth comes before the endpoints. Behind a reverse proxy, forwarded headers must come first or HTTPS redirection and client IPs are wrong. Configure the known proxies.

## Exception handling
- One global handler. .NET 8+: `AddExceptionHandler<T>()` + `AddProblemDetails()` + `app.UseExceptionHandler()`. `UseExceptionHandler()` with no argument throws at startup unless `AddProblemDetails()` is registered. Before .NET 8: `UseExceptionHandler("/error")` or `UseExceptionHandler(b => b.Run(...))`, reading `IExceptionHandlerFeature`.
- `IExceptionHandler.TryHandleAsync` returns `true` when it wrote the response and `false` to pass to the next handler. Handlers run in registration order. They're singletons, so take scoped services from `httpContext.RequestServices`, not the constructor.
- Prefer middleware over MVC exception filters (`IExceptionFilter`). Filters only see exceptions thrown in controller actions, not in middleware, minimal APIs, or model binding.
- Don't try/catch in every action. Catch only where you can recover, add context, or translate an exception, then rethrow with `throw;` (not `throw ex;`, which loses the stack trace) or wrap it with the original as `innerException`.
- Never swallow: no empty `catch`, no `catch (Exception) { return null; }`. Use `catch (X ex) when (condition)` filters instead of catch-and-rethrow.
- Expected outcomes aren't exceptions. Return `TypedResults.NotFound()`, `Conflict()`, or `ValidationProblem(errors)` (or a result type) for not-found, conflicts, and validation. Throwing for control flow is slow and floods the error logs.
- Map exceptions to status codes in the handler: your domain or validation exceptions → 400/422, not-found → 404, `DbUpdateConcurrencyException` → 409, unknown → 500. Keep one mapping, not one per controller.
- Return `ProblemDetails` for every error, including empty 4xx responses (`UseStatusCodePages()` with `AddProblemDetails()`). In production the `detail` is generic: no exception message, stack trace, SQL, or internal ids. The developer exception page is on automatically in Development (.NET 6+ `WebApplication`); never enable it in production.
- Log an exception once. In .NET 8 and 9 the middleware already logs every unhandled exception as an error, so don't log again in the handler. In .NET 10+ it no longer logs exceptions a handler handled (`TryHandleAsync` returned `true`), so log in the handler, or set `ExceptionHandlerOptions.SuppressDiagnosticsCallback`.
- A canceled request (`OperationCanceledException` while `RequestAborted` is canceled) isn't a server error. Don't map it to a 500 or log it as an error.
- If `Response.HasStarted` (a streamed response), the status and body can't be changed: the handlers don't run, the middleware logs the exception and the connection is aborted.
- `BackgroundService`: since .NET 6 an unhandled exception in `ExecuteAsync` stops the host. Catch and log per work item inside the loop, unless stopping the app is what you want.

## HTTP clients
- Use `IHttpClientFactory` (named or typed clients). `new HttpClient()` per call exhausts sockets. A single static client without `PooledConnectionLifetime` keeps stale DNS.
- Resilience: `AddStandardResilienceHandler()` (`Microsoft.Extensions.Http.Resilience` package, released with .NET 8) adds retries, timeouts, and a circuit breaker. Don't stack a second retry policy on top.
- Always pass a `CancellationToken`. A `CancellationToken` action parameter binds to `HttpContext.RequestAborted` automatically.
- Call `EnsureSuccessStatusCode()` or check `IsSuccessStatusCode` before reading the body.

## Configuration and options
- `services.AddOptions<T>().BindConfiguration("Section").ValidateDataAnnotations().ValidateOnStart()`, so bad config fails fast.
- `IOptions<T>` is a singleton snapshot, `IOptionsSnapshot<T>` is scoped (re-read per request, can't be injected into a singleton), `IOptionsMonitor<T>` gives change notifications.
- Secrets: user-secrets in development; environment variables or a vault in production. Never commit them in `appsettings.json`.

## Endpoints
- Minimal APIs or controllers are both fine, but keep one style per area. Use `TypedResults` (.NET 7+) for testable, OpenAPI-friendly results.
- Validate at the boundary and return `ValidationProblemDetails`. `[ApiController]` controllers return 400 automatically for invalid models. Minimal APIs validate data annotations only from .NET 10 (`AddValidation()`); before that, use an endpoint filter or FluentValidation.
- Bind requests to DTOs, never to EF entities: binding an entity lets clients set fields they shouldn't (over-posting).
- Authorization: define policies (`AddAuthorization(o => o.AddPolicy(...))`) and apply them with `[Authorize(Policy=...)]` / `.RequireAuthorization()`. Check resource ownership inside handlers to prevent IDOR. Consider a fallback policy that requires authenticated users, so a new endpoint isn't public by mistake.
- CORS: list the origins. `AllowAnyOrigin()` with `AllowCredentials()` throws when the policy is built.
- OpenAPI: .NET 9+ templates use the built-in `AddOpenApi()` / `MapOpenApi()` instead of Swashbuckle.
- Limit abuse: `AddRateLimiter` (.NET 7+) and `AddRequestTimeouts` (.NET 8+) on public or expensive endpoints.

## Logging and health
- Structured logging with message templates (`_log.LogInformation("Order {OrderId} paid", id)`), not string interpolation. Use `[LoggerMessage]` source generators on hot paths.
- Pass the exception as the first argument (`_log.LogError(ex, "...")`), not `ex.Message` in the template, so the stack trace is kept.
- Health checks: `AddHealthChecks()` with a DB check, and separate liveness and readiness endpoints.

## Performance
- Output caching (`AddOutputCache`, .NET 7+) for cacheable GETs; `IMemoryCache`, or `HybridCache` (`Microsoft.Extensions.Caching.Hybrid`, released with .NET 9) for data.
- Never block on async in the request pipeline. Keep `AllowSynchronousIO` false.
