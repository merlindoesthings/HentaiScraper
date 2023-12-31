import customtkinter as ctk
import toml

from PIL import Image
from spider import Parser
from spider.nhentai import nHentai

BORDER_COLOR = "#ED2553"
ENTRY_COLOR = "#1F1F1F"
TEXT_COLOR = "#D9D9D9"
FG_COLOR = "#0D0D0D"
HOVER_COLOR = "#762739"
FRAME_COLOR = "#292424"
SUCCESS_COLOR = "#34eb46"

WIDTH, HEIGHT = 550, 450

class GUI(ctk.CTk):
    def __init__(self):
        ctk.set_appearance_mode("Dark")
        super().__init__()
        self.path = ctk.StringVar()
        self.threads = ctk.IntVar()
        
        self.title("HentaiScraper")
        self.geometry(f'{WIDTH}x{HEIGHT}')
        self.resizable(False, False)
        
        self.sideframe = ctk.CTkFrame(master = self, 
                                  width = 75, 
                                  height = HEIGHT, 
                                  fg_color = FG_COLOR,
                                  border_width = 0,
                                  corner_radius = 0)
        self.sideframe.grid(row = 0, column = 0, padx = 0, pady= 0, sticky = 'nsew', rowspan = 4)

        self.local_settingFrame = ctk.CTkFrame(self,
                                               width = 450,
                                               height = 300,
                                               corner_radius = 15,
                                               fg_color = FG_COLOR,
                                               bg_color = "transparent"
                                               )
        
        self.download_button = ctk.CTkButton(self.sideframe,
                                            width = 20,
                                            height = 20,
                                            fg_color = FG_COLOR,
                                            hover_color = HOVER_COLOR,
                                            corner_radius = 15,
                                            text = "",
                                            bg_color = FG_COLOR,
                                            image = ctk.CTkImage(dark_image = Image.open("asset/download.png"), size = (35, 35)),
                                            command = self.download
                                            )
        self.download_button.place(x = 9, y = 20)
        
        self.path_button = ctk.CTkButton(
            self.sideframe,
            width = 20,
            height = 20,
            fg_color = FG_COLOR,
            hover_color = HOVER_COLOR,
            corner_radius = 15,
            text = "",
            bg_color = FG_COLOR,
            image = ctk.CTkImage(dark_image = Image.open("asset/directory.png"), size = (35, 35)),
            command = self.browse_directory
        )
        self.path_button.place(x = 9, y = 80)

        self.setting_button = ctk.CTkButton(self.sideframe,
                                            width = 20,
                                            height = 20,
                                            fg_color = FG_COLOR,
                                            hover_color = HOVER_COLOR,
                                            corner_radius = 15,
                                            text = "",
                                            bg_color = FG_COLOR,
                                            image = ctk.CTkImage(dark_image = Image.open("asset/setting.png"), size = (35, 35)),
                                            command = self.settings
                                        )
        self.setting_button.place(x = 9, y = 140)
       
        self.url_entry = ctk.CTkEntry(self, 
                                      width = 450,
                                      height = 24,
                                      placeholder_text = "Enter the URL",
                                      text_color = TEXT_COLOR,
                                      placeholder_text_color = TEXT_COLOR,
                                      font = ('Roboto', 20),
                                      corner_radius = 15,
                                      fg_color = 'transparent',
                                      border_color = BORDER_COLOR)
        self.url_entry.place(x = 85, y = 30)        

        self.path_label = ctk.CTkLabel(self,
                                       fg_color = "transparent",
                                       textvariable = self.path,
                                       text_color = TEXT_COLOR,
                                       font = ("Roboto", 14))
        self.path_label.place(x = 88, y = 61)

    def download(self):    
        nHentai(self.url_entry.get()).main()
                    
    def update_userSetting(self, key, value):
        data = Parser().read_file()
        
        data['UserSetting'][key] = value
        
        with open(Parser().FILE, "w") as data_file:
            toml.dump(data, data_file)
    
    def browse_directory(self):
        directory = ctk.filedialog.askdirectory()
        self.path.set(directory)

        self.update_userSetting("CurrentPath", directory)
    
    def change_thread(self):
        self.update_userSetting("Parallelism", self.threads.get())

    def update_clearance(self):
        data = Parser().read_file()
        
        data['nHentai']['cf_clearance'] = self.clearanceEntry.get()
        
        with open(Parser().FILE, "w") as data_file:
            toml.dump(data, data_file)
            
    def update_token(self):
        data = Parser().read_file()
        
        data['nHentai']['csrftoken'] = self.tokenEntry.get()
        
        with open(Parser().FILE, "w") as data_file:
            toml.dump(data, data_file)

    def update_userAgent(self):
        data = Parser().read_file()
        
        data['nHentai']['User-Agent'] = self.agentEntry.get()
        
        with open(Parser().FILE, "w") as data_file:
            toml.dump(data, data_file)     
        
    def settings(self):
        if self.local_settingFrame.winfo_ismapped():
            self.local_settingFrame.place_forget()
            
        else:
            self.local_settingFrame.place(x = 85, y = 100)
            
            workerLabel = ctk.CTkLabel(self.local_settingFrame,
                                       text = "Number of Threads to use:",
                                       text_color = TEXT_COLOR,
                                       fg_color = 'transparent',
                                       font = ("Roboto", 16))
            workerLabel.place(x = 10, y = 15)
            
            worker2 = ctk.CTkRadioButton(self.local_settingFrame,
                                         value = 2,
                                         variable = self.threads,
                                         text = "2 Threads",
                                         border_color = BORDER_COLOR,
                                         fg_color = BORDER_COLOR,
                                         corner_radius = 90,
                                         width = 30,
                                         height = 30,
                                         border_width_checked = 7,
                                         border_width_unchecked = 1,
                                         hover_color = HOVER_COLOR,
                                         command = self.change_thread)
            worker2.place(x = 10, y = 40)
            
            worker3 = ctk.CTkRadioButton(self.local_settingFrame,
                                         value = 3,
                                         variable = self.threads,
                                         text = "3 Threads",
                                         border_color = BORDER_COLOR,
                                         fg_color = BORDER_COLOR,
                                         corner_radius = 90,
                                         width = 30,
                                         height = 30,
                                         border_width_checked = 7,
                                         border_width_unchecked = 1,
                                         hover_color = HOVER_COLOR,
                                         command = self.change_thread)
            worker3.place(x = 10, y = 65)
            
            clearanceLabel = ctk.CTkLabel(self.local_settingFrame,
                                       text = "cf_clearance Cookie: ",
                                       text_color = TEXT_COLOR,
                                       fg_color = 'transparent',
                                       font = ("Roboto", 16))
            clearanceLabel.place(x = 10, y = 95)
            
            self.clearanceEntry = ctk.CTkEntry(self.local_settingFrame,
                                          width = 350,
                                          height = 16,
                                          corner_radius = 15,
                                          border_width = 1,
                                          border_color = BORDER_COLOR,
                                          fg_color = "transparent",
                                          bg_color = "transparent",
                                          placeholder_text = "Enter your cf_clearance",
                                          placeholder_text_color = TEXT_COLOR,
                                          font = ("Roboto", 14))
            self.clearanceEntry.place(x = 10, y = 120)

            clearanceSave = ctk.CTkButton(self.local_settingFrame,
                                          width = 20,
                                          height = 20,
                                          corner_radius = 15,
                                          hover_color = HOVER_COLOR,
                                          fg_color = FG_COLOR,
                                          bg_color = FG_COLOR,
                                          text = "",
                                          image = ctk.CTkImage(dark_image = Image.open("asset/pin.png"), size = (20, 20)),
                                          command = self.update_clearance)
            clearanceSave.place(x = 360, y = 117)
            
            tokenLabel = ctk.CTkLabel(self.local_settingFrame,
                                       text = "csrftoken Cookie: ",
                                       text_color = TEXT_COLOR,
                                       fg_color = 'transparent',
                                       font = ("Roboto", 16))
            tokenLabel.place(x = 10, y = 150)
            
            self.tokenEntry = ctk.CTkEntry(self.local_settingFrame,
                                          width = 350,
                                          height = 16,
                                          corner_radius = 15,
                                          border_width = 1,
                                          border_color = BORDER_COLOR,
                                          fg_color = "transparent",
                                          bg_color = "transparent",
                                          placeholder_text = "Enter your csrftoken",
                                          placeholder_text_color = TEXT_COLOR,
                                          font = ("Roboto", 14))
            self.tokenEntry.place(x = 10, y = 175) 

            tokenSave = ctk.CTkButton(self.local_settingFrame,
                                          width = 20,
                                          height = 20,
                                          corner_radius = 15,
                                          hover_color = HOVER_COLOR,
                                          fg_color = FG_COLOR,
                                          bg_color = FG_COLOR,
                                          text = "",
                                          image = ctk.CTkImage(dark_image = Image.open("asset/pin.png"), size = (20, 20)),
                                          command = self.update_token)
            tokenSave.place(x = 360, y = 173)
            
            agentLabel = ctk.CTkLabel(self.local_settingFrame,
                                       text = "User-Agent Header: ",
                                       text_color = TEXT_COLOR,
                                       fg_color = 'transparent',
                                       font = ("Roboto", 16))
            agentLabel.place(x = 10, y = 205)
            
            self.agentEntry = ctk.CTkEntry(self.local_settingFrame,
                                          width = 350,
                                          height = 16,
                                          corner_radius = 15,
                                          border_width = 1,
                                          border_color = BORDER_COLOR,
                                          fg_color = "transparent",
                                          bg_color = "transparent",
                                          placeholder_text = "Enter your User-Agent",
                                          placeholder_text_color = TEXT_COLOR,
                                          font = ("Roboto", 14))
            self.agentEntry.place(x = 10, y = 230)  
            
            agentSave = ctk.CTkButton(self.local_settingFrame,
                                          width = 20,
                                          height = 20,
                                          corner_radius = 15,
                                          hover_color = HOVER_COLOR,
                                          fg_color = FG_COLOR,
                                          bg_color = FG_COLOR,
                                          text = "",
                                          image = ctk.CTkImage(dark_image = Image.open("asset/pin.png"), size = (20, 20)),
                                          command = self.update_userAgent)
            agentSave.place(x = 360, y = 227)
         
app = GUI()
