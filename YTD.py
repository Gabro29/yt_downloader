"""
    Desktop App that download video from YT
"""

from tkinter import Label, Entry, Tk, Button, END, Menu, Toplevel, Text
from tkinter import font as tkfont
from tkinter import messagebox
from tkinter.filedialog import askdirectory
from ttkthemes import ThemedStyle
from moviepy.video.io.VideoFileClip import VideoFileClip
import pytube
from os import listdir, remove, path
from shutil import copyfile
from threading import Thread


class SecondWindow(Toplevel):
    def __init__(self, parent, title, geometry, propagate, b):
        super().__init__(parent)
        self.title(title)
        self.geometry(geometry)
        self.propagate(propagate)
        self.resizable(0, 0)
        self.iconbitmap("icon.ico")


class DYT(Tk):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.geometry("600x200")
        self.title("YouTube Downloader")
        self.iconbitmap("icon.ico")
        self.propagate(True)
        self.resizable(1, 1)

        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        self.on_start()
        self.read_fronzoli()

    def on_start(self):

        # Add Menu
        self.menubar = Menu(self)
        self.add_menu()
        self.config(menu=self.menubar)

        url_label = Label(self, text="Click inside the box to paste the URL", font=("Spectral", 15), foreground="black",
                          relief="flat")
        url_label.place(relx=0.2, rely=0.09)
        self.url_entry = Entry(self, font=("Lucinda Console", 15))
        self.url_entry.place(relx=0.15, rely=0.3, width=400, height=30)
        self.url_entry.bind("<Button>", self.pasted)

        download_button = Button(self, text="Download", command=lambda: Thread(target=self.download_link).start(),
                                 fg="black", bg="light green", relief="raised",
                                 activebackground="Silver", font=("Times", 15))
        download_button.place(relx=0.3, rely=0.5, width=110, height=30)

        cancel_button = Button(self, text="Clear", command=lambda: Thread(target=self.clear_box).start(),
                                 fg="black", bg="Silver", relief="raised",
                                 activebackground="light green", font=("Times", 15))
        cancel_button.place(relx=0.5, rely=0.5, width=110, height=30)

        self.load_label = Label(self, text="", font=("Spectral", 17),
                                foreground="black", relief="flat")
        self.load_label.place(relx=0.32, rely=0.75, width=210, height=30)

    def read_fronzoli(self):

        with open("fronzoli.dat", "r") as file:
            for line in file:
                if line.split("=")[0] == "EXE_DIR":
                    exe_dir = line.split("=")[1][:-1]
                elif line.split("=")[0] == "OUTPUT_DIR":
                    output_dir = line.split("=")[1]
        try:
            print(exe_dir)
            print(output_dir)
        except UnboundLocalError:
            self.manage_directories()

    def add_menu(self):

        filemenu = Menu(self.menubar, tearoff=0, font=("Lucinda Console", 10))
        filemenu.add_command(label="Output Directories", command=lambda: Thread(target=self.manage_directories).start())
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.quit)
        self.menubar.add_cascade(label="Options", menu=filemenu)

        helpmenu = Menu(self.menubar, tearoff=0, font=("Lucinda Console", 10))
        helpmenu.add_command(label="Contacts", command=self.contact_me)
        helpmenu.add_separator()
        helpmenu.add_command(label="About...", command=self.info_app)
        self.menubar.add_cascade(label="Help", menu=helpmenu)

    def download_link(self):
        """Download pasted link"""

        self.load_label.config(text=f"Wait...")
        self.update_idletasks()
        # Download Video and get mp3
        if self.url_entry.get() == "" or "https://www.youtube.com" not in self.url_entry.get():
            self.load_label.config(text="Insert a valid URL!")
            self.update_idletasks()
        else:
            # Download Video
            mp4_only = self.download_video(self.url_entry.get())
            # Convert to Mp3
            self.convert_to_mp3(mp4_only)

            # Remove downloades video and move in the music directory
            self.move_and_remove()

            self.clear_box()
            self.load_label.config(text="Done!")
            self.update_idletasks()

    def download_video(self, url):
        self.load_label.config(text="Downloading...")
        self.update_idletasks()
        video = pytube.YouTube(url)
        self.load_label.config(text="Converting...")
        self.update_idletasks()
        stream = video.streams.get_highest_resolution()
        stream.download()
        return stream.default_filename

    @staticmethod
    def convert_to_mp3(filename):
        clip = VideoFileClip(filename)
        clip.audio.write_audiofile(filename[:-4] + ".mp3")
        clip.close()

    @staticmethod
    def move_and_remove():
        """https://www.youtube.com/watch?v=aDL7dwpKOuw"""

        with open("fronzoli.dat", "r") as file:
            for line in file:
                if line.split("=")[0] == "EXE_DIR":
                    exe_dir = line.split("=")[1][:-1]
                elif line.split("=")[0] == "OUTPUT_DIR":
                    output_dir = line.split("=")[1]

        for file in listdir(fr"{exe_dir}"):
            if file.endswith(".mp3"):
                copyfile(path.join(fr"{exe_dir}", file),
                                path.join(fr"{output_dir}", file))
        for file in listdir(fr"{exe_dir}"):
            if file.endswith(".mp4") or file.endswith(".mp3"):
                remove(path.join(fr"{exe_dir}", file))

    def pasted(self, b):

        selected = self.clipboard_get()
        self.url_entry.insert(0, selected)

    def clear_box(self):

        self.url_entry.delete(0, END)

    def contact_me(self):
        """Stampo a schermo il mio indirizzo mail"""

        contact_window = SecondWindow(self, "Mail Contact ", "300x100", False, (0, 0))
        stile_5 = ThemedStyle(contact_window)
        stile_5.theme_use(f"clearlooks")

        label_contact = Text(contact_window, height=3, font=("Spectral", 15))
        label_contact.insert(1.0,
                             "    You can contact the productor\n      by email to:\n          gabri729@gmail.com")
        label_contact.pack()
        label_contact.configure(state="disabled")

    def info_app(self):
        """Termini e condizioni d'uso"""

        info_window = SecondWindow(self, "Info App", "720x140", False, (0, 0))
        stile_6 = ThemedStyle(info_window)
        stile_6.theme_use(f"clearlooks")

        info_label = Label(info_window,
                           text="This program have been made by Gabro.\n"
                                "Its free and very minimal.\n"
                                "It is able to download audio from\n"
                                "a YouTube video.",
                           font=("Spectral", 15),
                           foreground="black")

        info_label.pack(pady=10)

    def manage_directories(self):


        manage_popup = messagebox.showinfo('Select Directory', 'Select the diretory where the exe file lives. Press OK to continue')
        exe_directory = askdirectory()

        manage_popup = messagebox.showinfo('Select Directory', 'Now select the output diretory. Press OK to continue')
        output_directory = askdirectory()

        if exe_directory != "" and output_directory != "":
            if "YTD.exe" in listdir(fr"{exe_directory}"):
                with open("fronzoli.dat", "w") as file:
                    file.write(f"EXE_DIR={exe_directory}\n")
                    file.write(f"OUTPUT_DIR={output_directory}")
            else:
                manage_popup = messagebox.showerror('Attention', 'Select the right directory for the exe file, please repeat again :(')
                self.manage_directories()
        else:
            manage_popup = messagebox.showwarning('Attention', 'Nothing has changed. Some error occurred, please repeat again :(')
            self.manage_directories()


if __name__ == "__main__":
    try:
        dat = open("fronzoli.dat", "xt")
    except FileExistsError:
        pass

    DYT().mainloop()
