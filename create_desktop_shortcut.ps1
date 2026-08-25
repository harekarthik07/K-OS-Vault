$DesktopPath = [System.IO.Path]::Combine($env:USERPROFILE, "Desktop")
$ShortcutPath = [System.IO.Path]::Combine($DesktopPath, "K-OS Capture Hub.lnk")
$PythonwPath = "C:\Users\sonic\AppData\Local\Programs\Python\Python312\pythonw.exe"
$ScriptPath = "d:\2nd Brain\K-OS - Thinking Visualized\kos_capture_hub.py"
$WorkingDir = "d:\2nd Brain\K-OS - Thinking Visualized"

$WshShell = New-Object -ComObject WScript.Shell
$Shortcut = $WshShell.CreateShortcut($ShortcutPath)
$Shortcut.TargetPath = $PythonwPath
$Shortcut.Arguments = "`"$ScriptPath`""
$Shortcut.WorkingDirectory = $WorkingDir
$Shortcut.Description = "K-OS Thinking Visualized Capture Hub"
$Shortcut.Save()

Write-Output "Desktop shortcut created successfully at: $ShortcutPath"
