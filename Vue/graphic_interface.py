from PIL import ImageTk
import PIL.Image
import os
from Controller.Controller import *
from tkinter import *
from email_validator import validate_email, EmailNotValidError

# Color palette & variables

root = Tk()
root.minsize(1400,800)
root.geometry("1400x800")
root.title("Operatory : the opera repertory")
root.iconbitmap(".\\Images\\icon_2gps2.ico")

theme = "Dark"

C_BACKGROUND    = None
C_CASE_COLOR_BG = None
C_LINE_COLOR    = None
C_COLOR_BUTTON  = None
C_TEXT_COLOR_2  = None
C_TEXT_COLOR    = None
C_RED           = "#E21111"

def switch_theme(): #changer le thème (sombre et clair)
    global current_page, theme, C_BACKGROUND, C_CASE_COLOR_BG, C_LINE_COLOR, C_COLOR_BUTTON, C_TEXT_COLOR_2, C_TEXT_COLOR, C_RED, C_TEXT_COLOR, C_COLOR_BUTTON, C_TEXT_COLOR, C_TEXT_COLOR, C_TEXT_COLOR_2, C_CASE_COLOR_BG
    if theme == "Dark":
        C_BACKGROUND    = "gainsboro"
        C_CASE_COLOR_BG = "whitesmoke"
        C_LINE_COLOR    = "darkgray"
        C_TEXT_COLOR_2  = "black"
        C_TEXT_COLOR    = "black"
        C_COLOR_BUTTON  = "#AAAAAA"
        
        theme = "Light"
    else:
        C_BACKGROUND    = "#212325"
        C_CASE_COLOR_BG = "#3A3D3E"
        C_LINE_COLOR    = "#4B4D4F"
        C_TEXT_COLOR_2  = "#D4D4D4"
        C_TEXT_COLOR    = "#FFFFFF"
        C_COLOR_BUTTON  = "#4466EE"
        
        theme = "Dark"
        
    root.configure(bg =  C_BACKGROUND)
    
switch_theme()
root.configure(bg =  C_BACKGROUND)
current_page = 0
n, i = 0, 0
user_login = StringVar()
user_password = StringVar()
user_theme = StringVar()
user_card_numbers = StringVar()
user_cryptogram = StringVar()
user_date = StringVar()
user_mail = StringVar()
popcorn = IntVar()
price = 0
popcorn_price = 0
admin_login = False

controller_load_json()

def load_logo(theme, path_image): #charger les logos en fonction du thème et d'un chemin
        path_image = "./Images/%s%s.png"%(path_image, theme)
        loaded_img = PIL.Image.open(path_image)
        resized_img = loaded_img.resize((595, 149))
        final_img = ImageTk.PhotoImage(resized_img)
        lbl = Label(root, bg = C_BACKGROUND)
        lbl.image = final_img  # This is were we anchor the img object
        lbl.configure(image = final_img, bg = C_BACKGROUND)
        lbl.pack(anchor = "center", pady = 10)
        
def return_image(article): #retourne et charge une image et si elle n'existe pas, une par défaut se place.
    path_image = f"./Images/{article[5]}"
    
    if not os.path.isfile(path_image):
        path_image = f"./Images/NoImage.png"
        
    loaded_img = PIL.Image.open(path_image)
    resized_img = loaded_img.resize((150, 150))
    final_img = ImageTk.PhotoImage(resized_img)
    return final_img
    
def validate(key): #permet de limiter le nombre de caractère en entrée dans une 'Entry'
        if len(key) <= 25:
            return True
        else:
            return False

vcmd = (root.register(validate),"%P")

def login(): #page d'enregistrement (où il faut entrer 'admin' et 'admin' pour avoir accès à la modification des spectacles)
    global n
    def check_registration(event = 0):
        global n, admin_login
        if user_login.get() == "admin"and user_password.get() == "admin":
            admin_login = True
            home()
        else:
            n+=1
            if n <= 1 :
                Label(inner, font = ("Bahnschrift SemiBold", 10), bg = C_CASE_COLOR_BG, fg = "red", text = "Incorrect username or password").pack(anchor = "center", pady = 10)
                
    for w in root.winfo_children():
        w.destroy()
    
    user_login.set("")
    user_password.set("")
    
    container = Frame(root, bg = C_CASE_COLOR_BG, borderwidth = 2, relief = "ridge")
    container.place(anchor = "center", relx = 0.5, rely = 0.5, width = 400, height = 300)

    inner = Frame(container, bg = C_CASE_COLOR_BG)
    inner.pack(anchor = "center", expand = True)

    Label(inner, bg =  C_CASE_COLOR_BG, text = "", justify = "left").pack(anchor = "w") #permet de crée un espacement dans les packs
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Username :", justify = "left").pack(anchor = "w")
    Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = ("key"), validatecommand = vcmd, textvariable = user_login).pack(pady = 10)
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Password :", justify = "left",).pack(anchor = "w")
    password_entry = Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = "key", validatecommand = vcmd, textvariable = user_password, show = "*")
    password_entry.pack(pady = 10)
    Button(container, text = "Validate ✓", font = ("Bahnschrift SemiBold", 11), command = check_registration, foreground =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, relief = RAISED).pack(pady = 20)
    Button(root, text = "Back", command = home, fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -10, y = 10, anchor = "ne")  
    Label(root, font = ("Bahnschrift SemiBold", 30), bg =  C_BACKGROUND, fg =  C_TEXT_COLOR, text = "Sign in").pack(fill = "x", anchor = "n", pady = 50)
    password_entry.bind('<Return>', check_registration)
    n = 0 #reset n when the login page is closed

def reservation(num): #page de réservation où il y a toute les informations des spectacles en détail
    global article
    
    for w in root.winfo_children():
        w.destroy()

    load_logo(theme,"Logo")
        
    Button(root, text = "Back", command = lambda:home(current_page), fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -10, y = 10, anchor = "ne")
    Frame(root, bg =  C_LINE_COLOR, relief = "ridge", borderwidth = 2).pack(side = "top", anchor = "center", fill = "x", padx = 160)

    article = controller_get_article(num)
    
    image_area = Frame(root, bg =  C_BACKGROUND, width = 100, height = 60)
    image_area.place(rely = 0.4, relx = 0.8, x = -300)
    
    parent_area = Frame(root, bg =  C_BACKGROUND, width = 700, height = 300)
    parent_area.place(x = 0, rely = 0.35, relx = 0.12)
    
    data_area = Frame(parent_area, bg =  C_CASE_COLOR_BG)
    data_area.pack(fill = Y, side = "right", padx = 10)

    info_area = Frame(parent_area, bg =  C_CASE_COLOR_BG)
    info_area.pack(fill = Y, side = "left")

    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Type :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Title :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Name :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Place :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Date :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Director :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Time & attendance :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Language :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Subtitle(s) :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Next date :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Standart seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Confort seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Premium seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = "Popcorn Price :").pack(side = "top", anchor = "w")
     
    Label(data_area, font = ("Bahnschrift Bold", 15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[0]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[1]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[2]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[3]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[4]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[6]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[7]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[8]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[9]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[10]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[11]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[12]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[13]).pack(side = "top", anchor = "w")
    Label(data_area, font = ("Bahnschrift",      15), bg = C_CASE_COLOR_BG, fg = C_TEXT_COLOR, text = article[14]).pack(side = "top", anchor = "w")
     
    Button(root, text = "Order now", bg = C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = lambda:payment(num)).pack(anchor = "s", pady = 35, side = "bottom")
    
    path_image = f"./Images/{article[5]}"
    if not os.path.isfile(path_image):
        path_image = f"./Images/NoImage.png"
    
    loaded_img = PIL.Image.open(path_image)
    resized_img = loaded_img.resize((300, 300))
    final_img = ImageTk.PhotoImage(resized_img)
    lbl = Label(image_area, bg =  C_CASE_COLOR_BG)
    lbl.image = final_img  # This is were we anchor the img object
    lbl.configure(image = final_img, bg =  C_CASE_COLOR_BG, height = 300, width = 300)
    lbl.pack(anchor = "e", padx = 110)

def payment(num): #page du paiement
    global user_card_numbers, user_cryptogram, user_date, user_mail, popcorn, inner, i

    validate_price_button = None
    def check_payment():
        
        def check_mail(mail):
            try:
                # Validating the `testEmail`
                emailObject = validate_email(mail)

                # If the `testEmail` is valid
                # it is updated with its normalized form
                mail = emailObject.email
                return True
            except EmailNotValidError as errorMsg:
                # If `testEmail` is not valid
                # we print a human readable error message
                return False
            
        def check_date(date:str):
            
            date = date.split("/")
            if len(date) != 2:
                return False
            
            if not date[0].isdigit():
                return False
            if int(date[0]) > 31:
                return False
            if int(date[0]) < 1:
                return False
            
            if not date[1].isdigit():
                return False
            if int(date[1]) > 30:
                return False
            if int(date[1]) < 23: 
                return False
        
            return True
        
        def check_cryptogram(crypto:str):
            if not crypto.isdigit():
                return False
            if int(crypto) > 999:
                return False
            if int(crypto) < 1:
                return False
            return True
        
        def check_card_number(card_number:str):
            card_number = card_number.replace(" ","")
            if not card_number.isdigit() :
                return False
            if len(card_number) != 16:
                return False
            return True
        
        global i
        print(check_mail(user_mail.get()), check_card_number(user_card_numbers.get()), check_cryptogram(user_cryptogram.get()), check_date(user_date.get()))
        if check_mail(user_mail.get()) == False or check_card_number(user_card_numbers.get()) == False or check_cryptogram(user_cryptogram.get()) == False or check_date(user_date.get()) == False or price <= 0 or optlistvar2.get() == 'Select date' :
            i+=1
            if i<=1:
                Label(inner, font = ("Bahnschrift SemiBold", 10), bg =  C_CASE_COLOR_BG, fg = "red", text = "Incorrect informations").pack(anchor = "center", side = "bottom")
        else:
            print(user_card_numbers.get(), user_date.get(), user_cryptogram.get(), user_mail.get(), price, controller_articles()[num][1])
            controller_payment_manage(user_card_numbers.get(), user_date.get(), user_cryptogram.get(), user_mail.get(), price, controller_articles()[num][1], optlistvar2.get())
            for w in root.winfo_children():
                w.destroy()

            Label(root, font = ("Bahnschrift", 15), bg =  C_BACKGROUND, text = "").pack(side = "top",pady = 160)
            Label(root, font = ("Bahnschrift", 15), bg =  C_BACKGROUND, fg = "limegreen", text = "The order has been completed for the amount of %.2f€"%price).pack(side = "top", anchor = "center")
            Label(root, font = ("Bahnschrift", 13), bg =  C_BACKGROUND, fg =  C_TEXT_COLOR, text = "An email has been sent to you to recap your order").pack(anchor = "center",pady = 10)
            Button(root, text = "Back to the menu", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = home).pack(anchor = "center", pady = 20)
    
    def get_price(price:str):
        i = 0
        tmp = ""
        price = price.replace(",",".")
        ban_characters = [".",""]
        
        while i < len(price):
            if price[i].isdigit():
                break
            i += 1
            
        while i < len(price):
            if not price[i].isdigit() and price[i] not in ban_characters:
                break
            tmp += price[i]
            i += 1
            
        return float(tmp) 
                
    def price_calculator(_=None):
        global price, popcorn_price
        
        price = 0
        popcorn_price = 0
        
        if optlistvar.get() == "Standart seat":
            price = get_price(article[11])
        if optlistvar.get() == "Confort seat":
            price = get_price(article[12])
        if optlistvar.get() == "Premium seat":
            price = get_price(article[13])
            
        if popcorn.get() == 1:
            popcorn_price += get_price(article[14])
        if popcorn.get() == 0:
            popcorn_price = 0
            
        price += popcorn_price
        
        if price > 0:    
            validate_price_button.config(text = "Validate %.2f € ✓"%price)
        else:
            validate_price_button.config(text = "Validate ✓")
        
    for w in root.winfo_children():
        w.destroy()
        
    user_card_numbers.set("")
    user_cryptogram.set("")
    user_date.set("")
    user_mail.set("")
    popcorn.set(0)
    
    container = Frame(root, bg =  C_CASE_COLOR_BG, borderwidth = 2, relief = "ridge")
    container.place(anchor = "center", relx = 0.5, rely = 0.61, width = 400, height = 550)
    
    inner = Frame(container, bg =  C_CASE_COLOR_BG)
    inner.pack(anchor = "center", expand = True)

    option_list = ("Standart seat","Confort seat","Premium seat")
    optlistvar = StringVar()
    optlistvar.set("Select seat quality")
    
    option_list2 = ("7 january 2023","10 january 2023","16 january 2023")
    optlistvar2 = StringVar()
    optlistvar2.set("Select date")
    
    Button(root, text = "Back", command =  lambda:reservation(num), fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -10, y = 10, anchor = "ne")
    load_logo(theme,"LogoSecurity")
    Frame(root, bg =  C_LINE_COLOR, relief = "ridge", borderwidth = 2).pack(side = "top", anchor = "center", fill = "x", padx = 160)
    
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Mail :", justify = "left").pack(anchor = "w", pady = 10)
    Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = "key", validatecommand = vcmd, textvariable = user_mail).pack(pady = 6)
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Card number :", justify = "left").pack(anchor = "w", pady = 3)
    Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = "key", validatecommand = vcmd, textvariable = user_card_numbers).pack(pady = 6)
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "CVC code :", justify = "left").pack(anchor = "w", pady = 3)
    Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = "key", show = "*", validatecommand = vcmd, textvariable = user_cryptogram).pack(pady = 6)
    Label(inner, font = ("Bahnschrift SemiBold", 16), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Expiration date :", justify = "left",).pack(anchor = "w", pady = 3)
    Entry(inner, bg =  C_LINE_COLOR, width = 25, fg =  C_TEXT_COLOR, font = ("Bahnschrift SemiBold", 14), justify = "center", validate = "key", validatecommand = vcmd, textvariable = user_date).pack(pady = 6)
    
    menu_options = OptionMenu(inner, optlistvar, *option_list, command = price_calculator)
    menu_options.config(width = 20,font = ("Bahnschrift SemiBold", 10), fg =  C_TEXT_COLOR, bg =  C_CASE_COLOR_BG, activebackground =  C_CASE_COLOR_BG, activeforeground =  C_TEXT_COLOR, highlightbackground =  C_CASE_COLOR_BG, relief = SOLID, border = 2)
    menu_options.pack(pady = 10)

    menu_options2 = OptionMenu(inner, optlistvar2, *option_list2, command = price_calculator)
    menu_options2.config(width = 20,font = ("Bahnschrift SemiBold", 10), fg =  C_TEXT_COLOR, bg =  C_CASE_COLOR_BG, activebackground =  C_CASE_COLOR_BG, activeforeground =  C_TEXT_COLOR, highlightbackground =  C_CASE_COLOR_BG, relief = SOLID, border = 2)
    menu_options2.pack()
    
    Checkbutton(inner, font = ("Bahnschrift SemiBold", 13), command = price_calculator, text = "Popcorn", fg =  C_TEXT_COLOR, bg =  C_CASE_COLOR_BG, var = popcorn, onvalue = 1, offvalue = 0, activebackground =  C_CASE_COLOR_BG, selectcolor =  C_LINE_COLOR, activeforeground =  C_TEXT_COLOR).pack(pady = 10)
    validate_price_button = Button(container, text = "Validate ✓", font = ("Bahnschrift SemiBold", 11), command = check_payment, foreground =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, relief = RAISED)
    validate_price_button.pack(pady = 10)
    i = 0 #reset i when the page is closed
    
def admin_edit(num, create = False): #page permettant la modification des spectacles si tu es admin
    global article
    
    for w in root.winfo_children():
        w.destroy()

    load_logo(theme,"LogoCreator")
    Button(root, text = "Back", command = home, fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -10, y = 10, anchor = "ne")
    Frame(root, bg =  C_LINE_COLOR, relief = "ridge", borderwidth = 2).pack(side = "top", anchor = "center", fill = "x", padx = 160)

    article = controller_get_article(num)
    
    parent_area = Frame(root, bg = C_BACKGROUND)
    parent_area.place(rely = 0.5, relx = 0.5, x = -323, y = -160)
    
    data_area = Frame(parent_area, bg =  C_CASE_COLOR_BG)
    data_area.pack(fill = Y, side = "right", padx = 10)

    info_area = Frame(parent_area, bg =  C_CASE_COLOR_BG)
    info_area.pack(fill = Y, side = "left")
    
    var_entry_00 = StringVar(value = "%s"%article[0])
    var_entry_01 = StringVar(value = "%s"%article[1])
    var_entry_02 = StringVar(value = "%s"%article[2])
    var_entry_03 = StringVar(value = "%s"%article[3])
    var_entry_04 = StringVar(value = "%s"%article[4])
    var_entry_05 = StringVar(value = "%s"%article[5])
    var_entry_06 = StringVar(value = "%s"%article[6])
    var_entry_07 = StringVar(value = "%s"%article[7])
    var_entry_08 = StringVar(value = "%s"%article[8])
    var_entry_09 = StringVar(value = "%s"%article[9])
    var_entry_10 = StringVar(value = "%s"%article[10])
    var_entry_11 = StringVar(value = "%s"%article[11])
    var_entry_12 = StringVar(value = "%s"%article[12])
    var_entry_13 = StringVar(value = "%s"%article[13])
    var_entry_14 = StringVar(value = "%s"%article[14])
    
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Type :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Title :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Name :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Place :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Date :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Image :").pack(side = "top", anchor = "w")  
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Director :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Time & attendance :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Language :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Subtitle(s) :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Next date :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Standart seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Confort seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Premium seat price :").pack(side = "top", anchor = "w")
    Label(info_area, font = ("Bahnschrift", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, text = "Popcorn Price :").pack(side = "top", anchor = "w")
    
    Entry(data_area, font = ("Bahnschrift Bold", 15), bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_00, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_01, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_02, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_03, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_04, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_05, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_06, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_07, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_08, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_09, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_10, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_11, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_12, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_13, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    Entry(data_area, font = ("Bahnschrift", 15),      bg =  C_CASE_COLOR_BG, fg =  C_TEXT_COLOR, textvariable = var_entry_14, width = 40, border = 1).pack(side = "top", anchor = "w", padx = 0, pady = 1)
    
    def delete_article():
        articles = controller_articles()
        articles.pop(num)
        controller_save_json()
        home()
    
    def validate_editing():
        
        article[ 0] = var_entry_00.get()
        article[ 1] = var_entry_01.get()
        article[ 2] = var_entry_02.get()
        article[ 3] = var_entry_03.get()
        article[ 4] = var_entry_04.get()
        article[ 5] = var_entry_05.get()
        article[ 6] = var_entry_06.get()
        article[ 7] = var_entry_07.get()
        article[ 8] = var_entry_08.get()
        article[ 9] = var_entry_09.get()
        article[10] = var_entry_10.get()
        article[11] = var_entry_11.get()
        article[12] = var_entry_12.get()
        article[13] = var_entry_13.get()
        article[14] = var_entry_14.get()
        
        controller_save_json()
        home()
        
    suppr_frame = Frame(root, bg =  C_BACKGROUND)
    suppr_frame.pack(anchor = "s", pady = 35, side = "bottom")
    
    Button(suppr_frame, text = "Delete", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = delete_article).pack(side = "left", anchor = "n", padx = 10)
    Button(suppr_frame, text = "Save ✓", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = validate_editing).pack(side = "right", anchor = "n", padx = 10)

def home(page = 0): #page d'accueil
    global current_page
    current_page = page
    ARTICLE_WIDTH  = 300
    ARTICLE_HEIGHT = 160
    NB_ARTICLES_H = 3 # Number of articles to display horizontally
    NB_ARTICLES_V = 2 # Number of articles to display vertically
    NB_ARTICLES_PER_PAGE = NB_ARTICLES_H * NB_ARTICLES_V

    for w in root.winfo_children():
        w.destroy()
    root.bind("<Escape>", root.quit)
    
    def logout():
        global admin_login
        admin_login = False
        home()
    
    if admin_login:
        Button(root, font = ("Bahnschrift SemiBold", 12), text = "Logout", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = logout).place(x = 10, y = 10)
        load_logo(theme,"LogoCreator")
    else:
        Button(root, font = ("Bahnschrift SemiBold", 12), text = "Login", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = login).place(x = 10, y = 10)
        load_logo(theme,"Logo")
    
    def change_theme():
        switch_theme()
        home(current_page)
        
    Button(root, text = "Theme : %s"%("Dark"if theme == "Light"else"Light"), command = change_theme, fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -50, y = 10, anchor = "ne")
    Button(root, text = "Back", command = root.destroy, fg =  C_TEXT_COLOR, bg =  C_COLOR_BUTTON, font = ("Bahnschrift SemiBold", 10)).place(relx = 1, x = -10, y = 10, anchor = "ne")
    Frame(root, bg =  C_LINE_COLOR, relief = "ridge", borderwidth = 2).pack(side = "top", anchor = "center", fill = "x", padx = 160)

    nb_page = (len(controller_articles()) + 5) // NB_ARTICLES_PER_PAGE

    container = Frame(root, bg =  C_BACKGROUND)
    container.pack(expand = True, fill = "both")

    footer = Frame(root, bg =  C_BACKGROUND, width = 100, height = 60)
    footer.pack(anchor = "s", side = "bottom", pady = 10)

    for i in range(nb_page):
        Button(footer, text = str(i+1), bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = lambda x = i: home(x)).pack(side = "left", padx = 3)
        
    if admin_login:
        def add_container():
            controller_empty_article()
            admin_edit(len(controller_articles())-1, create = True)
        
        Button(root, text = "Add container", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = add_container).pack(side = "bottom", anchor = "s", pady = 4)
    
    line = 0
    column = 0
    articles = controller_articles()
    for i in range(page * NB_ARTICLES_PER_PAGE, min(len(articles), (page+1) * NB_ARTICLES_PER_PAGE)):
        article = articles[i]

        relx = (1/(NB_ARTICLES_H*2)) * (column*2+1)
        rely = (1/(NB_ARTICLES_V*2)) * (line*2+1)

        item = Frame(container, width = ARTICLE_WIDTH, height = ARTICLE_HEIGHT, bg =  C_CASE_COLOR_BG, relief = "ridge", borderwidth = 1, highlightthickness = 2, highlightbackground = "#7A7A7A")
        item.place(anchor = "center", relx = relx, rely = rely, width = 450, height = 250)

        leftpart = Frame(item, bg =  C_CASE_COLOR_BG)
        leftpart.pack(side = "left", fill = "both", expand = True)

        rightpart = Frame(item, bg =  C_CASE_COLOR_BG)
        rightpart.pack(side = "right", fill = "y")

        text = " %s\n\n %s\n\n %s\n\n %s"%(article[1], article[2], article[3], article[4])
        Label(leftpart, text = "\n%s"%article[0], font = ("Product Sans", 15,"bold"), fg =  C_TEXT_COLOR, bg =  C_CASE_COLOR_BG).pack(anchor = "center", padx = 10)
        Label(leftpart, text = text, font = ("Product Sans", 10,"bold"), fg =  C_TEXT_COLOR_2, bg =  C_CASE_COLOR_BG, justify = "left").pack(expand = True, anchor = "w", padx = 10)

        final_img = return_image(article)
        lbl = Label(rightpart, bg =  C_CASE_COLOR_BG)
        lbl.image = final_img  # This is were we anchor the img object
        lbl.configure(image = final_img, bg =  C_CASE_COLOR_BG, height = 150, width = 150)
        lbl.pack(anchor = "center", pady = 20, padx = 20)
        
        button_frame = Frame(rightpart, bg =  C_CASE_COLOR_BG)
        button_frame.pack(anchor = "s", pady = 10, side = "bottom")
        
        Button(button_frame, text = "Discover", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = lambda x = i: reservation(x)).pack(side = "left", anchor = "n", padx =  3)
        
        if admin_login:
            Button(button_frame, text = "Edit", bg =  C_COLOR_BUTTON, fg =  C_TEXT_COLOR, command = lambda x = i: admin_edit(x)).pack(side = "left", anchor = "n", padx =  3)
            
        column += 1
        if column >= NB_ARTICLES_H:
            column = 0
            line += 1
        if line >= NB_ARTICLES_V:
            break

home()
root.mainloop()