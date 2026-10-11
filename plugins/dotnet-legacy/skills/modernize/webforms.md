# WebForms modernization

WebForms (`System.Web.UI`) does not exist on modern .NET. The UI layer has to be rewritten. The goal is to rewrite **only** the UI, reusing business logic and data access after they're decoupled from `System.Web`.

## Choose the target
| Target | Pick when | Watch out |
|---|---|---|
| **Blazor Server** (or Blazor Web App, interactive server) | event-driven pages, heavy server state, the closest mental model to WebForms (components + events) | a SignalR circuit per user: memory per user, sticky sessions, reconnect UX |
| **Blazor WebAssembly** | offline or rich client, API already exists | download size, all data goes through an API, no direct DB access |
| **Razor Pages** | form-over-data pages, CRUD, SEO-relevant pages | no component event model. Postback logic becomes GET/POST handlers |
| **MVC + (React/Angular)** | a separate SPA team, a public API needed anyway | two stacks to maintain |

## Concept mapping
| WebForms | Blazor | Razor Pages |
|---|---|---|
| `.aspx` page + code-behind | `.razor` component with `@page`, `@code` | `.cshtml` + `PageModel` |
| Master page | `MainLayout.razor` (`@Body`) | `_Layout.cshtml` (`@RenderBody()`) |
| User control `.ascx` | child component with `[Parameter]` | partial view / view component / tag helper |
| Server controls (`TextBox`, `DropDownList`, `CheckBox`) | `<InputText @bind-Value>`, `<InputSelect>`, `<InputCheckbox>` inside `<EditForm>` | `<input asp-for>`, `<select asp-items>` |
| `GridView` / `Repeater` / `ListView` | `@foreach` table, `QuickGrid` (paging/sort), or a component library grid | `@foreach` table + paging handler |
| Validators (`RequiredFieldValidator`...) | DataAnnotations + `<DataAnnotationsValidator>` + `<ValidationMessage>` | DataAnnotations + `asp-validation-for` |
| `OnClick` postback | `@onclick="Handler"` | `OnPost<Name>Async` handler |
| `UpdatePanel` | not needed: Blazor re-renders only the diff | fetch/htmx partial updates |
| `Page_Load` / `!IsPostBack` | `OnInitializedAsync` / `OnParametersSetAsync` | `OnGetAsync` |
| `ViewState` | component fields (live for the circuit) | hidden fields / TempData / re-query |
| `Session[...]` | scoped service per circuit; ProtectedSessionStorage; distributed cache | `ISession` with distributed cache (needs `AddSession`) |
| `Response.Redirect` | `NavigationManager.NavigateTo` | `RedirectToPage` |
| `Server.MapPath` | `IWebHostEnvironment.WebRootPath/ContentRootPath` | same |
| `HttpContext.Current` | inject `IHttpContextAccessor` (avoid in components; prefer passing state) | `HttpContext` property on the PageModel |
| Forms authentication / Membership | ASP.NET Core Identity or OIDC (Entra ID etc.) | same |

## Third-party control suites (e.g. Telerik RadControls, AjaxControlToolkit)
Each suite needs its vendor's Blazor or Core product, or a replacement. Inventory which controls are used and how much (the grid is usually the hardest) before estimating. Budget for licenses and the grid feature gaps.

## Migration strategy
1. **Decouple first, inside the old app.** Move business logic out of code-behind into class libraries with no `System.Web` references. Multi-target those libraries (`net48;net8.0`) so both apps share them.
2. **Side-by-side with a reverse proxy (strangler fig).** The new ASP.NET Core app sits in front, routes migrated paths itself, and proxies the rest to the old app (YARP; `Microsoft.AspNetCore.SystemWebAdapters` for shared session and auth during the transition).
3. **Migrate by feature/area** (highest value or lowest risk first). Each area ships independently, with parity tests.
4. Retire the old app when no routes remain.

A big-bang rewrite is only reasonable for small apps (roughly under 30 pages) with good test coverage of the behavior.

## Parity checklist per page
- Same validation rules (client and server), same error messages.
- Same authorization rules per role. Check that no page loses an `[Authorize]`.
- Same URLs, or redirects from the old ones (bookmarks, SEO).
- Same data written. Compare DB writes for identical inputs.
- Performance at least equal (ViewState removal usually helps).
- Tests: bUnit for Blazor components; `WebApplicationFactory` integration tests; Playwright for end-to-end flows.
