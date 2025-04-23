import customtkinter as ctk
from PIL import Image
from tkinter import filedialog, messagebox
import os
import subprocess
import tkinter as tk

def browse_file():
    file_path = filedialog.askopenfilename(
        filetypes=[("MP4 Video Files", "*.mp4")],  # Restrict to .mp4 files
        title="Select a Video File"
    )
    if file_path:
        input_label.configure(text=f"Selected: {os.path.basename(file_path)}")
        global selected_file
        selected_file = file_path  # Store the selected file globally for further use
    else:
        input_label.configure(text="No file selected.")

def convert_video():
    global selected_file, save_path
    if not selected_file:
        output_label.configure(text="No video file selected!")
        return

    if not save_path:
        output_label.configure(text="No save location selected!")
        return

    # Check if the file already exists, and delete it if necessary
    if os.path.exists(save_path):
        try:
            os.remove(save_path)  # Delete the existing file
        except Exception as e:
            output_label.configure(text="Error removing existing file!")
            print(f"Error removing file: {e}")
            return

    # Prepare input path
    input_path = selected_file

    # FFmpeg conversion command
    ffmpeg_command = [
        "ffmpeg",
        "-y",  # Force overwrite
        "-i", input_path,  # Input file
        "-s", "176x144",  # Resolution
        "-c:v", "mpeg4",  # Video codec
        "-c:a", "aac",  # Audio codec
        "-b:a", "32k",  # Audio bitrate
        save_path  # Output file path
    ]

    try:
        # Run the FFmpeg command
        subprocess.run(ffmpeg_command, check=True)
        output_label.configure(text=f"Video converted and saved successfully: {os.path.basename(save_path)}")

        # Show success message box
        messagebox.showinfo("Converted", f"Video successfully converted and saved as:\n{os.path.basename(save_path)}")

    except subprocess.CalledProcessError as e:
        output_label.configure(text="Error during video conversion!")
        print("FFmpeg error:", e)

def browse_save_location():
    global save_path
    save_path = filedialog.asksaveasfilename(
        defaultextension=".3gp",
        filetypes=[("3GP Video Files", "*.3gp")],
        title="Select Save Location"
    )

    if save_path:
        output_label.configure(text=f"Save Location Selected: {os.path.basename(save_path)}")
    else:
        output_label.configure(text="No save location selected.")

def exit_app():
    root.quit()

# Function for the About menu
def about():
    messagebox.showinfo("About", "This application is designed to convert videos into a low-resolution format for older phones, using FFmpeg as the backend"
                                               "Please note: This application is optimized for older devices and may not support high-resolution video outputs"  
                                               "            \n"
                                               "Version: 1.0\n"  
                                                "                  \n"
                                                "Developed by Yossef Ibrahim"
                                              )

root = ctk.CTk()
root.geometry("600x600")
root.iconbitmap("Data/icon.ico")
root.title("Video Converter")
root.resizable(False, False)
image_path=r"Data\\image.png"

image = ctk.CTkImage(
    dark_image=Image.open(image_path),
    light_image=Image.open(image_path),
    size=(120, 150)
)
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)

file_menu.add_command(label="About", command=about)
file_menu.add_command(label="Exit", command=exit_app)

root.config(menu=menu_bar)

ctk.CTkLabel(root,text="", image=image).place(
    relx=0.5, rely=0.05, anchor="n")
ctk.CTkLabel(root,text="Video Converter",font=ctk.CTkFont("Arial",40)).place(
    relx=0.5, rely=0.35, anchor="n")
ctk.CTkLabel(root,text="To Run on itel Phone",font=ctk.CTkFont("Times new roman",20)).place(
    relx=0.5, rely=0.45, anchor="n")

# This is a buttons
# Button of Browse path video

selected_file = None

folder_icon_path=r"Data\icon_folder.png"
folder_img = ctk.CTkImage(
    dark_image=Image.open(folder_icon_path),
    light_image=Image.open(folder_icon_path),
    size=(25, 25)
)

# Input file selection button
browse_button = ctk.CTkButton(root, image=folder_img,text="",command=browse_file,width=25,fg_color="transparent")
browse_button.place(relx=0.2,rely=0.59)

input_label = ctk.CTkLabel(root, text="No file selected.", font=("Arial", 20))
input_label.place(relx=0.35,rely=0.6)

output_label = ctk.CTkLabel(root, text="output.3gp", font=("Arial", 20))
output_label.place(relx=0.35,rely=0.70)

#func browse_file
saved_video = ctk.CTkButton(master=root,text=" Browse ",fg_color="#4cd44c",font=ctk.CTkFont("Arial",14),corner_radius=15,width=110,height=30,command=browse_save_location).place(relx=0.22,rely=0.75,anchor="s")
#func convert_video
convert_button = ctk.CTkButton(master=root,text=" Convert ",font=ctk.CTkFont("Arial",14),corner_radius=15,width=130,height=30,command=convert_video).place(relx=0.5,rely=0.9,anchor="s")

root.mainloop()
