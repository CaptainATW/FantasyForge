import tkinter as tk
from PIL import ImageTk, Image

# Create the main window
root = tk.Tk()

# Create the header frame
header = tk.Frame(root)
header.pack(side="top", fill="x")

# Load the icon image
img = Image.open("icon.png")
img = img.resize((int(img.width/2), int(img.height/2)))
icon = ImageTk.PhotoImage(img)

# Add the image to the header frame
icon_label = tk.Label(header, image=icon)
icon_label.pack(side="left")

# Add the character and health text to the header frame
character = "Alex"
health = "100/100"
character_health_label = tk.Label(header, text=f"Character: {character} | Health: {health}")
character_health_label.pack(side="left")

# Add the "Made by Alex Wang" text to the header frame
made_by_label = tk.Label(header, text="Made by Alex Wang for Leland CS hackathon")
made_by_label.pack(side="right")

# Start the main event loop
root.mainloop()
