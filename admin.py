# -*- mini-projet -*-
# Author: Paolo De Keyzer/Thibault Kiss
# Version: 14/11/2015

from tkinter import *
import urllib.request
import json



# Class for the main frame
class App(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.pack()
        self.createwidgets()
    
    def createwidgets(self):
        # Listbox for URLs
        self.__listbox = Listbox(self)
        self.__listbox.pack()
        with open ("database.json","r+") as Results:
            database = json.load(Results)
        for serie in database:
            self.__listbox.insert(END, serie+" ("+ database[serie]['name']+')')
        # Add a link control frame
        f = Frame(self)
        Label(f, text='Abbreviation').pack()
        self.__name=Entry(f)
        self.__name.pack()
        Label(f, text='Saison').pack(side=LEFT)
        self.__season = Entry(f)
        self.__season.pack(side=LEFT)
        Label(f, text='Episode').pack(side=LEFT)
        self.__episode = Entry(f)
        self.__episode.pack(side=LEFT)
        Button(f, text='Changer', command=self.addlink).pack()
        f.pack()

    def addlink(self):
        # Changement du statut de la série
        try:
            name = self.__name.get()
            season = self.__season.get()
            episod =self.__episode.get()

            #ouverture de la database
            with open("database.json","r+") as settingsData:
                settings = json.load(settingsData)
                #remplacement des ancirennes valeurs par celles insérées dans les Entry
                settings[name]['Season'] = season
                settings[name]['episode']=episod

                settingsData.seek(0)
                settingsData.write(json.dumps(settings,indent=2,sort_keys=True))
                settingsData.truncate()
        except:
            #une fenêtre s'ouvre en cas de mauvais nom de série
            warning=Tk()
            warning.title("Attention")
            Label(warning,text="Valeur entrée invalide").pack()
            Button(warning,text="Ok",command=warning.destroy).pack()




# Launch the application
window = Tk()
app = App(window)
app.mainloop()
