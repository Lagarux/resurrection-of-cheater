[Setup]
; Uygulama Bilgileri
AppName=Resurrection of Cheater
AppVersion=1.0
AppPublisher=Karamanoğlu Mehmetbey Üniversitesi - Bilgisayar Mühendisliği
DefaultDirName={autopf}\ResurrectionOfCheater
DefaultGroupName=ResurrectionOfCheater
UninstallDisplayIcon={app}\ResurrectionOfCheater.exe
Compression=lzma2/ultra64
SolidCompression=yes
OutputDir=.\InstallerOutput
SetupIconFile=D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\assets\RoC.ico

[Files]
; 1. PyInstaller Çıktıları (dist klasörü)
Source: "D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\dist\ResurrectionOfCheater\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

; 2. Tesseract-OCR Klasörü (Dışarıdan dahil ediyoruz)
Source: "D:\SoftwareTechs\Python_Projects\resurrection-of-cheater\Tesseract-OCR\*"; DestDir: "{app}\Tesseract-OCR"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; Masaüstü ve Başlat Menüsü Kısayolları
Name: "{group}\Resurrection of Cheater"; Filename: "{app}\ResurrectionOfCheater.exe"
Name: "{commondesktop}\Resurrection of Cheater"; Filename: "{app}\ResurrectionOfCheater.exe"; IconFilename: "{app}\ResurrectionOfCheater.exe"

[Run]
; Kurulum bittiğinde çalıştırma seçeneği
Filename: "{app}\ResurrectionOfCheater.exe"; Description: "Uygulamayı Hemen Başlat"; Flags: nowait postinstall skipifsilent