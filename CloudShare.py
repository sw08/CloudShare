import tkinter as tk
import tkinter.font
from tkinter import filedialog
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from os.path import isfile, isdir, abspath
from tkinter import messagebox
from tkinter.ttk import Combobox, Progressbar, Notebook
from random import randint
import binascii
from threading import Thread

cred = credentials.Certificate('토큰 파일 경로')
firebase_admin.initialize_app(cred,{
    'databaseURL' : '저장소 URL'
})

root = tk.Tk()
root.title('CloudShare')
root.resizable(False, False)
root.geometry('275x325+100+100')
root.iconbitmap(abspath('logo.ico'))

tabs = Notebook(root)
tabs.pack(fill='both', expand=True)

uploadframe = tk.Frame(root, bd=0)
downloadframe = tk.Frame(root, bd=0)
infoframe = tk.Frame(root, bd=0)

tabs.add(uploadframe, text='업로드')
tabs.add(downloadframe, text='다운로드')
tabs.add(infoframe, text='정보')

titleFont = tkinter.font.Font(family="맑은 고딕", size=20, weight="bold")
contentFont = tkinter.font.Font(family='맑은 고딕', size=12)\

code = ''
binary = ''

def convertBase(number, base):
    T="0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    i,j=divmod(number,base)
    if i==0: return T[j]
    else: return convertBase(i,base)+T[j]

def addzero(c):
    for _ in range(6-len(c)):
        c = '0' + c
    return c

def create_code():
    global code
    a = randint(0, 2176782335)
    a_36 = convertBase(a, 36)
    dir = db.reference(addzero(str(a_36)))
    while dir.get() is not None:
        a = randint(0, 2176782335)
        a_36 = convertBase(a, 36)
        dir = db.reference(addzero(str(a_36)))
    a_36 = (a_36).upper()
    code = a_36

def controlHex(route):
    global binary
    with open(route, 'rb') as f:
        bin = f.read()
    binary = binascii.hexlify(bin)

def controlBinCode(route):
    code_thread = Thread(target=create_code)
    code_thread.setDaemon(True)
    code_thread.start()
    hex_thread = Thread(target=controlHex, args=(route,))
    hex_thread.setDaemon(True)
    hex_thread.start()

def collectUploadFile():
    route = filedialog.askopenfilename(initialdir="C:/", title='파일 선택')
    if route != '':
        UploadrouteEntry.delete(0, len(UploadrouteEntry.get()))
        UploadrouteEntry.insert(0, route)

def collectDownloadFile():
    route = filedialog.askdirectory(initialdir="C:/", title='폴더 선택')
    if route != '':
        DownloadrouteEntry.delete(0, len(DownloadrouteEntry.get()))
        DownloadrouteEntry.insert(0, route)

def uploadFile(route):
    if isfile(route):
        if CanusedCombo.get() not in ['1', '2', '3', '4', '5']:
            messagebox.showwarning("경고", '최대 파일 다운로드 횟수를 올바르게 입력해 주십시오')
            return
        global code
        global binary
        controlBinCode(route)
        print(code, binary)
        route = route.replace('\\\\', '/').replace('\\', '/')
        filename = route.split('/') 
        filename = filename[len(filename)-1]
        code = addzero(code)
        dir = db.reference()
        binary = str(binary)
        canused = str(CanusedCombo.get())
        try:
            dir.update({code:
                {"filename": filename,
                "fileHex": binary,
                "used": "0",
                "canused": canused}
            })
            UploadcodeLabel.configure(text=f'파일 다운로드 코드: {code}')
        except:
            messagebox.showerror('오류', '파일을 업로드할 수 없습니다')
    else:
        messagebox.showwarning("경고", "파일이 존재하지 않습니다.")

def downloadFile():
    code = (DownloadCodeEntry.get()).upper()
    dir = db.reference(code)
    if dir.get() is None:
        messagebox.showwarning("경고", "서버에서 파일을 찾을 수 없습니다")
        return
    if not isdir(DownloadrouteEntry.get()):
        messagebox.showwarning("경고", "다운로드 파일을 저장할 폴더를 찾을 수 없습니다")
        return
    data = dir.get()
    binary = data['fileHex']
    filename = data['filename']
    binary = eval(f"b'{binary[2:]}")
    binary = binascii.unhexlify(binary)
    with open(f'{DownloadrouteEntry.get()}/{filename}', 'wb') as f:
        f.write(binary)
    if int(data['used']) == int(data['canused']):
        dir.delete()
        return
    data['used'] = str(int(data['used']) + 1)
    dir.update(data)

UploadrouteEntry = tk.Entry(uploadframe, font=contentFont, bg="#ffffff", width=20)
UploadrouteBtn = tk.Button(uploadframe, text='찾아보기', command=collectUploadFile, font=contentFont)
UploadBtn = tk.Button(uploadframe, text='업로드', command=lambda: uploadFile(UploadrouteEntry.get()), font=contentFont)
CanusedCombo = Combobox(uploadframe, values=['1', '2', '3', '4', '5'], font=contentFont, state='readonly')
UploadcodeLabel = tk.Label(uploadframe, font=contentFont, text='')

UploadrouteEntry.pack(pady=10, padx=20, fill='x')
UploadrouteBtn.pack()
CanusedCombo.pack(pady=10)
UploadBtn.pack()
UploadcodeLabel.pack(pady=20)

Label1 = tk.Label(downloadframe, text='다운로드할 폴더')
DownloadCodeEntry = tk.Entry(downloadframe, font=contentFont, bg='#ffffff')
DownloadBtn = tk.Button(downloadframe, text='다운로드', command=downloadFile, font=contentFont)
Label2 = tk.Label(downloadframe, text='다운로드 코드')
DownloadrouteEntry = tk.Entry(downloadframe, font=contentFont, bg="#ffffff", width=20)
DownloadrouteBtn = tk.Button(downloadframe, text='찾아보기', command=collectDownloadFile, font=contentFont)

Label1.pack(pady=10)
DownloadrouteEntry.pack()
DownloadrouteBtn.pack(pady=10)
Label2.pack()
DownloadCodeEntry.pack(pady=10)
DownloadBtn.pack()

makerLabel = tk.Label(infoframe, text='제작: Studio Orora', font=titleFont)
versionLabel = tk.Label(infoframe, text='버전: 1.0', font=titleFont)
makerLabel.pack()
versionLabel.pack()

CanusedCombo.set("다운로드 가능 횟수")
print(db.reference('/').delete())
root.mainloop()
