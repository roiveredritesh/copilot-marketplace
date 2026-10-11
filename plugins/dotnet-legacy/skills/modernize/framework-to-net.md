# .NET Framework 4.x → modern .NET

## Assess
- **Project format first:** convert each project to SDK-style (`dotnet tool install -g upgrade-assistant`, or by hand), still targeting `net48`. This step is low-risk and makes the rest mechanical.
- Then multi-target libraries (`<TargetFrameworks>net48;net8.0</TargetFrameworks>`) and fix compile errors behind `#if NETFRAMEWORK` only where unavoidable.
- Order: leaf libraries → shared libraries → app hosts (web, services) last.
- Dependencies: check each NuGet package for a .NET-compatible version. Packages without one are blockers (find a replacement or isolate them).
- Analyze API usage: the .NET Upgrade Assistant analysis, or the inventory counts from SKILL.md step 1.

## Breaking areas and replacements
| .NET Framework | Modern .NET |
|---|---|
| `System.Web` (HttpContext, modules, handlers) | ASP.NET Core middleware, endpoints, `IHttpContextAccessor` |
| `Global.asax` events | `Program.cs` startup + middleware + `IHostedService` |
| `web.config` / `app.config` + `ConfigurationManager` | `appsettings.json` + environment variables + `IOptions<T>`. A `System.Configuration.ConfigurationManager` package exists as a stop-gap |
| HTTP modules / handlers | middleware / endpoints |
| WCF server | CoreWCF (closest), gRPC, or REST. WCF *client* works via the `System.ServiceModel.*` packages |
| ASMX web services | REST/gRPC; CoreWCF for SOAP compatibility |
| .NET Remoting, AppDomains, Code Access Security | not supported: use IPC (gRPC/named pipes), separate processes, `AssemblyLoadContext` |
| `BinaryFormatter` | removed: System.Text.Json, MessagePack, protobuf. Plan data-format migration for persisted blobs |
| EF6 with EDMX | EF Core (code-first: scaffold with `dotnet ef dbcontext scaffold`) or EF 6.4+ on .NET as an intermediate step (EDMX designer not supported) |
| Windows Service (`ServiceBase`) | Worker Service + `UseWindowsService()` |
| `System.Drawing` on servers | Windows-only on .NET 6+. Use ImageSharp/SkiaSharp for cross-platform |
| Registry, WMI, Event Log | Windows-only packages (`Microsoft.Win32.Registry`, `System.Management`). Fine when staying on Windows |
| Forms auth / Membership | ASP.NET Core Identity or OIDC |
| `HttpWebRequest` / `WebClient` | `HttpClient` via `IHttpClientFactory` |

## Behavior differences to test for
- Default string comparison and globalization: modern .NET uses ICU, so culture-sensitive `IndexOf`/`StartsWith` behave differently. Use `StringComparison.Ordinal` where it matters.
- `DateTime` and time zone APIs: IANA vs Windows zone ids (`TimeZoneInfo.FindSystemTimeZoneById` accepts both on .NET 6+ with ICU).
- JSON: System.Text.Json is stricter than Newtonsoft (case sensitivity, number handling). Keep Newtonsoft (`AddNewtonsoftJson`) during migration if contracts depend on it.
- `SynchronizationContext`: ASP.NET Core has none, so old deadlock-avoidance hacks can go, but blocking calls now starve the thread pool instead.

## Strategy
- **In-place** (libraries, services, small apps): SDK-style → multi-target → switch the host → drop `net48`.
- **Strangler fig** (large web apps): a new ASP.NET Core host fronts the old one via YARP and moves routes over (`Microsoft.AspNetCore.SystemWebAdapters` for shared session/auth). See webforms.md for UI.
- Keep both builds in CI while multi-targeting. Run the same test suite against both targets.

## Checklist
- [ ] All projects SDK-style, building on `net48`
- [ ] Packages updated or replaced; no `packages.config`
- [ ] Libraries multi-targeted and green on both targets
- [ ] Config moved to `IOptions<T>`; secrets out of config files
- [ ] Host migrated (web: ASP.NET Core; services: Worker Service)
- [ ] Data access on EF Core (or EF 6.4 on .NET as an interim step)
- [ ] Performance and parity tests vs the old system; rollback plan per phase
