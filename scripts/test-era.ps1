[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ChildWorktrees,
    [Parameter(Mandatory)][string]$ArtifactRoot,
    [string]$SourcesRoot = 'C:/Dev/WoW',
    [string]$ClientRoot = 'C:/Program Files (x86)/World of Warcraft/_classic_era_',
    [switch]$SkipFrozenRegression
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repo = Split-Path -Parent $PSScriptRoot
if (Test-Path -LiteralPath $ArtifactRoot) { throw 'Use a new external artifact directory.' }
Push-Location $repo
try {
    # Validate fresh Era authority before API-dependent tests.
    python -B scripts/era_distribution.py --client-root $ClientRoot --sources-root $SourcesRoot --output (Join-Path $ArtifactRoot 'packages')
    if ($LASTEXITCODE -ne 0) { throw 'Era source/API verification or build failed.' }
    $lock = Get-Content distribution/era/candidate.lock.json -Raw | ConvertFrom-Json
    foreach ($child in $lock.children) {
        $childRoot = Join-Path $ChildWorktrees $child.name
        if ((git -C $childRoot rev-parse HEAD) -ne $child.commit) { throw "Wrong test source revision: $($child.name)" }
        if (git -C $childRoot status --porcelain) { throw "Uncommitted test source: $($child.name)" }
        Push-Location $childRoot
        try {
            foreach ($file in git ls-files '*.lua') {
                luac -p $file
                if ($LASTEXITCODE -ne 0) { throw "Lua parse failed: $file" }
            }
            foreach ($spec in Get-ChildItem tests/*_spec.lua | Sort-Object Name) {
                lua $spec.FullName
                if ($LASTEXITCODE -ne 0) { throw "Child regression failed: $($spec.Name)" }
            }
        } finally { Pop-Location }
    }
    python -B tests/distribution/test_era.py --sources-root $SourcesRoot --child-worktrees $ChildWorktrees --client-root $ClientRoot -v
    if ($LASTEXITCODE -ne 0) { throw 'Generated Era package checks failed.' }
    $priorChildren = $env:APOGEE_CHILD_WORKTREES
    $priorSources = $env:APOGEE_SOURCES_ROOT
    try {
        $env:APOGEE_CHILD_WORKTREES = $ChildWorktrees
        $env:APOGEE_SOURCES_ROOT = $SourcesRoot
        python -B tests/distribution/test_launcher.py -v
        if ($LASTEXITCODE -ne 0) { throw 'Generated shared launcher checks failed.' }
    } finally {
        $env:APOGEE_CHILD_WORKTREES = $priorChildren
        $env:APOGEE_SOURCES_ROOT = $priorSources
    }
    if (-not $SkipFrozenRegression) {
        Write-Host 'Frozen Forever OFFLINE regression checks only; no live Forever validation.'
        foreach ($test in @('test_repository', 'test_curseforge', 'test_publisher')) {
            python -B "tests/distribution/$test.py"
            if ($LASTEXITCODE -ne 0) { throw "Frozen regression failed: $test" }
        }
        foreach ($test in @('test_distribution', 'test_migration', 'test_dual')) {
            python -B "tests/distribution/$test.py" --sources-root $SourcesRoot --artifacts (Join-Path $ArtifactRoot $test)
            if ($LASTEXITCODE -ne 0) { throw "Frozen regression failed: $test" }
        }
    }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'Whitespace check failed.' }
    Write-Host 'Era offline candidate verified. Native user testing and installation approval remain separate.'
} finally { Pop-Location }
