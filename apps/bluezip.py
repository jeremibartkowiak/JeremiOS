import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import zipfile
import os
import webbrowser  # Module to open links in the default browser


# Function to extract a .bluezip or .redzip archive
def extract_archive(file_extension):
    archive_path = filedialog.askopenfilename(
        title=f"Select a {file_extension.upper()} Archive",
        filetypes=[(f"{file_extension.upper()} Files", f"*.{file_extension}"), ("All Files", "*.*")]
    )
    if not archive_path:
        return  # User canceled

    destination = filedialog.askdirectory(title="Select Destination Folder")
    if not destination:
        return  # User canceled

    create_folder = messagebox.askyesno(
        "Create Folder?",
        f"Do you want to create a new folder named '{os.path.basename(archive_path).split('.')[0]}'?"
    )
    if create_folder:
        destination = os.path.join(destination, os.path.basename(archive_path).split('.')[0])
        os.makedirs(destination, exist_ok=True)

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
    progress.pack(pady=10)
    progress.start()

    try:
        with zipfile.ZipFile(archive_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        messagebox.showinfo("Success", f"{file_extension.upper()} Archive Extracted Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to Extract Archive: {str(e)}")
    finally:
        progress.stop()
        progress.pack_forget()


# Function to create a .bluezip or .redzip archive
def create_archive(file_extension):
    # Ask the user to choose between selecting files or a folder
    choice = messagebox.askquestion(
        "Choose Input Type", "Do you want to archive an entire folder? Click 'Yes' for Folder or 'No' for Files."
    )

    if choice == 'yes':
        # User wants to archive a folder
        folder_path = filedialog.askdirectory(title="Select Folder to Archive")
        if not folder_path:
            return  # User canceled
        source = [folder_path]
    else:
        # User wants to archive files
        source = filedialog.askopenfilenames(title="Select Files to Archive")
        if not source:
            return  # User canceled

    # Ask the user to select destination for the archive
    save_path = filedialog.asksaveasfilename(
        title=f"Save as {file_extension.upper()} Archive",
        defaultextension=f".{file_extension}",
        filetypes=[(f"{file_extension.upper()} Archive", f"*.{file_extension}")]
    )
    if not save_path:
        return  # User canceled

    if not save_path.endswith(f".{file_extension}"):
        save_path += f".{file_extension}"

    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="indeterminate")
    progress.pack(pady=10)
    progress.start()

    try:
        with zipfile.ZipFile(save_path, 'w') as zip_ref:
            for item in source:
                if os.path.isdir(item):  # It's a folder
                    for root_dir, dirs, files in os.walk(item):
                        for file in files:
                            file_path = os.path.join(root_dir, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(item))
                            zip_ref.write(file_path, arcname)
                else:  # It's a file
                    zip_ref.write(item, os.path.basename(item))

        messagebox.showinfo("Success", f"{file_extension.upper()} Archive Created Successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to Create Archive: {str(e)}")
    finally:
        progress.stop()
        progress.pack_forget()


# Function to open a link in the browser
def open_link():
    webbrowser.open("https://example.com")  # Replace with your desired URL


# Main Tkinter Window
root = tk.Tk()
root.title("BlueZIP")
root.geometry("600x500")
root.resizable(True, True)
root.configure(bg="lightblue")

# Add a title label
title_label = tk.Label(
    root, text="Welcome to BlueZIP", font=("Arial", 20), bg="lightblue", fg="darkblue"
)
title_label.pack(pady=20)

# Create buttons
btn_extract_bluezip = tk.Button(
    root, text="Extract a BlueZIP Archive", font=("Arial", 14), bg="blue", fg="white",
    command=lambda: extract_archive("bluezip")
)
btn_extract_bluezip.pack(pady=10)

btn_make_bluezip = tk.Button(
    root, text="Make a BlueZIP Archive", font=("Arial", 14), bg="blue", fg="white",
    command=lambda: create_archive("bluezip")
)
btn_make_bluezip.pack(pady=10)

btn_extract_redzip = tk.Button(
    root, text="Extract a RedZIP Archive", font=("Arial", 14), bg="red", fg="white",
    command=lambda: extract_archive("redzip")
)
btn_extract_redzip.pack(pady=10)

btn_make_redzip = tk.Button(
    root, text="Make a RedZIP Archive", font=("Arial", 14), bg="red", fg="white",
    command=lambda: create_archive("redzip")
)
btn_make_redzip.pack(pady=10)

# Add an image label in the bottom-left corner
try:
    # Load the image
    from PIL import Image, ImageTk  # Pillow for image handling
    image_path = "C:/Images/image.png"  # Replace with the path to your image
    image = Image.open(image_path)
    image = image.resize((66, 50))  # Resize to a smaller size for display
    tk_image = ImageTk.PhotoImage(image)

    # Create an image label (without button)
    img_label = tk.Label(root, image=tk_image, bg="lightblue")  # Set bg to match window color
    img_label.place(x=10, y=440)  # Adjust the position for bottom-left corner
except FileNotFoundError:
    print("Image not found. Please provide a valid image path.")

# Run the Tkinter main loop
root.mainloop()
