# CI templates

## GitHub Actions: SDK-style .NET (Linux)
```yaml
name: ci
on:
  pull_request:
  push:
    branches: [main]
permissions:
  contents: read
concurrency:
  group: ci-${{ github.ref }}
  cancel-in-progress: true
jobs:
  build-test:
    runs-on: ubuntu-latest
    # services:                    # keep only if integration tests need PostgreSQL without Testcontainers
    #   postgres:
    #     image: postgres:17-alpine
    #     env: { POSTGRES_PASSWORD: postgres }
    #     ports: ["5432:5432"]
    #     options: --health-cmd pg_isready --health-interval 5s --health-retries 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-dotnet@v4
        with:
          global-json-file: global.json   # or: dotnet-version: 9.0.x
          cache: true
          cache-dependency-path: '**/packages.lock.json'   # remove if lock files aren't used
      - run: dotnet restore
      - run: dotnet build --no-restore -c Release -warnaserror
      - run: dotnet test --no-build -c Release --logger trx --collect:"XPlat Code Coverage" --results-directory TestResults
      - uses: actions/upload-artifact@v4
        if: always()
        with: { name: test-results, path: TestResults }
      - run: dotnet list package --vulnerable --include-transitive 2>&1 | tee vuln.txt; ! grep -q '>' vuln.txt
```
Testcontainers tests work on `ubuntu-latest` (Docker is available) with no services block.

## GitHub Actions: legacy .NET Framework (Windows)
```yaml
name: ci-netfx
on: [pull_request, push]
jobs:
  build-test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v4
      - uses: microsoft/setup-msbuild@v2
      - uses: NuGet/setup-nuget@v2
      - run: nuget restore MySolution.sln
      - run: msbuild MySolution.sln /m /p:Configuration=Release /nologo /v:m
      - name: test
        shell: pwsh
        run: |
          $vs = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -latest -products * -property installationPath
          $dlls = Get-ChildItem -Recurse -Filter *Tests.dll | Where-Object FullName -match '\\bin\\Release\\' | ForEach-Object FullName
          & "$vs\Common7\IDE\Extensions\TestPlatform\vstest.console.exe" $dlls /Logger:trx
```

## Azure DevOps: SDK-style
```yaml
trigger: [main]
pr: [main]
pool: { vmImage: ubuntu-latest }
steps:
  - task: UseDotNet@2
    inputs: { useGlobalJson: true }
  - script: dotnet restore
  - script: dotnet build --no-restore -c Release
  - task: DotNetCoreCLI@2
    inputs:
      command: test
      arguments: --no-build -c Release --collect:"XPlat Code Coverage"
      publishTestResults: true
```
For .NET Framework on Azure DevOps: `pool: windows-latest`, then `NuGetCommand@2` (restore), `VSBuild@1`, `VSTest@3`.

## Deploy stage (add only on request)
Use environment-scoped secrets, an approval gate for production, and migration bundles (`dotnet ef migrations bundle`) run as a separate step before the app rollout.
