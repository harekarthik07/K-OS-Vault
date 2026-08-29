<#
Creates a launcher shortcut for the K-OS Capture Hub.

    .\create_shortcut.ps1              -> Desktop shortcut
    .\create_shortcut.ps1 -Startup     -> also launches at login (recommended)
    .\create_shortcut.ps1 -Remove      -> removes both

Paths are derived from this script's own location, so the vault can live
anywhere and move between machines without editing anything.
#>
param(
    [switch]$Startup,
    [switch]$Remove
)

$ErrorActionPreference = 'Stop'

$ToolsDir   = $PSScriptRoot
$VaultDir   = Split-Path $ToolsDir -Parent
$ScriptPath = Join-Path $ToolsDir 'kos_capture_hub.py'

$DesktopLnk = Join-Path ([Environment]::GetFolderPath('Desktop')) 'K-OS Capture Hub.lnk'
$StartupLnk = Join-Path ([Environment]::GetFolderPath('Startup')) 'K-OS Capture Hub.lnk'

if ($Remove) {
    foreach ($lnk in $DesktopLnk, $StartupLnk) {
        if (Test-Path -LiteralPath $lnk) { Remove-Item -LiteralPath $lnk -Force; "removed  $lnk" }
    }
    return
}

if (-not (Test-Path -LiteralPath $ScriptPath)) {
    throw "kos_capture_hub.py not found in $ToolsDir. Keep this script next to it."
}

# pythonw.exe runs the GUI without leaving a console window behind.
$Pythonw = $null
$cmd = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if ($cmd) {
    $Pythonw = $cmd.Source
} else {
    $py = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($py) {
        $candidate = Join-Path (Split-Path $py.Source -Parent) 'pythonw.exe'
        if (Test-Path -LiteralPath $candidate) { $Pythonw = $candidate }
    }
}
if (-not $Pythonw) {
    # The py launcher knows where the real interpreter lives even when PATH doesn't.
    $listed = & py -0p 2>$null | Select-String -Pattern '([A-Za-z]:\\.*python\.exe)' | Select-Object -First 1
    if ($listed) {
        $candidate = $listed.Matches[0].Groups[1].Value -replace 'python\.exe$', 'pythonw.exe'
        if (Test-Path -LiteralPath $candidate) { $Pythonw = $candidate }
    }
}
if (-not $Pythonw) { throw "Could not locate pythonw.exe. Install Python or put it on PATH." }

function New-Lnk($Path, $Label) {
    $shell = New-Object -ComObject WScript.Shell
    $s = $shell.CreateShortcut($Path)
    $s.TargetPath       = $Pythonw
    $s.Arguments        = "`"$ScriptPath`""
    $s.WorkingDirectory = $VaultDir
    $s.Description      = 'K-OS Capture Hub - Ctrl+Alt+K to capture'
    $s.Save()
    "created  $Label"
    "         $Path"
}

New-Lnk $DesktopLnk 'Desktop shortcut'
if ($Startup) { New-Lnk $StartupLnk 'Startup shortcut (launches at login)' }

""
"python : $Pythonw"
"script : $ScriptPath"
"vault  : $VaultDir"
