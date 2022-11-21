#-*- coding: utf-8 -*-

import tkinter as tk
from tkinter import font,ttk
import os,webbrowser,sys,json,time
from requests_handler import *

def get_tl_id(team_mappings,team):
    for key in team_mappings:
        if key.startswith(team.lower())==True:
            return team_mappings[key]
            break
    else:
        return ['TeamNotFound','LeagueNotFound']

def dat_format(utc):
    mth_mappings = {1:'January',2:'February',3:'March',4:'April',5:'May',
            6:'June',7:'July',8:'August',9:'September',10:'October',
            11:'November',12:'December'}
    yr,mth,day = str(utc[:4]),str(utc[5:7]),str(utc[8:10])
    utctime = utc[11:16]
    loc_hr = int(utctime[:2])+6
    if (loc_hr > 24):
        loc_time = str(loc_hr-24)+':'+utctime[3:]
    elif (loc_hr == 24):
        loc_time = '00:'+utctime[3:]
    else:
        loc_time = str(loc_hr)+':'+utctime[3:]
    text = ('starts on '+day+' '+mth_mappings[int(mth)]+','+' at'+' '+loc_time+
            ' '+'localTime')
    return text

def stan_format(key,league_id,canvas):
    data,count = standings(key,league_id)
    text = ('\n'+3*' '+ ' Team'+23*' '+'PL'+' '+'WN'+' '+'DR'+' '+'LS'+' '+'PT'+' '+
            'GLD'+'\n'+50*'-'+'\n')
    for i in range(1,5):
        team_name = data[i][0]
        extra_whitespaces = (27-len(team_name))*'.'
        text += (' '+str(i).rjust(2)+'.'+team_name+extra_whitespaces+str(data[i][1]).rjust(2)+' '+
                str(data[i][2]).rjust(2)+
                ' '+str(data[i][3]).rjust(2).rjust(2)+' '+
                str(data[i][4]).rjust(2)+' '+str(data[i][5]).rjust(2)+' '+
                str(data[i][6]).rjust(3)+'\n')
    for i in range(count-2,count+1):
        index = i
        team_name = data[index][0]
        extra_whitespaces = (27-len(team_name))*'.'
        text += (' '+str(i).rjust(2)+'.'+team_name+extra_whitespaces+str(data[index][1]).rjust(2)+' '+
                str(data[index][2]).rjust(2)+' '+str(data[index][3]).rjust(2)+
                ' '+str(data[index][4]).rjust(2)+
                ' '+str(data[index][5]).rjust(2)+' '+
                str(data[index][6]).rjust(3)+'\n')
    canvas.itemconfigure(canv_text,text=text,justify='left',fill='#bf4040',
            font=('Lucida Console',10,'normal'),width=405)

def fix_format(key,team,canvas):
    global team_id,league_id
    tl = get_tl_id(team_mappings,team)
    team_id = tl[0]
    league_id = tl[1]
    data = fixtures(key,team_id)
    try:
        mday,utc,hteam,ateam = str(data['mday']),data['utc'],data['hteam'],data['ateam']
        matchday = 'Matchday-'
        if mday == 'None':
            matchday = 'ϟChampions Leagueϟ'
            mday = ''
        text = matchday+mday+'\n'+len(matchday+mday)*'.'+'\n'+hteam+' '+'<vs>'+' '+ateam+'\n'+dat_format(utc)
        font_size,fg_col = 13,'#159e8e'
    except:
        if team_id == 'TeamNotFound':
            text,font_size,fg_col = 'ERROR: Check your spelling and have a look at the READ_ME.txt file',12,'#e6196b'
        else:
            text,font_size,fg_col = data,12,'#ff0000'
    canvas.itemconfigure(canv_text,text=text,justify='left',fill=fg_col,font=('Consolas',font_size,'normal'),width=405)

def res_format(key,team_id,canvas):
    data = results(key,team_id)
    data_len = len(data)
    text = ''
    team_len_0 = len(sorted([data[x][0][0] for x in range(data_len)],key=len,reverse=True)[0])
    team_len_1 = len(sorted([data[x][1][0] for x in range(data_len)],key=len,reverse=True)[0])
    if(team_len_0>team_len_1):
        max_team_len = team_len_0
    else:
        max_team_len = team_len_1
    data.reverse()
    for i in range(data_len):
        hteam = data[i][0][0]
        ateam = data[i][1][0]
        hscore= str(data[i][0][1])
        ascore= str(data[i][1][1])
        pscore= data[i][2]
        extra_whitespaces = max_team_len - len(hteam)
        hteam+= extra_whitespaces*' '
        text += hteam+' '+hscore+':'+ascore+'  '+ateam+pscore+'\n'
    font_size = 12
    if max_team_len>20:
        font_size = 10
    canvas.itemconfigure(canv_text,text=text,justify='left',fill='#8080ff',font=('Consolas',font_size,'normal'),width=405)

def restart_script():
    os.execv(sys.executable, ['Python'] + sys.argv)

def callback():
    webbrowser.open_new('https://www.football-data.org/client/register')

def custom_font(family='consolas',weight='normal',size=14):
    return font.Font(family=family,weight=weight,size=size)

def write_key(key):
    key_dict = {
            'key':key,
            'default_team':'Real Madrid CF'
            }
    with open('config.json','w') as file:
        json.dump(key_dict,file)
        file.close()

def main_window(label=False,img_path=None):
    global root
    wt,ht = 450,150
    root = tk.Tk()
    root.resizable(False,False)
    root.title('argon')
#    root.geometry('-5+5')
    root.geometry('-300+100')
#    root.iconbitmap('./graphix/isthatit.ico')
    canvas = tk.Canvas(root,height=ht,width=wt)
    canvas.pack()
    if label == True:
        bg_img = tk.PhotoImage(file=img_path)
        bg_label = tk.Label(root,image=bg_img)
        bg_label.image = bg_img     #keeping a ref so the thing works
        bg_label.place(relwidth=1,relheight=1)

try:
    with open('config.json',mode='r',encoding='utf-8') as config, open('team_codes.json',encoding='ISO-8859-1') as team_codes:
        user_info = json.load(config)
        config.close()
        team_mappings = json.load(team_codes)
    key = user_info['key'].strip()
    default_team = user_info['default_team']
    main_window()
    top_frame = tk.Frame(root,bg='#262626')
    top_frame.place(relwidth=1,relheight=1)

    bottom_canvas = tk.Canvas(top_frame,bg='#262626',bd=0,highlightthickness=0)
    bottom_canvas.place(relx=0.05,rely=0.22,relheight=0.765,relwidth=0.9)
    img = tk.PhotoImage(file='graphix/champ.png')
    canv_img = bottom_canvas.create_image(205,60,image=img)
    canv_text =bottom_canvas.create_text(205,60,justify='left')
    team_name = tk.StringVar()
    team_name.set(default_team)
    team_entry = tk.Entry(top_frame,textvariable=team_name,bg='#262626',fg='#737373',font=
                custom_font('Consolas','normal','10'),insertbackground='#e6196b',
                insertofftime=0,bd=2,relief='groove')
    team_entry.bind("<Enter>",lambda e:team_entry.config(highlightthickness=1,
                highlightbackground='#e6196b', highlightcolor='#e6196b',bd=0))
    team_entry.bind("<Leave>",lambda e:team_entry.config(highlightthickness=0,bd=2))
    #team_entry.insert(0,'Enter team-name and hit enter')
    team_entry.bind("<FocusIn>",lambda e:team_entry.delete(0,'end') or team_entry.config(fg='#e6e6e6',font=custom_font('Consolas','bold',12)))
    team_entry.place(relx=0.05,rely=0.05,relwidth=0.40,relheight=0.15)
    team_entry.bind("<Return>",lambda e: fix_format(key,team_entry.get(),bottom_canvas)or ki_chan.set('fixture'))


    ki_chan = tk.StringVar()
    ki_chan.set('fixture')
    style = ttk.Style()
    style.configure("TRadiobutton",background="#262626",foreground="#a64dff",
              font=('Consolas',8,'bold'),indicatorbackground='#ffffff')
    radio_1 = ttk.Radiobutton(top_frame,text="Fixture",variable=ki_chan,
              value="fixture",style='TRadiobutton',
              command=lambda :fix_format(key,team_entry.get(),bottom_canvas))
    radio_2 = ttk.Radiobutton(top_frame,text="Standings",variable=ki_chan,
              value="standings",style='TRadiobutton',
              command=lambda :stan_format(key,league_id,bottom_canvas))
    radio_3 = ttk.Radiobutton(top_frame,text="Results",variable=ki_chan,
              value="results",style='TRadiobutton',
              command=lambda :res_format(key,team_id,bottom_canvas))
    radio_1.place(relx=0.46,rely=0.065)
    radio_2.place(relx=0.625,rely=0.065)
    radio_3.place(relx=0.805,rely=0.065)

    root.after(100, lambda: fix_format(key,team_entry.get(),bottom_canvas))
    root.mainloop()

except FileNotFoundError:
    main_window(label=True,img_path='graphix/bgwall.png')
    API_Frame = tk.Frame(root,bg='#262626',bd='3',relief='flat',
            padx='0.3',pady='0.1')
    API_Frame.place(relx=0.5,rely=0.12,relwidth=0.80,relheight=0.78,anchor='n')

    text_label = tk.Label(API_Frame,bg='#262626',fg='#e6196b',text='Enter your API key:',
    font=custom_font('Consolas','bold','14'),bd=0,padx=5,pady=2 )
    text_label.place(relx=0,rely=0)

    key_entry = tk.Entry(API_Frame,bg='#262626',fg='#f2e5ff',
            insertbackground='#e6196b',font=custom_font('Consolas','normal','12')
            ,bd=2,relief='groove')
    key_entry.bind("<Enter>",lambda e:key_entry.config(highlightthickness=1,
              highlightbackground='#3385ff', highlightcolor='#3385ff',bd=0))
    key_entry.bind("<Leave>",lambda e:key_entry.config(highlightthickness=0,bd=2))
    key_entry.bind("<Return>",lambda e:write_key(key_entry.get()) or restart_script())
    key_entry.place(relx=0,rely=0.3,relwidth=0.75,relheight=0.2)

    link_label = tk.Label(API_Frame,bg='#262626',fg='#e6196b',
               text='>>Click here to get a key',
               font=custom_font('Consolas','normal',12),bd=0,padx=0)
    link_label.bind("<Button-1>",lambda e:callback())
    link_label.bind("<Enter>",lambda e:link_label.config(fg='#008080'))
    link_label.bind("<Leave>",lambda e:link_label.config(fg='#e6196b'))
    link_label.place(relx=0,rely=0.8)

    button = tk.Button(API_Frame,activebackground='#ffffff',activeforeground=
            '#000000',bg='#262626',fg='#e6196b',text='Done',
            font=custom_font('Consolas','normal',12),
            bd=2,relief='groove',
            command=lambda :write_key(key_entry.get()) or restart_script() )
    button.place(relx=0.79,rely=0.3,relheight=0.2)

    #root.attributes('-alpha',0.8)
    root.mainloop()




