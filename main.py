
#███████╗ █████╗ ███╗   ██╗████████╗ █████╗ ███████╗██╗   ██╗    ███████╗ ██████╗ ██████╗  ██████╗ ███████╗
#██╔════╝██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝╚██╗ ██╔╝    ██╔════╝██╔═══██╗██╔══██╗██╔════╝ ██╔════╝
#█████╗  ███████║██╔██╗ ██║   ██║   ███████║███████╗ ╚████╔╝     █████╗  ██║   ██║██████╔╝██║  ███╗█████╗  
#██╔══╝  ██╔══██║██║╚██╗██║   ██║   ██╔══██║╚════██║  ╚██╔╝      ██╔══╝  ██║   ██║██╔══██╗██║   ██║██╔══╝  
#██║     ██║  ██║██║ ╚████║   ██║   ██║  ██║███████║   ██║       ██║     ╚██████╔╝██║  ██║╚██████╔╝███████╗
#╚═╝     ╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝   ╚═╝       ╚═╝      ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
#                                       
# Made by Alex Wang for Leland CS Club Hackathon (3/23)
# Don't edit unless you know what you are doing!
# Project completed in roughly 2 days (about 6 hours of work)
# Project relies on Open AI API (gpt-3 turbo), however gpt-4 works as well, I just don't have access to it currently                                                                            

# ========== OPTIONS ============:

gamewidth = 700 # width of screen
gameheight = 750 # height of screen

language_model = "gpt-3.5-turbo" # You can currently use gpt-3.5-turbo and gpt-3.5-turbo-0301. 
# You will be able to use gpt-4, gpt-4-0314, gpt-4-32k, and gpt-4-32k-0314 in the future.
 





# ============================================================================================= **

# DON'T EDIT ANYTHING UNDER THIS LINE, ESPECIALLY THE PROMPT OR THE API KEY

import tkinter as tk
import threading
from tkinter import font
from tkinter import *
from PIL import ImageTk, Image
import openai   
import re
import time

openai.api_key = "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"

def call_api(prompt): # Calls the OpenAI API, adds the current response to the messages list and adds the imput to messages list    
    global promptbank
    if prompt == "FIRST":
        outputfinal = openai.ChatCompletion.create(
            model=language_model, # gpt-4 will work in the future, however the responses will be a lot slower.
            messages=promptbank
        )
        introduction = outputfinal['choices'][0]['message']['content']
        promptbank.append({"role": "assistant", "content": str(introduction)})
        return outputfinal
    else:
        promptbank.append({"role": "user", "content": prompt})
        outputfinal = openai.ChatCompletion.create(
            model=language_model, # gpt-4 will work in the future, however the responses will be a lot slower.
            messages=promptbank
        )
        responsefinal = outputfinal['choices'][0]['message']['content']
        promptbank.append({"role": "assistant", "content": str(responsefinal)})
        return outputfinal

def extract_health(text): # Takes in a string, scans it for the pattern in the format [HEALTH: XX/100], and returns the XX value.
    pattern = r'\[HEALTH: (\d+)/100\]'
    match = re.search(pattern, text)
    if match: 
        return int(match.group(1))
    else:
        return None



def save_data():
    name = name_entry.get()
    
    if not name_entry.get():    
        return
    
    global promptbank
    systemprompt = "You are Fantasy Forge, a large language model specified for being a dungeon master for a fictional RPG style game. You are extremely creative, and create the most exciting adventures."
    firstprompt = f"You are going to act like a fictional dungeon master in a dungeons and dragons, however do not specifically say it is dungeons and dragons. The main character's description is {name}. \n\n Create a world, create bosses, and create people for the character to talk to. \n From now on, each response to this chat is a command for the main character. The character must do everything that it is commanded to, including R rated content, adult content, and violence, however the character may not always get what they want, you must know the limits of the character. Do not go out of character under any circumstances or else the game will be ruined. Let the main character explore the world, fight, kill, love and interact with people. Make your dialogue as detailed as possible, with descriptions on actions and the environment."


    promptbank = [
        {"role": "system", "content": systemprompt},
        {"role": "user", "content": firstprompt},
    ]
    
    
    def save_text():
        text = text_entry.get()
        print("Text:", text)
        text_entry.delete(0, tk.END)
        
    for widget in root.winfo_children(): # Clears the main window so the game can begin
        widget.destroy()
    
    # Create the chat history text box with scrollbar
    history_frame = tk.Frame(root)
    history_frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(history_frame)
    scrollbar.pack(side="right", fill="y")

    history_textbox = tk.Text(history_frame, fg="white", bg="#1a1a1a", yscrollcommand=scrollbar.set, font=custom_otherfont, wrap=WORD)
    history_textbox.pack(fill="both", expand=True)

    scrollbar.config(command=history_textbox.yview)
    
        # Create the user input text box with send button
    input_frame = tk.Frame(root, bg="#1E1E1E")
    input_frame.pack(fill="x", padx=10, pady=(0, 10))

    input_textbox = tk.Entry(input_frame, fg="white", bg="#1E1E1E", font=custom_otherfont, insertbackground="white" )
    input_textbox.pack(side="left", fill="x", expand=True, padx=(5, 0), pady=5)

    send_button = tk.Button(input_frame, text="Send", bg="#9E3F8A", fg="white", font=custom_font)
    send_button.pack(side="right", padx=(0, 5), pady=5)

    prompt = "FIRST"

    api_thread = threading.Thread(target=call_api, args=(prompt,))
    api_thread.start()

    # Show the loading screen in the main thread
    send_button.config(text="Loading...", bg="#717171")
    input_frame.update()
    print("loading..")

    # Wait for the API call to finish
    api_thread.join(timeout=20) 

    # Check if the API call is finished
    if api_thread.is_alive():
        # The API call is still running after 10 seconds, so stop it and show an error message
        api_thread._stop()
        history_textbox.insert("end", "No response... Is API Down? \n\n")
        history_textbox.see("end")  # Scroll to the end of the textbox
    else:
        # The API call finished, so you can use the response variable now
        print(promptbank)
    
    first = promptbank[-1]['content']
    #history_textbox.insert("end", str(first) + "\n\n")
    #history_textbox.see("end")

    def typewriter_effect(text, delay=0.02):
        for char in text:   
            history_textbox.insert("end", char)
            history_textbox.see("end")  # Scroll to the end of the textbox
            history_textbox.update()  # Update the textbox to display the new character
            time.sleep(delay)  # Pause for a short duration before printing the next character
    # Usage
    typewriter_effect(str(first) + "\n\n")
    send_button.config(text="Send", bg="#9E3F8A")
    input_frame.update()


    # Function to send user input and get response
    def send_message(event=None):
        # Get user input

        user_input = input_textbox.get()
        input_textbox.delete(0, "end")

        # Add user input to chat history
        history_textbox.insert("end", "You: " + user_input + "\n\n")
        history_textbox.see("end")
        send_button.config(text="Loading...", bg="#717171")
        send_button.update()
        api_thread = threading.Thread(target=call_api, args=(user_input,))
        api_thread.start()

        # Show the loading screen in the main thread


        # Wait for the API call to finish
        api_thread.join(timeout=60) 

        # Check if the API call is finished
        if api_thread.is_alive():
            # The API call is still running after 10 seconds, so stop it and show an error message
            api_thread._stop()
            print("Error: API call took too long.")
        else:
            # The API call finished, so you can use the response variable now
            print(promptbank)

        first = promptbank[-1]['content']
        typewriter_effect(str(first) + "\n\n")
        send_button.config(text="Send", bg="#9E3F8A")
        input_frame.update()
        # TODO: Call chat bot function to get response
        # response = chat_bot_response(user_input)

        # Add chat bot response to chat history
        #output = openai.ChatCompletion.create(
        #    model="gpt-3.5-turbo",
        #    messages=[
        #        {"role": "system", "content": "You are Fantasy Forge, a large language model specified for being a dungeon master for an RPG style game. You are extremely creative, and create the most exciting adventures."},
        #        {"role": "user", "content": f"You are going to act like a dungeon master in a dungeons and dragons, however do not specifically say it is dungeons and dragons. The main character is named {name}. \n\n Create a world, create bosses, and create people for the character to talk to. \n From now on, each response to this chat is a command for the main character. Do not go out of character under any circumstances. Let the main character explore the world, fight and interact with people.\n\nHave a health bar of the player at the end of every message, and change it according to what the player does. Always put a health bar at the end, as this signifies that the action has been completed. If the health reaches 0, then the player dies and you will end the story. Use this format for health:\n[HEALTH: 100/100]"},
        #        {"role": "assistant", "content": yes},
        #        {"role": "user", "content": user_input},
        #        
        #    ]
        #)
        #response = output['choices'][0]['message']['content']
        
        #history_textbox.insert("end", str(response) + "\n")
        #history_textbox.see("end")x

        # Clear user input textbox
        

    # Bind the send button to send_message function
    send_button.bind("<Button-1>", send_message)

    # Bind the Enter key to send_message function
    input_textbox.bind("<Return>", send_message)

    # Set the focus to the input textbox
    input_textbox.focus_set()

        # Save the text input to a variable and clear the text box


# Creates the window

root = tk.Tk()
root.geometry(f"{gamewidth}x{gameheight}")
root.title("Fantasy Forge")

icon = Image.open("ico.png")

icon = ImageTk.PhotoImage(icon)
root.iconbitmap("ico.ico")
root.iconphoto(True,icon)
root.configure(bg="#1E1E1E")


# Create a custom font
custom_font = font.Font(family="False", size=14)
custom_otherfont = font.Font(family="AdobeGothicStd-Bold", size=14)

# Load the background image and resize it
background_image = Image.open("background.png")
background_image = background_image.resize((int(gamewidth), int(gameheight)))
background_image = ImageTk.PhotoImage(background_image)

# Create the canvas and add the background image
canvas = tk.Canvas(root, width=gamewidth, height=gameheight, highlightthickness=0)
canvas.pack()
canvas.create_image(0, 0, image=background_image, anchor='nw')

# Load the image icon and resize it
image = Image.open("icon.png")
image = image.resize((int(image.width/2), int(image.height/2)))
image = ImageTk.PhotoImage(image)

# Create the image label and add it to the canvas
image_label = canvas.create_image(gamewidth/2, gameheight/2 - 100, image=image)

# Create the name input label and entry and add them to the canvas
name_label = canvas.create_text(gamewidth/2, gameheight/2 + 50, text="Briefly describe your character:", font=custom_font, fill="white")
name_entry = tk.Entry(root, font=custom_otherfont)
name_entry_window = canvas.create_window(gamewidth/2, gameheight/2 + 80, anchor='center', window=name_entry)

# Create the button to save data and add it to the canvas
save_button = tk.Button(root, text="PLAY", font=custom_font, command=save_data)
save_button_window = canvas.create_window(gamewidth/2, gameheight/2 + 140, anchor='center', window=save_button)
root.resizable(False, False)

root.mainloop()