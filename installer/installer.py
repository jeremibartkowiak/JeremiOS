import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import sys
import winshell
from win32com.client import Dispatch
import json


class JeremiOSInstaller:
    def __init__(self, root):
        self.root = root
        self.root.title("JeremiOS Installer")
        self.root.geometry("600x500")
        self.root.resizable(False, False)

        # Set installer variables
        self.install_dir = os.path.join(os.path.expanduser("~"), "Documents", "JeremiOS")
        self.create_start_menu_shortcut = tk.BooleanVar(value=True)
        self.create_desktop_shortcut = tk.BooleanVar(value=True)
        self.install_wallpapers = tk.BooleanVar(value=True)
        self.install_apps = tk.BooleanVar(value=True)

        # Get the directory where the installer is located
        if getattr(sys, 'frozen', False):
            self.installer_dir = os.path.dirname(sys.executable)
        else:
            self.installer_dir = os.path.dirname(os.path.abspath(__file__))

        self.installer_data_dir = os.path.join(self.installer_dir, "installerdata")

        self.setup_ui()

    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="JeremiOS Installer", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Step 1: Installation Directory
        step1_frame = ttk.LabelFrame(main_frame, text="Step 1: Installation Directory", padding="10")
        step1_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Label(step1_frame, text="Install JeremiOS to:").grid(row=0, column=0, sticky=tk.W)

        dir_frame = ttk.Frame(step1_frame)
        dir_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(5, 0))

        self.dir_entry = ttk.Entry(dir_frame, width=50)
        self.dir_entry.insert(0, self.install_dir)
        self.dir_entry.grid(row=0, column=0, sticky=(tk.W, tk.E))

        ttk.Button(dir_frame, text="Browse", command=self.browse_directory).grid(row=0, column=1, padx=(5, 0))

        dir_frame.columnconfigure(0, weight=1)

        # Step 2: Shortcuts
        step2_frame = ttk.LabelFrame(main_frame, text="Step 2: Create Shortcuts", padding="10")
        step2_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 10))

        ttk.Checkbutton(step2_frame, text="Create Start Menu shortcut",
                        variable=self.create_start_menu_shortcut).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(step2_frame, text="Create Desktop shortcut",
                        variable=self.create_desktop_shortcut).grid(row=1, column=0, sticky=tk.W)

        # Step 3: Additional Components
        step3_frame = ttk.LabelFrame(main_frame, text="Step 3: Additional Components", padding="10")
        step3_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        ttk.Checkbutton(step3_frame, text="Install Extra Wallpapers",
                        variable=self.install_wallpapers).grid(row=0, column=0, sticky=tk.W)
        ttk.Checkbutton(step3_frame, text="Install Additional Apps",
                        variable=self.install_apps).grid(row=1, column=0, sticky=tk.W)

        # Progress bar
        self.progress = ttk.Progressbar(main_frame, orient=tk.HORIZONTAL, length=560, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=2, pady=(0, 10))

        # Status label
        self.status_label = ttk.Label(main_frame, text="Ready to install...")
        self.status_label.grid(row=5, column=0, columnspan=2, pady=(0, 10))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=6, column=0, columnspan=2)

        ttk.Button(button_frame, text="Install", command=self.start_installation).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(button_frame, text="Cancel", command=self.root.quit).grid(row=0, column=1)

        main_frame.columnconfigure(0, weight=1)

    def browse_directory(self):
        directory = filedialog.askdirectory(initialdir=self.install_dir)
        if directory:
            self.install_dir = directory
            self.dir_entry.delete(0, tk.END)
            self.dir_entry.insert(0, directory)

    def update_status(self, message, progress=None):
        self.status_label.config(text=message)
        if progress is not None:
            self.progress['value'] = progress
        self.root.update_idletasks()

    def copy_directory(self, src, dst):
        """Copy directory recursively with better error handling"""
        try:
            print(f"Copying directory: {src} -> {dst}")  # Debug
            if os.path.exists(dst):
                shutil.rmtree(dst)
            shutil.copytree(src, dst)
            print(f"Successfully copied: {src} -> {dst}")  # Debug
            return True
        except Exception as e:
            print(f"Error copying directory {src} to {dst}: {e}")  # Debug
            return False

    def create_shortcut(self, target, shortcut_path, description):
        """Create Windows shortcut"""
        try:
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.Description = description
            shortcut.save()
            return True
        except Exception as e:
            print(f"Error creating shortcut: {e}")
            return False

    def start_installation(self):
        # Validate installation directory
        self.install_dir = self.dir_entry.get().strip()
        if not self.install_dir:
            messagebox.showerror("Error", "Please select an installation directory")
            return

        # Confirm installation
        result = messagebox.askyesno("Confirm Installation",
                                     f"JeremiOS will be installed to:\n{self.install_dir}\n\nProceed with installation?")
        if not result:
            return

        # Start installation process
        try:
            self.perform_installation()
        except Exception as e:
            messagebox.showerror("Installation Error", f"An error occurred during installation:\n{str(e)}")

    def perform_installation(self):
        total_steps = 4
        current_step = 0

        # Step 1: Create installation directory
        current_step += 1
        self.update_status("Creating installation directory...", (current_step / total_steps) * 100)

        os.makedirs(self.install_dir, exist_ok=True)

        # Step 2: Copy main executable
        current_step += 1
        self.update_status("Copying main application...", (current_step / total_steps) * 100)

        # Copy W10JeremiOS.exe from installerdata directory
        source_exe = os.path.join(self.installer_data_dir, "W10JeremiOS.exe")

        if os.path.exists(source_exe):
            target_exe = os.path.join(self.install_dir, "W10JeremiOS.exe")
            shutil.copy2(source_exe, target_exe)
        else:
            messagebox.showerror("Error",
                                 "W10JeremiOS.exe not found in installerdata folder. Installation cannot continue.")
            return

        # Step 3: Copy additional components
        current_step += 1
        self.update_status("Installing additional components...", (current_step / total_steps) * 100)

        my_python_os_dir = os.path.join(self.install_dir, "MyPythonOS")

        # Create MyPythonOS directory structure
        os.makedirs(os.path.join(my_python_os_dir, "Home"), exist_ok=True)
        os.makedirs(os.path.join(my_python_os_dir, "System"), exist_ok=True)

        # Copy wallpapers if selected - FIXED LOGIC
        if self.install_wallpapers:
            wallpapers_src = os.path.join(self.installer_data_dir, "images")
            wallpapers_dst = os.path.join(my_python_os_dir, "System", "images")

            print(f"Looking for wallpapers at: {wallpapers_src}")  # Debug
            print(f"Wallpapers exist: {os.path.exists(wallpapers_src)}")  # Debug

            if os.path.exists(wallpapers_src):
                try:
                    self.copy_directory(wallpapers_src, wallpapers_dst)
                    print(f"Wallpapers copied to: {wallpapers_dst}")  # Debug
                except Exception as e:
                    print(f"Error copying wallpapers: {e}")  # Debug
            else:
                print("Wallpapers source directory not found!")  # Debug

        # Copy apps if selected - FIXED LOGIC
        if self.install_apps:
            apps_src = os.path.join(self.installer_data_dir, "apps")
            apps_dst = os.path.join(my_python_os_dir, "Home", "apps")

            print(f"Looking for apps at: {apps_src}")  # Debug
            print(f"Apps exist: {os.path.exists(apps_src)}")  # Debug

            if os.path.exists(apps_src):
                try:
                    self.copy_directory(apps_src, apps_dst)
                    print(f"Apps copied to: {apps_dst}")  # Debug
                except Exception as e:
                    print(f"Error copying apps: {e}")  # Debug
            else:
                print("Apps source directory not found!")  # Debug

        # Copy MyPythonOS content if exists - IMPROVED LOGIC
        my_python_os_src = os.path.join(self.installer_data_dir, "MyPythonOS")
        print(f"Looking for MyPythonOS at: {my_python_os_src}")  # Debug
        print(f"MyPythonOS exists: {os.path.exists(my_python_os_src)}")  # Debug

        if os.path.exists(my_python_os_src):
            try:
                # Copy the entire MyPythonOS directory structure
                for root, dirs, files in os.walk(my_python_os_src):
                    for file in files:
                        src_file = os.path.join(root, file)
                        # Calculate relative path to maintain directory structure
                        rel_path = os.path.relpath(src_file, my_python_os_src)
                        dst_file = os.path.join(my_python_os_dir, rel_path)

                        # Create destination directory if it doesn't exist
                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        print(f"Copied: {src_file} -> {dst_file}")  # Debug
            except Exception as e:
                print(f"Error copying MyPythonOS: {e}")  # Debug

        # Step 4: Create shortcuts
        current_step += 1
        self.update_status("Creating shortcuts...", (current_step / total_steps) * 100)

        target_exe = os.path.join(self.install_dir, "W10JeremiOS.exe")

        if self.create_start_menu_shortcut:
            try:
                start_menu_dir = os.path.join(winshell.start_menu(), "Programs", "JeremiOS")
                os.makedirs(start_menu_dir, exist_ok=True)
                shortcut_path = os.path.join(start_menu_dir, "JeremiOS.lnk")
                self.create_shortcut(target_exe, shortcut_path, "JeremiOS")
            except Exception as e:
                print(f"Failed to create Start Menu shortcut: {e}")

        if self.create_desktop_shortcut:
            try:
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "JeremiOS.lnk")
                self.create_shortcut(target_exe, shortcut_path, "JeremiOS")
            except Exception as e:
                print(f"Failed to create Desktop shortcut: {e}")

        # Final step
        self.update_status("Installation complete!", 100)

        # Save installation settings
        settings = {
            'install_dir': self.install_dir,
            'start_menu_shortcut': self.create_start_menu_shortcut.get(),
            'desktop_shortcut': self.create_desktop_shortcut.get(),
            'wallpapers_installed': self.install_wallpapers.get(),
            'apps_installed': self.install_apps.get()
        }

        settings_file = os.path.join(self.install_dir, "install_settings.json")
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

        # Show debug info
        debug_info = f"Installation completed!\n\nInstallation directory: {self.install_dir}\n"

        # Check what was actually installed
        if os.path.exists(os.path.join(my_python_os_dir, "System", "images")):
            debug_info += "✓ Wallpapers installed\n"
        else:
            debug_info += "✗ Wallpapers NOT installed\n"

        if os.path.exists(os.path.join(my_python_os_dir, "Home", "apps")):
            debug_info += "✓ Apps installed\n"
        else:
            debug_info += "✗ Apps NOT installed\n"

        if os.path.exists(my_python_os_dir):
            debug_info += "✓ MyPythonOS structure created\n"

        messagebox.showinfo("Installation Complete", debug_info)

        # Step 4: Create shortcuts
        current_step += 1
        self.update_status("Creating shortcuts...", (current_step / total_steps) * 100)

        target_exe = os.path.join(self.install_dir, "W10JeremiOS.exe")

        if self.create_start_menu_shortcut:
            try:
                start_menu_dir = os.path.join(winshell.start_menu(), "Programs", "JeremiOS")
                os.makedirs(start_menu_dir, exist_ok=True)
                shortcut_path = os.path.join(start_menu_dir, "JeremiOS.lnk")
                self.create_shortcut(target_exe, shortcut_path, "JeremiOS")
            except Exception as e:
                print(f"Failed to create Start Menu shortcut: {e}")

        if self.create_desktop_shortcut:
            try:
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "JeremiOS.lnk")
                self.create_shortcut(target_exe, shortcut_path, "JeremiOS")
            except Exception as e:
                print(f"Failed to create Desktop shortcut: {e}")

        # Final step
        self.update_status("Installation complete!", 100)

        # Save installation settings
        settings = {
            'install_dir': self.install_dir,
            'start_menu_shortcut': self.create_start_menu_shortcut.get(),
            'desktop_shortcut': self.create_desktop_shortcut.get(),
            'wallpapers_installed': self.install_wallpapers.get(),
            'apps_installed': self.install_apps.get()
        }

        settings_file = os.path.join(self.install_dir, "install_settings.json")
        with open(settings_file, 'w') as f:
            json.dump(settings, f, indent=4)

        messagebox.showinfo("Installation Complete",
                            f"JeremiOS has been successfully installed to:\n{self.install_dir}\n\n"
                            f"You can now run W10JeremiOS.exe from the installation directory.")


def main():
    root = tk.Tk()
    app = JeremiOSInstaller(root)
    root.mainloop()


if __name__ == "__main__":
    main()