[CmdletBinding()]
param([Parameter(Mandatory)][string]$Version, [string]$SourcesRoot = 'C:/Dev/WoW',
      [ValidateSet('classic-era','forever')][string]$Target, [string]$ClientRoot,
      [string]$ChildWorktrees, [string]$Notes, [string]$Basis)
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
if ($Version -notmatch '^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$') { throw 'Stable X.Y.Z version required.' }
$repo = Split-Path -Parent $PSScriptRoot
Push-Location $repo
try {
    if ((git branch --show-current) -ne 'main') { throw 'Prepare only from main.' }
    if (git status --porcelain) { throw 'Working tree must be clean; preserve existing changes.' }
    if ((git remote get-url origin).TrimEnd('/') -notmatch '^https://github.com/notify353/ApogeeForever(\.git)?$') { throw 'Unexpected remote.' }
    git fetch origin main
    if ($LASTEXITCODE -ne 0) { throw 'Fetch failed.' }
    if ((git rev-parse HEAD) -ne (git rev-parse origin/main)) { throw 'Main is not synchronized.' }
    $workflow = Get-Content .github/workflows/release.yml -Raw
    if ($workflow -notmatch 'publish_distribution.py upload') { throw 'Reviewed production workflow is not active.' }
    $changelog = Get-Content CHANGELOG.md -Raw
    if ($changelog.Contains("## [$Version]")) { throw 'Version already has changelog history.' }
    git switch -c "codex/release-$Version"
    if ($LASTEXITCODE -ne 0) { throw 'Release branch creation failed.' }
    if ($Target) {
        if (-not ($ClientRoot -and $ChildWorktrees -and $Notes -and $Basis)) { throw 'Client, exact child checkouts, notes and owner authorization basis required.' }
        python -B scripts/release_manifest.py prepare --target $Target --version $Version --sources-root $SourcesRoot --client-root $ClientRoot --notes $Notes --basis $Basis
        if ($LASTEXITCODE -ne 0) { throw 'Release selection preparation failed.' }
        python -B scripts/validate_release.py --version $Version --sources-root $SourcesRoot --child-worktrees $ChildWorktrees --output (Join-Path $repo ('.release/selected-' + [guid]::NewGuid().ToString('N')))
        if ($LASTEXITCODE -ne 0) { throw 'Selected release validation failed.' }
        git add -- "distribution/releases/$Version"
        git commit -m "Prepare Apogee $Target $Version"
        if ($LASTEXITCODE -ne 0) { throw 'Preparation commit failed.' }
        Write-Host 'Selected release prepared. Review through a PR; obtain final tag approval after hosted checks.'
        return
    }
    $updated = $changelog.Replace('## [Unreleased]', "## [Unreleased]`n`n## [$Version] - $((Get-Date).ToString('yyyy-MM-dd'))")
    [IO.File]::WriteAllText((Join-Path $repo 'CHANGELOG.md'), $updated.Replace("`r`n","`n"))
    $lockPath = Join-Path $repo 'distribution/candidate.lock.json'
    $lock = Get-Content $lockPath -Raw | ConvertFrom-Json
    $lock.version = $Version
    [IO.File]::WriteAllText($lockPath, (($lock | ConvertTo-Json -Depth 30) + "`n").Replace("`r`n","`n"))
    $tocPath = Join-Path $repo 'ApogeePartyHealthBars.toc'
    $toc = [regex]::Replace((Get-Content $tocPath -Raw), '(?m)^## Version:.*$', "## Version: $Version")
    [IO.File]::WriteAllText($tocPath, $toc.Replace("`r`n","`n"))
    & ./scripts/test-local.ps1 -SourcesRoot $SourcesRoot
    if ($LASTEXITCODE -ne 0) { throw 'Local validation failed.' }
    git diff --check
    if ($LASTEXITCODE -ne 0) { throw 'Whitespace validation failed.' }
    git add CHANGELOG.md distribution/candidate.lock.json ApogeePartyHealthBars.toc
    git commit -m "Prepare Apogee Forever $Version"
    if ($LASTEXITCODE -ne 0) { throw 'Preparation commit failed.' }
    Write-Host 'Preparation committed. Integrate through a PR, then wait for all hosted checks. No tag or release was published.'
} finally { Pop-Location }
