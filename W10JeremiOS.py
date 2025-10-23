import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog, colorchooser
import os
import shutil
import sys
import io
import subprocess
from PIL import Image, ImageTk
import random
import time


class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("My Python OS Desktop")

        # Define working directory before loading settings
        self.working_directory = os.path.join(os.getcwd(), 'MyPythonOS')
        self.current_directory = self.working_directory
        self.current_directory = self.working_directory

        # Ensure essential directories exist before loading settings
        os.makedirs(os.path.join(self.working_directory, 'System'), exist_ok=True)
        os.makedirs(os.path.join(self.working_directory, 'Home'), exist_ok=True)

        # Reminder messages
        self.reminder_messages = [
            "Friendly reminder: You're doing great!",
            "Don't forget to save your work!",
            "Remember to blink occasionally!",
            "Hydration check: Have you had water recently?",
            "Stretch break time! Your back will thank you.",
            "Pro tip: Ctrl+S is your best friend!",
            "This is not a real OS... or is it? 🤔",
            "Did you know: This was made with Python!",
            "Warning: Excessive coding may cause awesomeness.",
            "Just checking: Are you having fun yet?"
        ]

        # Load settings
        self.load_settings()

        # Initialize variables that depend on loaded settings
        # Fullscreen mode variable
        self.fullscreen_var = tk.BooleanVar(value=self.is_fullscreen)

        # Configure root window
        self.root.geometry(f"{self.screen_width}x{self.screen_height}")
        self.root.resizable(False, False)

        # Set fullscreen mode if enabled
        if self.is_fullscreen:
            self.root.attributes('-fullscreen', True)
        else:
            self.root.attributes('-fullscreen', False)

        # Initialize background
        self.background_label = None
        self.init_background()

        self.icons = []
        self.remove_icon_mode = False

        # Icon placement configuration
        self.icon_width = 80
        self.icon_height = 80
        self.icon_padding_x = 20
        self.icon_padding_y = 20
        self.icons_per_row = 10

        # Load icons and create toolbar
        self.load_icons()
        self.create_toolbar()

        # Bind right-click to show context menu
        self.root.bind("<Button-3>", self.show_context_menu)

        # Bind F11 to toggle fullscreen
        self.root.bind("<F11>", self.toggle_fullscreen)
        # Bind Escape to exit fullscreen if needed
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Start the reminder system
        self.start_reminders()

    def start_reminders(self):
        """Start showing random reminders every 120 seconds."""
        self.show_reminder()
        self.root.after(120000, self.start_reminders)  # 120,000 ms = 120 seconds

    def show_reminder(self):
        """Show a random reminder message."""
        message = random.choice(self.reminder_messages)
        # Create a non-modal toplevel window
        reminder_window = tk.Toplevel(self.root)
        reminder_window.title("Friendly Reminder")
        reminder_window.geometry("400x100")
        reminder_window.attributes('-topmost', True)

        # Position near the bottom right
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        reminder_window.geometry(f"+{screen_width - 420}+{screen_height - 150}")

        tk.Label(reminder_window, text=message, font=('Arial', 12)).pack(pady=20)
        tk.Button(reminder_window, text="OK", command=reminder_window.destroy).pack(pady=5)

        # Auto-close after 60 seconds if not manually closed
        reminder_window.after(60000, reminder_window.destroy)

    def load_settings(self):
        """Load settings from a file or set defaults."""
        settings_file = os.path.join(self.working_directory, 'System', 'settings.txt')
        # Set default values
        self.screen_width = 800
        self.screen_height = 600
        self.is_fullscreen = False
        self.background_color = "lightblue"
        self.background_image_path = None

        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=', 1)
                    print(f"Loaded setting: {key} = {value}")

        if os.path.exists(settings_file):
            with open(settings_file, 'r') as f:
                for line in f:
                    key, value = line.strip().split('=', 1)
                    if key == 'screen_width':
                        self.screen_width = int(value)
                    elif key == 'screen_height':
                        self.screen_height = int(value)
                    elif key == 'is_fullscreen':
                        self.is_fullscreen = value == 'True'
                    elif key == 'background_color':
                        self.background_color = value
                    elif key == 'background_image_path':
                        # Handle 'None' string
                        self.background_image_path = value if value != 'None' else None

    def save_settings(self):
        """Save settings to a file."""
        settings_file = os.path.join(self.working_directory, 'System', 'settings.txt')
        with open(settings_file, 'w') as f:
            f.write(f"screen_width={self.root.winfo_width()}\n")
            f.write(f"screen_height={self.root.winfo_height()}\n")
            f.write(f"is_fullscreen={self.fullscreen_var.get()}\n")
            f.write(f"background_color={self.background_color}\n")
            # Ensure the background_image_path is saved correctly
            f.write(f"background_image_path={self.background_image_path}\n")

    def init_background(self):
        """Initialize the desktop background."""
        # Create a Frame to hold the background
        self.desktop_frame = tk.Frame(self.root, width=self.screen_width, height=self.screen_height)
        self.desktop_frame.place(x=0, y=0, relwidth=1, relheight=1)

        print(f"Background image path: {self.background_image_path}")  # Debug print

        if self.background_image_path and os.path.exists(self.background_image_path):
            # Load and set background image
            self.set_background_image(self.background_image_path)
        else:
            print(f"Background image not set or not found. Using background color: {self.background_color}")
            # Set background color
            self.desktop_frame.configure(bg=self.background_color)

    def set_background_color(self, color):
        """Set the desktop background color."""
        self.background_color = color
        self.desktop_frame.configure(bg=color)
        self.background_image_path = None  # Remove any background image
        self.save_settings()

    def set_background_image(self, image_path):
        """Set the desktop background image."""
        try:
            # Use the stored screen dimensions
            width = self.screen_width
            height = self.screen_height
            print(f"Using screen dimensions for background image: width={width}, height={height}")

            # Convert to absolute path
            self.background_image_path = os.path.abspath(image_path)
            print(f"Attempting to open background image at: {self.background_image_path}")  # Debug print
            image = Image.open(self.background_image_path)
            image = image.resize((width, height), Image.LANCZOS)
            self.background_image = ImageTk.PhotoImage(image)
            if self.background_label:
                self.background_label.destroy()
            self.background_label = tk.Label(self.desktop_frame, image=self.background_image)
            self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
            self.background_label.lower()  # Ensure background is behind icons
            self.save_settings()
        except Exception as e:
            print(f"Error setting background image: {e}")
            messagebox.showerror("Background Image Error", f"Failed to set background image: {e}")
            # Revert to background color
            if self.background_label:
                self.background_label.destroy()
                self.background_label = None
            self.background_image_path = None
            self.desktop_frame.configure(bg=self.background_color)
            self.save_settings()

    def create_toolbar(self):
        """Create the toolbar with various application buttons."""
        toolbar = tk.Frame(self.root, bg="gray", height=40)
        toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        settings_button = tk.Button(toolbar, text="Settings", command=self.open_settings)
        settings_button.pack(side=tk.LEFT, padx=5, pady=5)

        customize_button = tk.Button(toolbar, text="Customize", command=self.open_customize)
        customize_button.pack(side=tk.LEFT, padx=5, pady=5)

        explorer_button = tk.Button(toolbar, text="File Explorer", command=self.open_explorer)
        explorer_button.pack(side=tk.LEFT, padx=5, pady=5)

        terminal_button = tk.Button(toolbar, text="Terminal", command=self.open_terminal)
        terminal_button.pack(side=tk.LEFT, padx=5, pady=5)

        text_editor_button = tk.Button(toolbar, text="Text Editor", command=self.open_text_editor)
        text_editor_button.pack(side=tk.LEFT, padx=5, pady=5)

    def add_icon(self, path, name, color):
        """Add an icon to the desktop."""
        index = len(self.icons)
        x = self.icon_padding_x + (index % self.icons_per_row) * (self.icon_width + self.icon_padding_x)
        y = self.icon_padding_y + (index // self.icons_per_row) * (self.icon_height + self.icon_padding_y)

        icon_frame = tk.Frame(self.desktop_frame, bg=color, width=self.icon_width, height=self.icon_height)
        icon_frame.pack_propagate(False)
        icon_frame.place(x=x, y=y)

        icon_label = tk.Label(icon_frame, text=name, bg=color, fg="white")
        icon_label.pack(fill=tk.BOTH, expand=True)

        # Bind events
        icon_frame.bind("<Button-1>", lambda event, frame=icon_frame: self.icon_clicked(event, frame))
        icon_label.bind("<Button-1>", lambda event, frame=icon_frame: self.icon_clicked(event, frame))

        # Store the icon data
        self.icons.append((icon_frame, path, name, color))

    def reposition_icons(self):
        """Rearrange icons in a grid layout."""
        for index, (icon_frame, path, name, color) in enumerate(self.icons):
            x = self.icon_padding_x + (index % self.icons_per_row) * (self.icon_width + self.icon_padding_x)
            y = self.icon_padding_y + (index // self.icons_per_row) * (self.icon_height + self.icon_padding_y)
            icon_frame.place_configure(x=x, y=y)

    def save_icons(self):
        """Save the icons' data to a file."""
        icon_data = [(path, name, color) for (icon_frame, path, name, color) in self.icons]
        icons_file = os.path.join(self.working_directory, 'System', 'icons.txt')
        with open(icons_file, 'w', encoding='utf-8') as f:
            for item in icon_data:
                safe_item = [str(element).replace(',', '%2C') for element in item]
                f.write(','.join(safe_item) + '\n')

    def load_icons(self):
        """Load the icons' data from a file."""
        icons_file = os.path.join(self.working_directory, 'System', 'icons.txt')
        if os.path.exists(icons_file):
            with open(icons_file, 'r', encoding='utf-8') as f:
                for line in f:
                    fields = [field.replace('%2C', ',') for field in line.strip().split(',')]
                    if len(fields) == 3:
                        path, name, color = fields
                        self.add_icon(path, name, color)
        self.reposition_icons()

    def show_context_menu(self, event):
        """Show context menu on right-click."""
        context_menu = tk.Menu(self.root, tearoff=0)
        context_menu.add_command(label="Add Icon", command=self.prompt_add_icon)
        context_menu.add_command(label="Remove Icons", command=self.enable_remove_icon_mode)
        context_menu.post(event.x_root, event.y_root)

    def prompt_add_icon(self):
        """Prompt the user to add a new icon."""
        path = filedialog.askopenfilename(title="Select File or App", initialdir=self.working_directory)
        if path:
            name = simpledialog.askstring("Icon Name", "Enter icon name:")
            if name:
                # Use color chooser instead of typing color name
                color = colorchooser.askcolor(title="Choose Icon Color")[1]
                if color:
                    self.add_icon(path, name, color)
                    self.save_icons()

    def enable_remove_icon_mode(self):
        """Enable icon removal mode."""
        response = messagebox.askokcancel(
            "Remove Icons",
            "You are about to enter icon removal mode.\n"
            "Click on icons to remove them.\n"
            "Press Esc to exit removal mode."
        )
        if response:
            self.remove_icon_mode = True
            self.root.bind('<Escape>', self.exit_remove_icon_mode)

    def exit_remove_icon_mode(self, event=None):
        """Exit icon removal mode."""
        self.remove_icon_mode = False
        self.root.unbind('<Escape>')

    def icon_clicked(self, event, icon_frame):
        """Handle icon click events."""
        # Find the icon data based on the frame
        for icon in self.icons:
            if icon[0] == icon_frame:
                path = icon[1]
                break
        else:
            return  # Icon not found

        if self.remove_icon_mode:
            # Remove the icon
            icon_frame.destroy()
            self.icons = [icon for icon in self.icons if icon[0] != icon_frame]
            self.save_icons()
            self.reposition_icons()
        else:
            # Open the icon
            self.open_icon(path)

    def open_icon(self, path):
        """Open the file or app associated with an icon."""
        if not os.path.exists(path):
            messagebox.showerror("File Not Found", f"The file '{path}' does not exist.")
            return

        extension = os.path.splitext(path)[1].lower()
        if extension in ['.exe', '.py']:
            response = messagebox.askyesno("Execute File", f"Do you want to execute '{os.path.basename(path)}'?")
            if response:
                self.execute_app(path)
            else:
                # Optionally, open in text editor
                self.open_text_editor(file_path=path)
        elif extension in ['.txt', '.md', '.csv', '.json']:
            # Open these file types in the text editor
            self.open_text_editor(file_path=path)
        else:
            # Optionally, open with default application
            try:
                os.startfile(path)
            except AttributeError:
                subprocess.Popen(['open', path])  # For macOS
                # subprocess.Popen(['xdg-open', path])  # For Linux
            except Exception as e:
                messagebox.showerror("Error", f"Cannot open '{os.path.basename(path)}': {e}")

    def execute_app(self, path):
        """Execute a Python script or application."""
        try:
            extension = os.path.splitext(path)[1].lower()
            if extension == '.py':
                # Find system Python to execute the script
                if os.name == 'nt':  # Windows
                    # Try common Python executable paths
                    python_commands = ['python', 'py', 'python3']
                    # Use CREATE_NO_WINDOW flag to hide console window
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0  # SW_HIDE
                else:  # macOS/Linux
                    python_commands = ['python3', 'python']
                    startupinfo = None

                # Try each command until one works
                for python_cmd in python_commands:
                    try:
                        if os.name == 'nt':
                            subprocess.Popen([python_cmd, path],
                                             cwd=os.path.dirname(path),
                                             startupinfo=startupinfo)
                        else:
                            # On Unix-like systems, use nohup to detach from terminal
                            subprocess.Popen([python_cmd, path],
                                             cwd=os.path.dirname(path),
                                             stdout=subprocess.DEVNULL,
                                             stderr=subprocess.DEVNULL)
                        return  # Success, exit the function
                    except FileNotFoundError:
                        continue

                # If no Python command worked, show error
                messagebox.showerror("Python Not Found",
                                     "Could not find Python interpreter to execute the script.\n"
                                     "Make sure Python is installed and in your PATH.")
            else:
                # Execute other applications directly
                if os.name == 'nt':
                    startupinfo = subprocess.STARTUPINFO()
                    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                    startupinfo.wShowWindow = 0
                    subprocess.Popen([path], cwd=os.path.dirname(path), startupinfo=startupinfo)
                else:
                    subprocess.Popen([path], cwd=os.path.dirname(path))
        except Exception as e:
            messagebox.showerror("Execution Error", f"Failed to execute app: {e}")

    def open_settings(self):
        """Open the Settings window."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("400x400")  # Increased height to accommodate new elements
        settings_window.attributes('-topmost', True)

        resolution_frame = tk.Frame(settings_window)
        resolution_frame.pack(pady=10)

        label = tk.Label(resolution_frame, text="Screen Resolution:")
        label.pack()

        self.width_var = tk.StringVar(value=str(self.root.winfo_width()))
        self.height_var = tk.StringVar(value=str(self.root.winfo_height()))

        width_entry = tk.Entry(resolution_frame, textvariable=self.width_var)
        width_entry.pack(pady=5)

        height_entry = tk.Entry(resolution_frame, textvariable=self.height_var)
        height_entry.pack(pady=5)

        # Add a Checkbutton for fullscreen mode
        fullscreen_check = tk.Checkbutton(settings_window, text="Fullscreen Mode", variable=self.fullscreen_var)
        fullscreen_check.pack(pady=10)

        apply_button = tk.Button(settings_window, text="Apply", command=self.apply_resolution)
        apply_button.pack(pady=20)

    def apply_resolution(self):
        """Apply the new screen resolution and fullscreen mode."""
        # Apply fullscreen mode
        if self.fullscreen_var.get():
            self.root.attributes('-fullscreen', True)
            messagebox.showinfo("Fullscreen Mode", "Fullscreen mode enabled. Press F11 or ESC to exit.")
        else:
            self.root.attributes('-fullscreen', False)
            width = self.width_var.get()
            height = self.height_var.get()

            try:
                width = int(width)
                height = int(height)
                self.root.geometry(f"{width}x{height}")
                self.root.resizable(False, False)
                messagebox.showinfo("Success", "Resolution applied successfully!")
                # Update background size
                self.desktop_frame.config(width=width, height=height)
                if self.background_image_path:
                    self.set_background_image(self.background_image_path)
            except ValueError:
                messagebox.showerror("Error", "Invalid resolution values.")

        self.save_settings()

    def toggle_fullscreen(self, event=None):
        """Toggle fullscreen mode with F11."""
        is_fullscreen = self.root.attributes('-fullscreen')
        self.root.attributes('-fullscreen', not is_fullscreen)
        # Update the fullscreen variable
        self.fullscreen_var.set(not is_fullscreen)
        self.save_settings()

    def exit_fullscreen(self, event=None):
        """Exit fullscreen mode when Esc is pressed."""
        if self.root.attributes('-fullscreen'):
            self.root.attributes('-fullscreen', False)
            self.fullscreen_var.set(False)
            self.save_settings()

    def open_customize(self):
        """Open the Customize window."""
        customize_window = tk.Toplevel(self.root)
        customize_window.title("Customize Desktop")
        customize_window.geometry("400x200")
        customize_window.attributes('-topmost', True)

        # Background Color
        color_button = tk.Button(customize_window, text="Change Background Color", command=self.choose_background_color)
        color_button.pack(pady=10)

        # Background Image
        image_button = tk.Button(customize_window, text="Set Background Image", command=self.choose_background_image)
        image_button.pack(pady=10)

        # Remove Background Image
        remove_image_button = tk.Button(customize_window, text="Remove Background Image",
                                        command=self.remove_background_image)
        remove_image_button.pack(pady=10)

    def choose_background_color(self):
        """Open color chooser to select background color."""
        color = colorchooser.askcolor(title="Choose Background Color")
        if color[1]:
            self.set_background_color(color[1])
            if self.background_label:
                self.background_label.destroy()
                self.background_label = None

    def choose_background_image(self):
        """Open file dialog to select a background image."""
        image_path = filedialog.askopenfilename(title="Select Background Image",
                                                filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp")])
        if image_path:
            self.set_background_image(image_path)

    def remove_background_image(self):
        """Remove the background image and revert to background color."""
        if self.background_label:
            self.background_label.destroy()
            self.background_label = None
        self.background_image_path = None
        self.desktop_frame.configure(bg=self.background_color)
        self.save_settings()

    def open_explorer(self):
        """Open the File Explorer window."""
        explorer_window = tk.Toplevel(self.root)
        explorer_window.title("File Explorer")
        explorer_window.geometry("600x400")
        explorer_window.attributes('-topmost', True)

        self.file_listbox = tk.Listbox(explorer_window)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        self.populate_file_list()

        explorer_toolbar = tk.Frame(explorer_window)
        explorer_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

        back_button = tk.Button(explorer_toolbar, text="<", command=self.go_back)
        back_button.pack(side=tk.LEFT, padx=5, pady=5)

        enter_button = tk.Button(explorer_toolbar, text=">", command=self.enter_directory)
        enter_button.pack(side=tk.LEFT, padx=5, pady=5)

        new_file_button = tk.Button(explorer_toolbar, text="New File", command=self.create_new_file)
        new_file_button.pack(side=tk.LEFT, padx=5, pady=5)

        new_folder_button = tk.Button(explorer_toolbar, text="New Folder", command=self.create_new_folder)
        new_folder_button.pack(side=tk.LEFT, padx=5, pady=5)

        delete_button = tk.Button(explorer_toolbar, text="Delete", command=self.delete_selected)
        delete_button.pack(side=tk.LEFT, padx=5, pady=5)

    def populate_file_list(self):
        """Populate the file list in the File Explorer."""
        self.file_listbox.delete(0, tk.END)
        if os.path.exists(self.current_directory):
            for item in os.listdir(self.current_directory):
                self.file_listbox.insert(tk.END, item)

    def go_back(self):
        """Navigate back to the parent directory."""
        parent_directory = os.path.dirname(self.current_directory)
        if os.path.commonpath([self.working_directory]) in os.path.commonpath([parent_directory]):
            self.current_directory = parent_directory
            self.populate_file_list()

    def enter_directory(self):
        """Enter the selected directory."""
        selected = self.file_listbox.get(tk.ACTIVE)
        new_directory = os.path.join(self.current_directory, selected)
        if os.path.isdir(new_directory):
            self.current_directory = new_directory
            self.populate_file_list()

    def create_new_file(self):
        """Create a new file in the current directory."""
        filename = simpledialog.askstring("New File", "Enter file name:")
        if filename:
            open(os.path.join(self.current_directory, filename), 'w').close()
            self.populate_file_list()

    def create_new_folder(self):
        """Create a new folder in the current directory."""
        foldername = simpledialog.askstring("New Folder", "Enter folder name:")
        if foldername:
            os.makedirs(os.path.join(self.current_directory, foldername), exist_ok=True)
            self.populate_file_list()

    def delete_selected(self):
        """Delete the selected file or folder."""
        selected = self.file_listbox.get(tk.ACTIVE)
        path = os.path.join(self.current_directory, selected)
        protected_paths = [
            os.path.join(self.working_directory, 'System'),
            os.path.join(self.working_directory, 'Home')
        ]
        if os.path.commonpath([path]) not in protected_paths:
            try:
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.remove(path)
                self.populate_file_list()
            except Exception as e:
                messagebox.showerror("Delete Error", f"Failed to delete: {e}")
        else:
            messagebox.showwarning("Protected Folder", "You cannot delete this folder.")

    def open_terminal(self):
        """Open the Terminal window."""
        terminal_window = tk.Toplevel(self.root)
        terminal_window.title("Terminal")
        terminal_window.geometry("600x400")
        terminal_window.attributes('-topmost', True)

        terminal_label = tk.Label(terminal_window, text="Enter Python code and press Shift+F10 to run:")
        terminal_label.pack(pady=5)

        self.terminal_entry = tk.Entry(terminal_window)
        self.terminal_entry.pack(fill=tk.X, padx=5, pady=5)
        self.terminal_entry.focus()

        self.terminal_entry.bind("<Shift-F10>", self.run_command_in_new_window)

    def run_command_in_new_window(self, event):
        """Execute the command entered in the terminal."""
        command = self.terminal_entry.get()
        self.terminal_entry.delete(0, tk.END)

        # Create window for output
        output_window = tk.Toplevel(self.root)
        output_window.title("Command Output")
        output_text = tk.Text(output_window)
        output_text.pack(fill=tk.BOTH, expand=True)

        # Create window for errors
        error_window = tk.Toplevel(self.root)
        error_window.title("Error Output")
        error_text = tk.Text(error_window)
        error_text.pack(fill=tk.BOTH, expand=True)

        # Redirect stdout and stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()

        try:
            exec(command, {})
            output = sys.stdout.getvalue()
            error = sys.stderr.getvalue()

            if output.strip():
                output_text.insert(tk.END, output)
            else:
                output_text.insert(tk.END, "No Output.\n")

            if error.strip():
                error_text.insert(tk.END, error)
            else:
                error_text.insert(tk.END, "No Errors.\n")

        except Exception as e:
            error_text.insert(tk.END, f"Exception: {e}\n")
            output_text.insert(tk.END, "No Output.\n")

        finally:
            # Reset stdout and stderr
            sys.stdout = old_stdout
            sys.stderr = old_stderr

        output_text.see(tk.END)
        error_text.see(tk.END)

    def open_text_editor(self, file_path=None):
        """Open the Text Editor window."""
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Text Editor")
        editor_window.geometry("600x400")
        editor_window.attributes('-topmost', True)

        self.editor_text = tk.Text(editor_window)
        self.editor_text.pack(fill=tk.BOTH, expand=True)

        if file_path:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    self.editor_text.insert(tk.END, content)
                editor_window.title(f"Text Editor - {os.path.basename(file_path)}")
                self.current_open_file = file_path
            except Exception as e:
                messagebox.showerror("File Error", f"Failed to open file: {e}")
                self.current_open_file = None
        else:
            self.current_open_file = None

        # Bind Ctrl+S to save function
        editor_window.bind('<Control-s>', self.save_text)

        # Reference to track the editor window
        self.editor_window = editor_window

    def save_text(self, event=None):
        """Save the content in the Text Editor."""
        if hasattr(self, 'editor_text'):
            content = self.editor_text.get("1.0", tk.END)
            if hasattr(self, 'current_open_file') and self.current_open_file:
                full_path = self.current_open_file
            else:
                # Prompt user for save path
                save_path = simpledialog.askstring("Save File",
                                                   "Enter save path including file name and extension (e.g., /Home/Document1.txt):")
                if not save_path:
                    return
                full_path = os.path.join(self.working_directory, save_path.lstrip('/'))
                # Create directories if they don't exist
                os.makedirs(os.path.dirname(full_path), exist_ok=True)
                self.current_open_file = full_path

            try:
                with open(full_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                messagebox.showinfo("Save Successful", f"File saved to {full_path}")
            except Exception as e:
                messagebox.showerror("Save Error", f"Failed to save file: {e}")

    def on_closing(self):
        """Handle the closing of the main window."""
        self.save_icons()
        self.save_settings()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = DesktopApp(root)
    # Handle the closing event to save icons and settings
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()


if __name__ == "__main__":
    main()