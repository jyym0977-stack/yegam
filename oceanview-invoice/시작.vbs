Dim objShell, objFSO, strDir

Set objFSO = CreateObject("Scripting.FileSystemObject")
Set objShell = CreateObject("WScript.Shell")

' 이 파일이 있는 폴더 경로
strDir = objFSO.GetParentFolderName(WScript.ScriptFullName)

' 서버 시작 (CMD 창 숨김)
objShell.CurrentDirectory = strDir
objShell.Run "cmd /c node server.js", 0, False

' 2초 대기 후 Chrome 열기
WScript.Sleep 2000
objShell.Run "chrome http://localhost:3000", 1, False

Set objShell = Nothing
Set objFSO = Nothing
