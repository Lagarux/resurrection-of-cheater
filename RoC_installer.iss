[Setup]
AppName=Resurrection of Cheater
AppVersion=1.0
AppPublisher=FTG
DefaultDirName={autopf}\ResurrectionOfCheater
DefaultGroupName=ResurrectionOfCheater
UninstallDisplayIcon={app}\ResurrectionOfCheater.exe
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir=.\InstallerOutput
SetupIconFile=D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\assets\RoC.ico

[Files]
; Derlenmiş ana uygulama
Source: "D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\dist\ResurrectionOfCheater\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; Tesseract Bağımlılığı (Hiyerarşiyi bozmadan ekliyoruz)
Source: "D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\Tesseract-OCR\*"; DestDir: "{app}\Tesseract-OCR"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Resurrection of Cheater"; Filename: "{app}\ResurrectionOfCheater.exe"
Name: "{commondesktop}\Resurrection of Cheater"; Filename: "{app}\ResurrectionOfCheater.exe"

[Run]
Filename: "{app}\ResurrectionOfCheater.exe"; Description: "Uygulamayı Başlat"; Flags: nowait postinstall skipifsilent