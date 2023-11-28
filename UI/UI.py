import sys
sys.path.append('../API')

import tkinter as tk
import api

BUTTON_WIDTH = 15  # Adjust the width of the buttons according to your preference
BUTTON_HEIGHT = 2  # Adjust the height of the buttons according to your preference

class TextClassifierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Title Classifier")
        self.master.geometry("850x300") # Fix the window to 800x300
        self.master.resizable(False, True)  # Allow only height adjustment
        self.titles = []
        self.last_title = ""

        # Attempt to connect to db
        self.db = api.connect_to_db()
        if self.db == -1:
            quit()

        self.welcome_screen()

    def welcome_screen(self):
        """
        Displays Welcome screen for user. Allows user to start classification
        """ 
        self.clear_screen()

        welcome_label = tk.Label(self.master, text="Welcome to Title Classifier!\nYou will receive different Reddit post titles and you must classify them based on bias. ", font=('Helvetica', 20), wraplength=600)
        welcome_label.pack(pady=20)

        start_button = tk.Button(self.master, text="Start Labeling", command=self.start_labeling)
        start_button.pack()
    
    def uploadTitle(self, label, title):
        """
        Attempts to upload title and label to database.
        Stores the recently uploaded title as self.last_title

        :param label: The category of bias based on the title
        :param title: The title that corresponds to the label
        """ 
        api.upload_title(self.db, label, title)

        self.last_title = title
        self.next_text() # go to the next text

    def start_labeling(self):
        """
        Clears the title screen and starts the labeling process.
        Retrieves Reddit titles from Reddit API
        """ 
        self.clear_screen()
        self.titles = api.get_titles()
        self.display_text()

    def display_text(self):
        """
        If self.titles is populated, display title text and buttons.
        If self.titles is not populated, repopulate list go to next_text()
        """ 
        if self.titles:
            title = self.titles.pop()

            text_label = tk.Label(self.master, text=title, font=('Helvetica', 20), wraplength=600)
            text_label.pack(pady=20)

            undo_button = tk.Button(self.master, text="Undo Last Choice", command=self.undo, width=BUTTON_WIDTH, height=BUTTON_HEIGHT)
            undo_button.pack(side="top")  # Add some padding between options and the undo button

            button_frame = tk.Frame(self.master)
            button_frame.pack(side="bottom", pady=10)

            option1_button = tk.Button(button_frame, text="Israel Bias", command=lambda: self.uploadTitle(-1, title), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="#005EB8")
            option1_button.pack(side="left",padx=20)

            option2_button = tk.Button(button_frame, text="Palestine Bias", command=lambda: self.uploadTitle(1, title), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="#009736")
            option2_button.pack(side="left",padx=20)

            neither_button = tk.Button(button_frame, text="Neither", command=lambda: self.uploadTitle(0, title), width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="#8D8D8D")
            neither_button.pack(side="left",padx=20)

            skip_button = tk.Button(button_frame, text="N/A", command=self.next_text, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="#464646")
            skip_button.pack(side="left",padx=20)

            quit_button = tk.Button(button_frame, text="Quit", command=self.quit_program, width=BUTTON_WIDTH, height=BUTTON_HEIGHT, bg="#FF0000")
            quit_button.pack(side="left",padx=20)
        
        else:
            self.titles = api.get_titles()
            self.next_text()

    def undo(self):
        """
        Removes the last uploaded title from the database
        """ 
        api.remove_title(self.db, self.last_title)

    def next_text(self):
        """
        Clears the screen and displays new title
        """ 
        self.clear_screen()
        self.display_text()

    def clear_screen(self):
        """
        Removes all widgets on screen
        """
        for widget in self.master.winfo_children():
            widget.destroy()
    
    def quit_program(self):
        """
        Quits program
        """ 
        quit()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextClassifierApp(root)
    root.mainloop()
