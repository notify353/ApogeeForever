[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$ChildWorktrees,
    [Parameter(Mandatory=$true)][string]$ArtifactRoot,
    [string]$SourcesRoot = 'C:/Dev/WoW',
    [string]$WowRoot = 'C:/Program Files (x86)/World of Warcraft'
)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    & ./scripts/check-wow-api-export.ps1 -Client Live -WowRoot $WowRoot -RequireInstalled
    & python -B scripts/validate_candidates.py --child-worktrees $ChildWorktrees `
        --sources-root $SourcesRoot --artifact-root $ArtifactRoot `
        --client-root (Join-Path $WowRoot '_classic_era_') `
        --forever-client-root (Join-Path $WowRoot '_forever_')
    if ($LASTEXITCODE -ne 0) { throw 'Live Forever candidate validation failed.' }
    Write-Host 'Live Forever authority and generated candidate validation passed. No installation; native acceptance is still required.'
} finally { Pop-Location }
