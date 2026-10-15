Option Explicit
Dim word, fs, folder, file, doc, pdf
Set fs = CreateObject("Scripting.FileSystemObject")
Set word = CreateObject("Word.Application")
word.Visible = False
word.DisplayAlerts = 0
Set folder = fs.GetFolder(WScript.Arguments(0))
For Each file In folder.Files
  If LCase(fs.GetExtensionName(file.Name)) = "docx" Then
    Set doc = word.Documents.Open(file.Path, False, True)
    doc.Repaginate
    pdf = fs.BuildPath(folder.Path, fs.GetBaseName(file.Name) & ".pdf")
    doc.ExportAsFixedFormat pdf, 17
    WScript.Echo file.Name & " pages=" & doc.ComputeStatistics(2)
    doc.Close False
  End If
Next
word.Quit
