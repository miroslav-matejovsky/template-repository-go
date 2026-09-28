# Installs this extension into the user's VS Code by copying it into ~/.vscode/extensions.
#
# VS Code does not load extensions from a workspace .vscode/extensions folder, so the runtime
# files are copied into the user extensions folder. The copied set is the same one vsce packages:
# package.json, README.md and the entries of the "files" list in package.json.
# Re-run after every change, then run "Developer: Reload Window". Re-running replaces the existing
# install, including an older junction-based install.

$ErrorActionPreference = "Stop"

$manifest = Get-Content (Join-Path $PSScriptRoot "package.json") -Raw | ConvertFrom-Json
$name = "$($manifest.publisher).$($manifest.name)-$($manifest.version)"
$target = Join-Path $HOME ".vscode/extensions/$name"

if (Test-Path $target) {
  $item = Get-Item $target -Force
  # A junction must be removed as a link, recursive removal would delete the source folder.
  if ($item.LinkType) { $item.Delete() } else { Remove-Item $target -Recurse -Force }
}

New-Item -ItemType Directory -Path $target | Out-Null
foreach ($file in @("package.json", "README.md") + $manifest.files) {
  Copy-Item (Join-Path $PSScriptRoot $file) -Destination $target -Recurse
}
Write-Output "installed $name -> $target, reload VS Code windows to activate"
