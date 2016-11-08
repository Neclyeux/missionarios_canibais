#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import *
import tkMessageBox
from missionarios_canibais import *


class AppScript(Frame):
    def __init__(self, width = 500, height=500):
        Frame.__init__(self,raiz)
        
        self.string = ""
        self.estado = None

        scrollbar = Scrollbar()
        scrollbar.pack(side=RIGHT, fill=Y)

        self.frame1 = Frame(self)
        self.frame1.pack(side=TOP)
        self.frame2 = Frame(self)
        self.frame2.pack(pady=20)
        self.frame3 = Frame(self)
        self.frame3.pack(pady=10)

        self.fonte1 = ('Verdana', '10', 'bold')

        self.labels = Frame(self.frame2)
        self.labels.pack(side=LEFT)

        self.campos = Frame(self.frame2)
        self.campos.pack(side=RIGHT)

        self.titulo1 = Label(self.labels, text="Numero de pessoas: ", width = 20, font = self.fonte1)
        self.titulo1.pack(side=TOP)

        self.campo1 = Entry(self.campos, font=self.fonte1, width=20)
        self.campo1.pack(side=TOP)
        self.campo1.focus_force()

        self.titulo2 = Label(self.labels, text="Tamanho do barco: ", width = 20, font = self.fonte1)
        self.titulo2.pack(side=TOP)

        self.campo2 = Entry(self.campos, font=self.fonte1, width=20)
        self.campo2.pack(side=TOP)
    
        self.texto = Text(self.frame1, yscrollcommand=scrollbar.set, width = 70, font = self.fonte1, background = "black", fg = "white")
        self.texto.pack()
        scrollbar.config(command=self.texto.yview)

        self.button0 = Button(self.frame3)
        self.button0.configure(text="Largura", background="darkgray", height=1, width=12, font=self.fonte1, fg="black")
        self.button0.pack(side = LEFT)
        self.button0.bind("<1>", self.busca_largura)

        
        self.button1 = Button(self.frame3)
        self.button1.configure(text="Profundidade", background="darkgray", height=1, width=12, font=self.fonte1, fg="black")
        self.button1.pack(side=LEFT)
        self.button1.bind("<1>", self.busca_profundidade)

        self.button2 = Button(self.frame3)
        self.button2.configure(text="Gulosa", background="darkgray", height=1, width=12, font=self.fonte1, fg="black")
        self.button2.pack(side=LEFT)
        self.button2.bind("<1>", self.busca_gulosa)

        self.button3 = Button(self.frame3)
        self.button3.configure(text="Heuristica A*", background="darkgray", height=1, width=12, font=self.fonte1, fg="black")
        self.button3.pack(side=LEFT)
        self.button3.bind("<1>", self.busca_heuristica_A)
        

    def busca_largura(self, event):
        self.string = ""
        numero_pessoas = int(self.campo1.get())
        tamanho_barco = int(self.campo2.get())
        self.estado = Missionarios_Canibais(numero_pessoas, tamanho_barco)
        self.string = self.estado.gerar_solucao_busca_largura()
        self.setaTxt(self.string)

    def busca_profundidade(self, event):
        self.string = ""
        numero_pessoas = int(self.campo1.get())
        tamanho_barco = int(self.campo2.get())
        self.estado = Missionarios_Canibais(numero_pessoas, tamanho_barco)
        self.string = self.estado.gerar_solucao_busca_profundidade()
        self.setaTxt(self.string)

    def busca_gulosa(self, event):
        self.string = ""
        numero_pessoas = int(self.campo1.get())
        tamanho_barco = int(self.campo2.get())
        self.estado = Missionarios_Canibais(numero_pessoas, tamanho_barco)
        self.string = self.estado.gerar_solucao_busca_gulosa()
        self.setaTxt(self.string)

    def busca_heuristica_A(self, event):
        self.string = ""
        numero_pessoas = int(self.campo1.get())
        tamanho_barco = int(self.campo2.get())
        self.estado = Missionarios_Canibais(numero_pessoas, tamanho_barco)
        self.string = self.estado.gerar_solucao_busca_A()
        self.setaTxt(self.string)
        
    def setaTxt(self, string):
        self.texto.configure(state=NORMAL)
        self.texto.delete(1.0,END)
        self.texto.insert(1.0, string)
        self.texto.configure(state=DISABLED)

raiz = Tk()
aplicativo = AppScript(raiz)
aplicativo.master.title("MISSIONARIOS E CANIBAIS")
aplicativo.pack()
tkMessageBox.showinfo("COMPONENTES", 'Igor Rafael\nLuiz Magno\nNeclyeux Sousa')
raiz.mainloop()


