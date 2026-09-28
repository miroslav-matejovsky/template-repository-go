# Installs this extension into the user's VS Code by linking it into ~/.vscode/extensions.
#
# VS Code does not load extensions from a workspace .vscode/extensions folder, so a directory
# junction (no admin rights needed) points the user extensions folder at this source folder.
# Edits here take effect after "Developer: Reload Window". Re-running replaces the existing link.

$ErrorActionPreference = "Stop"

$manifest = Get-Content (Join-Path $PSScriptRoot "package.json") -Raw | ConvertFrom-Json
$name = "$($manifest.publisher).$($manifest.name)-$($manifest.version)"
$target = Join-Path $HOME ".vscode/extensions/$name"

if (Test-Path $target) {
  $item = Get-Item $target -Force
  if (-not $item.LinkType) { throw "$target exists and is not a link, remove it manually" }
  $item.Delete()
}

New-Item -ItemType Junction -Path $target -Target $PSScriptRoot | Out-Null
Write-Output "installed $name -> $target, reload VS Code windows to activate"
