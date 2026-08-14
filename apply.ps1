[CmdletBinding()]
param(
    [switch]$Global
)

$ErrorActionPreference = 'Stop'
$HarnessDir = $PSScriptRoot

function Backup-IfExists {
    param([Parameter(Mandatory)][string]$Path)

    $item = Get-Item -Force -LiteralPath $Path -ErrorAction SilentlyContinue
    if ($null -eq $item) {
        return
    }

    if ($item.LinkType) {
        Remove-Item -Force -LiteralPath $Path
        return
    }

    $backup = '{0}.bak.{1}' -f $Path, (Get-Date -Format 'yyyyMMdd-HHmmssfff')
    Move-Item -LiteralPath $Path -Destination $backup
    Write-Output "backup: $Path -> $backup"
}

function Link-Path {
    param(
        [Parameter(Mandatory)][string]$Source,
        [Parameter(Mandatory)][string]$Target
    )

    Backup-IfExists -Path $Target

    try {
        New-Item -ItemType SymbolicLink -Path $Target -Target $Source | Out-Null
        $linkType = 'symbolic link'
    }
    catch {
        $existing = Get-Item -Force -LiteralPath $Target -ErrorAction SilentlyContinue
        if ($null -ne $existing) {
            Remove-Item -Force -LiteralPath $Target
        }

        $sourceItem = Get-Item -Force -LiteralPath $Source
        $fallbackType = if ($sourceItem.PSIsContainer) { 'Junction' } else { 'HardLink' }
        New-Item -ItemType $fallbackType -Path $Target -Target $Source | Out-Null
        $linkType = $fallbackType.ToLowerInvariant()
    }

    Write-Output "linked ($linkType): $Target -> $Source"
}

function Install-Global {
    $userProfile = [Environment]::GetFolderPath('UserProfile')
    if ([string]::IsNullOrWhiteSpace($userProfile)) {
        throw 'Could not resolve the Windows user profile directory.'
    }

    $codexDir = Join-Path $userProfile '.codex'
    $agentDir = Join-Path $codexDir 'agents'
    $skillDir = Join-Path $userProfile '.agents\skills'
    New-Item -ItemType Directory -Force -Path $agentDir, $skillDir | Out-Null

    Link-Path -Source (Join-Path $HarnessDir 'AGENTS.md') -Target (Join-Path $codexDir 'AGENTS.md')

    Get-ChildItem -Directory -LiteralPath (Join-Path $HarnessDir 'skills') | ForEach-Object {
        if (Test-Path -LiteralPath (Join-Path $_.FullName 'SKILL.md')) {
            Link-Path -Source $_.FullName -Target (Join-Path $skillDir $_.Name)
        }
    }

    Get-ChildItem -File -Filter '*.toml' -LiteralPath (Join-Path $HarnessDir 'agents') | ForEach-Object {
        Link-Path -Source $_.FullName -Target (Join-Path $agentDir $_.Name)
    }

    Write-Output 'done. restart Codex and invoke $harness'
}

if (-not $Global) {
    Write-Output 'usage: ./apply.ps1 -Global'
    exit 1
}

Install-Global
