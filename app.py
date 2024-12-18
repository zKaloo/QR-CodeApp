import qrcode
import datetime
import os
import webbrowser
from tkinter import *
import tkinter.font as tkFont
from PIL import Image, ImageTk
from pathlib import Path
from discord_webhook import DiscordWebhook, DiscordEmbed


date = datetime.datetime.now()
current_date = f"{date.year}{date.month:02d}{date.day:02d}" # ChatGPT
maindir = Path(__file__).resolve().parent
counter = 1
disclaimer = True


def createdir():
    try:
        os.makedirs(maindir / f"images/{current_date}")
    except FileExistsError:
        pass
    except PermissionError:
        entrytextlabel.config(text=f"Ich konnte {current_date} nicht erstellen, da mir die Berechtigungen fehlen.")
    except Exception as e:
        entrytextlabel.config(text=f"Ein unerwarteter Fehler ist aufgetreten: {e}")


def createcode(input):
    global counter
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(input)
    qr.make(fit=True)

    if counter == 1:
        img = qr.make_image(fill_color="#ffffff", back_color="black")
        img = img.resize((330, 330))
        img.save(maindir / "placeholder.png")
    else:
        img = qr.make_image(fill_color="#ffffff", back_color="black")
        img = img.resize((330, 330))
        img.save(maindir / f"images/{current_date}/{counter}.png")
        entrytextlabel.config(text=f"{counter}.png wurde erfolgreich in {current_date} erstellt.")

    counter += 1
    return img


createcode("https://www.youtube.com/watch?v=dQw4w9WgXcQ")


def accept():
    global disclaimer
    disclaimer = False
    try:
        entrytextlabel.config(text="Bitte gib eine URL oder einen Text ein:", fg="white", bg="#4d7350")
    except:
        pass


def gen(entry):
    global disclaimer
    if disclaimer:
        app2 = Tk()

        app2.title("QR-Code Disclamer")
        app2.geometry("300x150")
        app2.iconbitmap("kalo.ico")
        app2.resizable(False, False)
        app2.config(bg="#4d7350")

        titlelabel = Label(app2, text="Bevor du einen QR-Code generieren kannst musst du \n folgende Bedingungen von mir (Kalo) akzeptieren: \n \n 1. Ich hafte nicht für die erstellten Inhalte. \n 2. Die Inhalte könnten möglicherweise von \n mir ausgelesen werden (außer bei '-nosend-').", fg="#ffffff", bg="#4d7350")
        titlelabel.pack()

        frame1 = Frame(app2, bg="#4d7350")
        frame1.config()
        frame1.pack(side=TOP)

        default_font = tkFont.nametofont("TkDefaultFont")
        default_font.configure(size=12)

        acceptbtn = Button(frame1, text="Akzeptieren", bg="black", fg="white", command=lambda: (accept(), app2.destroy()))
        acceptbtn.pack(side=LEFT)

        denybtn = Button(frame1, text="Ablehnen", bg="black", fg="white", command=lambda: app2.destroy())
        denybtn.pack(side=LEFT)

        app2.mainloop()

    else:
        if 8 < len(entry) < 1000:
            if entry.startswith("-nosend-"):
                createdir()
                entry = entry.replace("-nosend-", "")
                img = createcode(entry)
                img_tk = ImageTk.PhotoImage(img)
                imglabel.config(image=img_tk)
                imglabel.image = img_tk
                url_entry.delete(0, END)

            else:
                try:
                    webhook = DiscordWebhook(url="https://discord.com/api/webhooks/1318181452457709568/PwtZvG7gkO4ScSOKzrux49F0sEu0uo5EKcCgZCgf6opw5HimatbS1lT4nGCorFA7f9Au", rate_limit_retry=True)

                    embed = DiscordEmbed(title="QR-CODE // GENERIERT", description="Es wurde soeben ein neuer QR-Code mithilfe der Applikation generiert.", color="ffffff")
                    embed.add_embed_field(name="Inhalt", value=f"```{entry}```")
                    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/1067058909287817256/b9a1ca0d99675bf4614ca6795ca93f03.webp?size=240")
                    embed.set_footer(text="Entwickelt von zkalo")
                    embed.set_timestamp()

                    webhook.add_embed(embed)
                    response = webhook.execute()
                except:
                    pass

                createdir()
                img = createcode(entry)
                img_tk = ImageTk.PhotoImage(img)
                imglabel.config(image=img_tk)
                imglabel.image = img_tk
                url_entry.delete(0, END)

        else:
            entrytextlabel.config(text=f"Ungültige Eingabe, bitte versuche es erneut.")


app = Tk()

app.title("QR-Code Generator von Kaloyan Simeonov - 11 // V1.0")
app.geometry("500x500")
app.iconbitmap("kalo.ico")
app.resizable(False, False)
app.config(bg="#4d7350")

default_font = tkFont.nametofont("TkDefaultFont")
default_font.configure(size=12)

wlclabel = Label(app, text="Willkommen in dem QR-Code Generator.", fg="#ffffff", bg="#4d7350")
wlclabel.pack()

frame1 = Frame(app, bg="#4d7350")
frame1.config()
frame1.pack(side=BOTTOM, ipady=10)

frame2 = Frame(app)
frame2.pack(side=TOP)
img = ImageTk.PhotoImage(Image.open("placeholder.png"))
imglabel = Label(frame2, image=img, bg="black")
imglabel.pack()

frame3 = Frame(app, bg="#4d7350")
frame3.pack(side=TOP, pady=10)
entrytextlabel = Label(frame3, text="Bedingungen noch nicht akzeptiert. Klicke auf 'QR-Code generieren'.", fg="white", bg="#4d7350")
entrytextlabel.pack(pady=5)

entry_str = StringVar()
url_entry = Entry(frame3, textvariable=entry_str, justify=CENTER)
url_entry.focus_force()
url_entry.pack(pady=5)

generatebtn = Button(frame1, text="QR-Code generieren", bg="black", fg="white", command=lambda: gen(entry_str.get()))
generatebtn.pack(side=LEFT)

opendirbtn = Button(frame1, text="Verzeichnis öffnen", bg="black", fg="white", command=lambda: (createdir(), os.startfile(maindir / f"images/{current_date}"))) # ChatGPT
opendirbtn.pack(side=LEFT)

knowledgebtn = Button(frame1, text="Dokumentation", bg="black", fg="white", command=lambda: webbrowser.open("https://ohglandau-my.sharepoint.com/:w:/g/personal/kaloyansim_ohg-landau_info/EQjIz7zWM2lFswC1OtsVRBYBecMxa2-p7f7Ym9EJ_0RiCg?e=ZEsStg"))
knowledgebtn.pack(side=LEFT)

app.mainloop()
