# JeremiOS - Python Desktop Environment 🖥️

**JeremiOS** is a custom desktop environment built entirely with Python and Tkinter, mimicking a full operating system experience with a modern UI and practical applications.

## 🚀 Key Features

### Desktop Environment
- **Customizable Desktop**: Change background colors or set custom images
- **Icon Management**: Add, remove, and organize desktop icons with custom colors
- **Fullscreen Support**: Toggle between windowed and fullscreen modes
- **Grid-based Icon Layout**: Automatic organization of desktop icons
- **Context Menu**: Right-click for quick actions

### Built-in Applications
- **File Explorer**: Navigate through directories, create files/folders, delete items
- **Text Editor**: Full-featured editor with syntax highlighting support and Ctrl+S save functionality
- **Terminal**: Python code execution with separate output and error windows (Shift+F10 to run)
- **Settings Panel**: Customize resolution and display preferences

### System Features
- **Persistent Settings**: Automatically saves preferences, icons, and background settings
- **Reminder System**: Friendly pop-up reminders every 2 minutes for health and productivity
- **Application Launcher**: Execute Python scripts (.py), executables (.exe), and other applications from desktop icons
- **Protected System Folders**: Prevents accidental deletion of critical directories
- **App Integration**: Seamlessly launch apps via desktop icons

## 🛠️ Technical Architecture

- **Framework**: Built with Tkinter for the GUI
- **File Management**: Custom file explorer with directory navigation
- **Process Execution**: Uses subprocess for running external applications
- **Image Handling**: PIL/Pillow for background image processing
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **App Ecosystem**: Extensible through the `apps/` directory

## 📁 Project Structure
```
JeremiOS/
├── W10JeremiOS.py # Main desktop environment
├── apps/ # Apps
├── MyPythonOS/ # User workspace
│ ├── System/ # OS configuration files
│ └── Home/ # User documents and files
└── .gitignore # Development environment exclusions
```

## 🎯 Launching Applications

### Via Desktop Icons
1. **Copy** apps from the apps folder to anywhere in `MyPythonOS/Home/`
2. **Right-click** on desktop → **"Add Icon"**
3. **Select** any `.py` or `.exe` file
4. **Choose** a name and color for your icon
5. **Click** the icon to launch the application

## 🚀 Getting Started

1. **Go to the [Releases](https://github.com/jeremibartkowiak/JeremiOS/releases) page**
2. **Download the latest installer ZIP**
3. **Extract the ZIP**
4. **Run `JeremiOS_Installer.exe`** and follow the setup steps
5. **Launch JeremiOS** from your desktop or start menu

### Quick Start Guide
1. Run the main script to launch the desktop
2. Use the toolbar at the bottom to access applications
3. Right-click on desktop → "Add Icon" to add apps from the `apps/` folder
4. Click desktop icons to launch your applications
5. Press F11 for fullscreen mode

## 🎨 Customization

- **Backgrounds**: Choose colors or images via Customize menu
- **Icons**: Add any `.py` or `.exe` file with custom colors
- **Resolution**: Adjust screen size in Settings

## 🔧 App Development

### Adding New Apps
1. Place your `.py` scripts anywhere in the `MyPythonOS/` folder
2. Use desktop icons to make them easily accessible
3. Apps can use any Python framework (Tkinter, PyQt6, etc.)