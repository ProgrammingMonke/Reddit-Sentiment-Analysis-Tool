import tkinter as tk

class TextClassifierApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Title Classifier")
        self.master.geometry("850x300") # Fix the window to 800x200
        self.master.resizable(False, True)  # Allow only height adjustment

        self.welcome_screen()

    # Welcome Screen
    def welcome_screen(self):
        self.clear_screen()

        welcome_label = tk.Label(self.master, text="Welcome to Title Classifier!\nYou will receive different Reddit post titles and you must classify them based on bias. ", font=('Helvetica', 20))
        welcome_label.pack(pady=20)

        start_button = tk.Button(self.master, text="Start Labeling", command=self.start_labeling)
        start_button.pack()

    # Call API to get the random Reddit Titles
    def getTitles(self):
        titles = ["The root cause of the Israel-Palestine conflict lies in its location, and obviously the British",
                             "Why did they split Palestine and Israel in that awful way? [Serious]", 
                            "I have changed my mind about the Israel-Palestine conflict. Have you?", 
                            "Palestinian Poll on the 10/7 Attacks Show Widespread Support"] 
        return titles
    
    # Call API to upload the title string and the label associated with it
    def uploadTitle(self,label,title):
        print("title:", title)
        print("label:",str(label))
        #upload_title(label,title)
        self.next_text() # go to the next text
    
    # Starts the labeling process
    def start_labeling(self):
        self.clear_screen()
        
        # Call getTitles()
        self.texts = self.getTitles()
        self.current_text_index = 0

        self.display_text()

    def display_text(self):
        if self.current_text_index < len(self.texts):
            undo_button = tk.Button(self.master, text="Undo Last Choice", command=self.undo, width=15, height=2)
            undo_button.pack(side="top")  # Add some padding between options and the undo button

            currTitle = self.texts[self.current_text_index]

            text_label = tk.Label(self.master, text=currTitle, font=('Helvetica', 20),wraplength=400)
            text_label.pack(pady=20)

            button_width = 15  # Adjust the width of the buttons according to your preference
            button_height = 2  # Adjust the height of the buttons according to your preference

            button_frame = tk.Frame(self.master)
            button_frame.pack(side="bottom", pady=10)

            option1_button = tk.Button(button_frame, text="Israel Bias", command=lambda: self.uploadTitle(-1,currTitle), width=button_width, height=button_height)
            option1_button.pack(side="left",padx=20)

            option2_button = tk.Button(button_frame, text="Palestine Bias", command=lambda: self.uploadTitle(1,currTitle), width=button_width, height=button_height)
            option2_button.pack(side="left",padx=20)

            neither_button = tk.Button(button_frame, text="Neither", command=lambda: self.uploadTitle(0,currTitle), width=button_width, height=button_height)
            neither_button.pack(side="left",padx=20)

            skip_button = tk.Button(button_frame, text="N/A", command=self.next_text, width=button_width, height=button_height)
            skip_button.pack(side="left",padx=20)
        
        else:
            self.show_completion_screen()

    def undo(self):
        # Implement the logic to undo the previous action
        if self.current_text_index > 0:
            self.current_text_index -= 1
            self.clear_screen()
            self.display_text()

    def next_text(self):
        self.current_text_index += 1
        self.clear_screen()
        self.display_text()

    def show_completion_screen(self):
        self.clear_screen()

        completion_label = tk.Label(self.master, text="All texts have been labeled!", font=('Helvetica', 16))
        completion_label.pack(pady=20)

        return_button = tk.Button(self.master, text="Return to Menu", command=self.welcome_screen)
        return_button.pack()

    def clear_screen(self):
        for widget in self.master.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextClassifierApp(root)
    root.mainloop()
