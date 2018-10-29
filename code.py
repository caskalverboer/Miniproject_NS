#Importeren modules
from tkinter import *
import requests
import xmltodict

#Account invoeren om in te loggen op de API
username = 'jestin.vanhamond@student.hu.nl'
password = 'qDjrtZk4yNvuVLqyzBPqSVG5XkKTkxA-R3cnRa9_11erxyf1gJGGGQ'

#XML bestand openenen als deze bestaat / aanmaken als deze nog niet bestaat in 'write' modus
file = open('Reistijden.xml', 'w')
xmlFile='Reistijden.xml'

#Tekstvelden/inputvelden
stationVertrek = ''
stationBestemming = ''

# While loop zorgt ervoor dat de informatie uit de API pas wordt opgehaald wanneer op de knop gedrukt wordt
while len(stationVertrek) == 0:
    def clicked():
        global stationVertrek
        global stationBestemming
        stationVertrek = str(beginhalte.get())
        stationBestemming = str(eindhalte.get())
        quit_root()


    def quit_root():
        root.destroy()


    root = Tk()
    label = Label(master=root, text='', width=200, height=100, background='#fccc20', )
    # Maakt een window aan met een achtergrondkleur

    label.pack()
    root.title('Actuele vertrektijden NS')
    root.configure(background='#fccc20')
    root.resizable(width=False, height=False)
    root.geometry("890x350")

    # Plaatst het logo
    logo = PhotoImage(file="index.jpg")
    logo_label = Label(root, image=logo, background='#ffc61e')
    logo_label.place(x=10, y='-10')


    welkom = Label(master=root,
                   text='Welkom bij de NS reisplanner',
                   foreground='dark blue',
                   background='#fccc20',
                   font=('Helvetica', 20, 'bold'))
    beginlabel = Label(master=root,
                    text='Voer hier de beginhalte in:',
                    background='#fccc20',
                    font = ('Helvetica', 14, 'bold'))
    beginhalte = Entry(master=root, width=30)

    eindlabel = Label(master=root,
                    text='Voer hier de eindhalte in:',
                    background='#fccc20',
                    font=('Helvetica', 14, 'bold'))
    eindhalte = Entry(master=root, width=30)

    #Plaatst de widgets
    button1 = Button(root, text="Plan uw reis", command=clicked)
    button1.place(x=630, y=290)
    welkom.place(x=120, y=5)
    beginlabel.place(x=630, y=160)
    beginhalte.place(x=630, y=190)
    eindlabel.place(x=630, y=230)
    eindhalte.place(x=630, y=260)

    root.mainloop()
#dxddf

# Informatie ophalen uit API
url = ('https://webservices.ns.nl/ns-api-avt?station=' + stationVertrek)
r = requests.get(url, auth=(username, password))
file.writelines(r.content.decode("utf-8"))
file.close()


try:
    def processXML(filename):
        """XML bestand omzetten naar een dictionary"""

        with open(filename) as myXMLFILE:
            filecontentstring = myXMLFILE.read()
            xmldictionary = xmltodict.parse(filecontentstring)

            return xmldictionary

    stationsdict = processXML(xmlFile)

    stations = stationsdict['ActueleVertrekTijden']['VertrekkendeTrein']

    setReizen = []

    for var in stations:
        eindbestemming = var['EindBestemming']
        ritNummer = var['RitNummer']
        vertrekTijd = var['VertrekTijd']
        vertrekTijden = vertrekTijd[11:16]


        if eindbestemming == stationBestemming:
            x = stationVertrek
            y = stationBestemming
            z = vertrekTijden

            setReizen.append('De trein van ' + x + ' naar ' + y + ' vertrekt om: ' + z + ' met ritnummer: ' + ritNummer)
    print(len(setReizen))
    # Opent tkinter form met output
    root2 = Tk()
    root2.configure(background='#fccc20')
    t = Text(root2, width='77', height='20', bg='#fccc20', padx='10', spacing1='5')

    # Voor elk item in setReizen schrijf weg
    if len(setReizen) == 0:
        t.insert(END, 'Er zijn geen reizen beschikbaar voor dit vertrek-en eindpunt.')
    else:
        for x in setReizen:
            t.insert(END,x +'\n')

    t.pack()
    root2.mainloop()

except KeyError:
    print('Er is geen geldig vertrekstation of eindstation opgegeven.')

except FileNotFoundError:
    print('Dit bestand bestaat niet in de directory.')

except:
    print('Algemene fout.')

