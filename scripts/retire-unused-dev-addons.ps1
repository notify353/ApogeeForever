[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ClientRoot,
    [Parameter(Mandatory)][string]$PreviousInstall,
    [Parameter(Mandatory)][string]$Backup
)
$ErrorActionPreference = 'Stop'
$names = @('ApogeeTankDev', 'ApogeeAuctionDev')
$client = (Resolve-Path -LiteralPath $ClientRoot).Path
$addons = (Resolve-Path -LiteralPath (Join-Path $client 'Interface/AddOns')).Path
$destination = [IO.Path]::GetFullPath($Backup)
if (Test-Path -LiteralPath $destination) { throw 'Use a new backup directory.' }
if ($destination.StartsWith($client + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
    throw 'Backup must be outside the game client.'
}
$receipt = Get-Content -LiteralPath $PreviousInstall -Raw | ConvertFrom-Json -AsHashtable
if ($receipt.schema -ne 1 -or $receipt.status -ne 'installed' -or [IO.Path]::GetFullPath($receipt.client) -ne $client) {
    throw 'A verified installation receipt for this client is required.'
}
function Read-AddonHashes([string]$Root) {
    $hashes = @{}
    foreach ($item in Get-ChildItem -LiteralPath $Root -Recurse -Force) {
        if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse points are not allowed.' }
        if (-not $item.PSIsContainer) {
            $relative = [IO.Path]::GetRelativePath($Root, $item.FullName).Replace('\', '/')
            $hashes[$relative] = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    return $hashes
}
$inventory = @{}
foreach ($name in $names) {
    $source = Join-Path $addons $name
    if (-not (Test-Path -LiteralPath $source)) { continue }
    $item = Get-Item -LiteralPath $source -Force
    if (-not $item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -or
        (Resolve-Path -LiteralPath $source).Path -ne [IO.Path]::GetFullPath($source)) { throw 'Unsafe addon path.' }
    $hashes = Read-AddonHashes $source
    foreach ($relative in $hashes.Keys) {
        if ($relative -match '\.(lua|toc)$' -and $receipt.after["$name/$relative"] -ne $hashes[$relative]) {
            throw "Unexpected runtime edit: $name/$relative"
        }
    }
    $inventory[$name] = $hashes
}
if (-not $inventory.Count) { throw 'Neither retired DEV addon is installed.' }
New-Item -ItemType Directory -Path $destination | Out-Null
$journal = @{schema=1;client=$client;status='prepared';addons=$inventory;moved=@()}
$journalPath = Join-Path $destination 'retirement.json'
$journal | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $journalPath
foreach ($name in $names) {
    if (-not $inventory.ContainsKey($name)) { continue }
    $source = [IO.Path]::GetFullPath((Join-Path $addons $name))
    $target = [IO.Path]::GetFullPath((Join-Path $destination $name))
    if ([IO.Path]::GetDirectoryName($source) -ne $addons -or
        [IO.Path]::GetDirectoryName($target) -ne $destination) { throw 'Path escaped intended directory.' }
    $current = Read-AddonHashes $source
    if ($current.Count -ne $inventory[$name].Count) { throw 'Addon changed during review.' }
    foreach ($p in $current.Keys) { if ($current[$p] -ne $inventory[$name][$p]) { throw 'Addon changed during review.' } }
    Move-Item -LiteralPath $source -Destination $target
    $journal.moved += $name
    $journal.status = 'in-progress'
    $journal | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $journalPath
    $verified = Read-AddonHashes $target
    if ($verified.Count -ne $current.Count) { throw 'Backup verification failed; preserve backup.' }
    foreach ($p in $current.Keys) { if ($verified[$p] -ne $current[$p]) { throw 'Backup verification failed; preserve backup.' } }
}
$journal.status = 'retired'
$journal | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $journalPath
Write-Host ('Retired to verified backup: ' + ($journal.moved -join ', '))
Write-Host 'Restart WoW yourself to unload removed addons and refresh addon discovery.'
