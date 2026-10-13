#define MyAppName "FRIDEY"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "FRIDEY"
#define MyAppExeName "FRIDEY.exe"

[Setup]
AppId={{D9B0C46D-6A62-4D2B-96A6-47B8F65B91C1}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\FRIDEY
DefaultGroupName=FRIDEY
DisableProgramGroupPage=yes
OutputDir=..\..\ai-service\dist
OutputBaseFilename=FRIDEY-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=admin
UninstallDisplayIcon={app}\FRIDEY.exe

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional shortcuts:"; Flags: unchecked

[Files]
Source: "..\..\ai-service\dist\FRIDEY.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\FRIDEY"; Filename: "{app}\FRIDEY.exe"
Name: "{group}\FRIDEY Voice Assistant"; Filename: "{app}\FRIDEY.exe"; Parameters: "--voice"
Name: "{autodesktop}\FRIDEY"; Filename: "{app}\FRIDEY.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\FRIDEY.exe"; Description: "Launch FRIDEY"; Flags: postinstall nowait skipifsilent
