Set oShell = CreateObject ("Wscript.Shell")

Dim strArgs

strArgs = "cmd /c FacialSymmetryAnalysis.bat"

oShell.Run strArgs, 0, false