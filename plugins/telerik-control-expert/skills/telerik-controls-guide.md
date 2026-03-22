# Telerik Controls Guide

**Version**: 2.0.0
**Plugin**: telerik-control-expert
**Purpose**: Comprehensive reference for Telerik RadControls including common issues, properties, and configuration

## Overview

This skill provides comprehensive reference information for Telerik UI for ASP.NET AJAX controls, covering common issues, property configurations, best practices, and troubleshooting guidance. Use this as the definitive reference when working with Telerik controls in ASP.NET WebForms applications.

## Core Telerik Controls

### RadGrid

**Purpose**: Advanced data grid with paging, sorting, filtering, grouping, and editing

**Common Issues**:

1. **Paging Not Working**
   - **Cause**: Missing `AllowPaging="true"` or `PageSize` not set
   - **Solution**: Set `AllowPaging="true"` and `PageSize="20"`
   - **Cause**: Missing `Rebind()` call in `PageIndexChanged` event
   - **Solution**: Call `RadGrid1.Rebind()` in event handler

2. **Data Not Binding**
   - **Cause**: Data binding in wrong event
   - **Solution**: Use `NeedDataSource` event for data binding
   - **Code**:
     ```csharp
     protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e)
     {
         RadGrid1.DataSource = GetData();
     }
     ```

3. **ViewState Too Large**
   - **Cause**: Grid persisting all data in ViewState
   - **Solution**: Use `clientStateDataSource` or disable ViewState for data
   - **Code**: `<telerik:RadGrid EnableViewState="false" ... />`

**Key Properties**:
- `AllowPaging`: Enable pagination
- `PageSize`: Items per page
- `AllowSorting`: Enable column sorting
- `AllowFilteringByColumn`: Enable filtering
- `AllowMultiRowEdit`: Enable inline batch editing
- `DataSourceID` vs `DataSource`: Prefer `NeedDataSource` event

**Best Practices**:
- Always use `NeedDataSource` for data binding
- Call `Rebind()` after programmatic changes
- Use `clientStateDataSource` for better performance
- Enable `AllowPaging` for large datasets
- Use custom paging for very large datasets (100k+ rows)

### RadComboBox

**Purpose**: Advanced dropdown with search, templates, cascading, and load-on-demand

**Common Issues**:

1. **Items Not Loading**
   - **Cause**: `DataTextField` or `DataValueField` incorrect
   - **Solution**: Verify property names match data source
   - **Code**:
     ```aspx
     <telerik:RadComboBox
         DataTextField="Name"
         DataValueField="Id"
         DataSourceID="SqlDataSource1" />
     ```

2. **Selected Value Lost on Postback**
   - **Cause**: `EnableViewState="false"` or data rebinding
   - **Solution**: Enable ViewState, check `!Page.IsPostBack` before binding
   - **Code**:
     ```csharp
     if (!Page.IsPostBack)
     {
         RadComboBox1.DataBind();
     }
     ```

3. **Cascading Not Working**
   - **Cause**: Missing `ClientEvents-OnClientSelectedIndexChanged`
   - **Solution**: Configure cascading properly
   - **Code**:
     ```javascript
     function OnClientSelectedIndexChanging(sender, args) {
         var childCombo = $find("<%= RadComboBox2.ClientID %>");
         childCombo.clearItems();
         childCombo.requestItems(args.get_item().get_value(), false);
     }
     ```

**Key Properties**:
- `DataTextField`, `DataValueField`: Binding properties
- `AutoPostBack`: Post back on selection change
- `EnableLoadOnDemand`: Load items on demand (for large datasets)
- `MarkFirstMatch`: Highlight first match while typing
- `AllowCustomText`: Allow user-entered values
- `Filter`: Client-side filtering (`Contains`, `StartsWith`)

**Best Practices**:
- Use `EnableLoadOnDemand` for large item lists (500+ items)
- Use `Filter="Contains"` for user-friendly search
- Cache loaded items with `EnableItemCaching="true"`
- Use templates for rich item display
- Implement `ItemsRequested` event for load-on-demand

### RadEditor

**Purpose**: Rich text WYSIWYG editor with formatting, file management, and content filtering

**Common Issues**:

1. **Content Not Saving**
   - **Cause**: Content not retrieved from editor
   - **Solution**: Use `Content` property in postback
   - **Code**:
     ```csharp
     protected void btnSave_Click(object sender, EventArgs e)
     {
         string htmlContent = RadEditor1.Content;
         // Save htmlContent
     }
     ```

2. **Toolbar Missing**
   - **Cause**: Missing ToolsFile or incorrect Tools configuration
   - **Solution**: Use default tools or specify ToolsFile
   - **Code**: `<telerik:RadEditor ToolsFile="~/EditorTools.xml" ... />`

3. **Image Upload Failing**
   - **Cause**: Missing ImageManager configuration
   - **Solution**: Configure image upload paths
   - **Code**:
     ```aspx
     <telerik:RadEditor>
         <ImageManager
             ViewPaths="~/Images"
             UploadPaths="~/Images"
             DeletePaths="~/Images" />
     </telerik:RadEditor>
     ```

**Key Properties**:
- `Content`: HTML content
- `ContentFilters`: Strip unwanted HTML (`DefaultFilters`, `StripAllFormattingTags`)
- `ToolsFile`: XML file defining toolbar
- `Height`, `Width`: Editor dimensions
- `EditModes`: Design, HTML, Preview modes
- `EnableResize`: Allow user resizing

**Best Practices**:
- Use `ContentFilters` to sanitize HTML (XSS prevention)
- Configure file managers (ImageManager, DocumentManager)
- Set realistic `MaxImageSize` and `MaxDocumentSize`
- Use custom ToolsFile for consistent toolbar
- Validate and sanitize content server-side

### RadAjaxManager / RadAjaxPanel

**Purpose**: AJAX-enable controls without full page postbacks

**Common Issues**:

1. **Full Postback Instead of AJAX**
   - **Cause**: AjaxSettings not configured
   - **Solution**: Add AjaxSetting with initiator and updated controls
   - **Code**:
     ```aspx
     <telerik:RadAjaxManager ID="RadAjaxManager1">
         <AjaxSettings>
             <telerik:AjaxSetting AjaxControlID="btnSubmit">
                 <UpdatedControls>
                     <telerik:AjaxUpdatedControl ControlID="RadGrid1" />
                 </UpdatedControls>
             </telerik:AjaxSetting>
         </AjaxSettings>
     </telerik:RadAjaxManager>
     ```

2. **Loading Icon Not Showing**
   - **Cause**: Missing LoadingPanel configuration
   - **Solution**: Add RadAjaxLoadingPanel and reference it
   - **Code**:
     ```aspx
     <telerik:RadAjaxManager ID="RadAjaxManager1">
         <AjaxSettings>
             <telerik:AjaxSetting AjaxControlID="btnSubmit">
                 <UpdatedControls>
                     <telerik:AjaxUpdatedControl ControlID="RadGrid1"
                         LoadingPanelID="RadAjaxLoadingPanel1" />
                 </UpdatedControls>
             </telerik:AjaxSetting>
         </AjaxSettings>
     </telerik:RadAjaxManager>

     <telerik:RadAjaxLoadingPanel ID="RadAjaxLoadingPanel1" />
     ```

3. **JavaScript Errors After AJAX Update**
   - **Cause**: Scripts not re-executing after partial update
   - **Solution**: Use `Sys.Application.add_load()` for script registration
   - **Code**:
     ```javascript
     Sys.Application.add_load(function() {
         // Code runs after every partial postback
         initializeControls();
     });
     ```

**Key Concepts**:
- **RadAjaxManager**: Global AJAX configuration (one per page)
- **RadAjaxPanel**: Wrap controls for automatic AJAX (simple scenarios)
- **AjaxSettings**: Define which control triggers update which controls
- **LoadingPanel**: Show loading indicator during AJAX request

**Best Practices**:
- Use RadAjaxManager for complex scenarios
- Use RadAjaxPanel for simple scenarios
- Don't mix RadAjax with ASP.NET UpdatePanel
- Always show LoadingPanel for user feedback
- Update only necessary controls (not entire page)

### RadWindow

**Purpose**: Modal and non-modal popup windows

**Common Issues**:

1. **Window Not Centering**
   - **Cause**: `VisibleOnPageLoad="true"` with wrong dimensions
   - **Solution**: Call `center()` client-side or set proper position
   - **Code**:
     ```javascript
     function openWindow() {
         var window = $find("<%= RadWindow1.ClientID %>");
         window.show();
         window.center();
     }
     ```

2. **Cannot Pass Data Between Windows**
   - **Cause**: Not using RadWindow argument/result pattern
   - **Solution**: Use `get_argument()` and `set_returnValue()`
   - **Code**:
     ```javascript
     // Parent page - open window with argument
     function openWindowWithData() {
         var window = $find("<%= RadWindow1.ClientID %>");
         window.setUrl("Popup.aspx");
         window.set_argument({userId: 123});
         window.add_close(onWindowClose);
         window.show();
     }

     // Popup page - get argument and return value
     function getArgument() {
         var arg = GetRadWindow().get_argument();
         var userId = arg.userId;
     }

     function closeAndReturn() {
         GetRadWindow().set_returnValue("Success");
         GetRadWindow().close();
     }

     // Parent page - handle close
     function onWindowClose(sender, args) {
         var result = args.get_returnValue();
         alert(result);
     }
     ```

**Key Properties**:
- `VisibleOnPageLoad`: Show on page load
- `Modal`: Block parent page interaction
- `Width`, `Height`: Window dimensions
- `Behaviors`: Minimize, Maximize, Close, etc.
- `NavigateUrl`: Content URL
- `OpenerElementID`: Control that opens window

**Best Practices**:
- Use `Modal="true"` for critical dialogs
- Always provide `Width` and `Height`
- Use `ReloadOnShow="true"` to refresh content
- Use argument/returnValue pattern for data exchange
- Call `center()` after showing window

## Common Patterns

### Data Binding Pattern
```csharp
// CORRECT: Use NeedDataSource
protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e)
{
    if (!e.IsFromDetailTable)
    {
        RadGrid1.DataSource = GetData();
    }
}

// INCORRECT: Binding in Page_Load
protected void Page_Load(object sender, EventArgs e)
{
    if (!Page.IsPostBack)
    {
        RadGrid1.DataSource = GetData();
        RadGrid1.DataBind(); // Don't do this
    }
}
```

### Cascading ComboBoxes Pattern
```javascript
function OnClientSelectedIndexChanged_Country(sender, args) {
    var cityCombo = $find("<%= RadComboBoxCity.ClientID %>");
    cityCombo.clearItems();
    cityCombo.set_enabled(true);

    var countryId = args.get_item().get_value();
    cityCombo.requestItems(countryId, false);
}
```

### AJAX Callback Pattern
```csharp
// Code-behind
protected void RadAjaxManager1_AjaxRequest(object sender, AjaxRequestEventArgs e)
{
    if (e.Argument == "RefreshGrid")
    {
        RadGrid1.Rebind();
    }
}

// Client-side
function refreshGrid() {
    var ajaxManager = $find("<%= RadAjaxManager1.ClientID %>");
    ajaxManager.ajaxRequest("RefreshGrid");
}
```

## Performance Optimization

### ViewState Optimization
```aspx
<!-- Disable ViewState for read-only controls -->
<telerik:RadGrid EnableViewState="false" ... />

<!-- Use clientStateDataSource for RadGrid -->
<telerik:RadGrid>
    <ClientSettings>
        <DataBinding
            SelectMethod="GetData"
            EnableClientSideDataSourceBinding="true" />
    </ClientSettings>
</telerik:RadGrid>
```

### AJAX Optimization
```aspx
<!-- Update only necessary controls -->
<telerik:AjaxSetting AjaxControlID="btnFilter">
    <UpdatedControls>
        <telerik:AjaxUpdatedControl ControlID="RadGrid1" />
        <!-- Don't update entire panel if not needed -->
    </UpdatedControls>
</telerik:AjaxSetting>
```

### Paging Optimization
```csharp
// Custom paging for large datasets
RadGrid1.AllowCustomPaging = true;
RadGrid1.VirtualItemCount = GetTotalCount();

protected void RadGrid1_NeedDataSource(object sender, GridNeedDataSourceEventArgs e)
{
    int pageSize = RadGrid1.PageSize;
    int currentPage = RadGrid1.CurrentPageIndex;

    RadGrid1.DataSource = GetPagedData(currentPage, pageSize);
}
```

## Deprecated Properties

### Common Deprecated Properties
- `Skin` → Use `RenderMode="Lightweight"` instead
- `EnableEmbeddedSkins` → Use `RenderMode`
- Classic render mode → Use Lightweight or Mobile render modes

### Version-Specific Deprecations
Check Telerik documentation for version-specific deprecated properties.

## Troubleshooting Checklist

### Control Not Working
- [ ] ScriptManager exists on page
- [ ] Telerik assemblies referenced
- [ ] web.config properly configured
- [ ] No JavaScript errors in console
- [ ] ViewState enabled if needed
- [ ] Data binding in correct event
- [ ] AJAX configuration correct

### Performance Issues
- [ ] ViewState size reasonable
- [ ] Paging enabled for large datasets
- [ ] AJAX used instead of full postbacks
- [ ] Client-side operations where possible
- [ ] Caching enabled where appropriate
- [ ] Custom paging for very large datasets

### Upgrade Issues
- [ ] All assemblies same version
- [ ] web.config updated for new version
- [ ] Deprecated properties replaced
- [ ] Breaking changes reviewed
- [ ] Render mode updated if needed

## Resources

- **Official Documentation**: https://docs.telerik.com/devtools/aspnet-ajax/
- **Demos**: https://demos.telerik.com/aspnet-ajax/
- **Forums**: https://www.telerik.com/forums/aspnet-ajax
- **Knowledge Base**: https://docs.telerik.com/devtools/aspnet-ajax/knowledge-base

---

**Guide Version**: 2.0.0
**Last Updated**: 2026-01-16
**Usage**: Reference this guide when diagnosing, configuring, or optimizing Telerik controls
