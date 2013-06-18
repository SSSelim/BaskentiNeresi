#! /usr/bin/python
# -*- coding: utf-8 -*-

import os
import sqlite3 as lite

#file = open("info.txt")
filename = "info.txt" # butun listeyi okuyacagimiz dosya

with open(filename) as file:
	bolgeler = file.read().split('BOL')

del bolgeler[0] # bosluk elemanini sil

bolgeAdlari = []
allList = []

for bolge in bolgeler:
	ulkeler = bolge.split('\n')
	del ulkeler[0] # bosluk elemanini sil
	bolgeAdlari.append(ulkeler.pop(0))
	ulkeler.pop()
	tempBolge = []
	for ulke in ulkeler:
		temp = ulke.split(' : ')
		tempBolge.append(temp)
		#print "%s r %s" % (temp[0], temp[1])
	allList.append(tempBolge)

dbFile = "myDB.db"
schemaFile = "schema.sql"

exists = not os.path.exists(dbFile) # myDB.db yoksa exists = True oluyor.

with lite.connect(dbFile) as conn:
	if exists:
		print "schema.sql icerigi okunuyor..."
		print "Tablolar olusturuluyor..."
		with open(schemaFile, "rt") as f:
			schema = f.read()
		conn.executescript(schema)
		
		print "Dosyadan okunan veriler veritabanina ekleniyor..."
		
		for i,bolge in enumerate(allList):
			for ulke in bolge:
				q = "insert into countries(ulke, baskent, bolge) values(?, ?, ?)"
				conn.execute(q, (ulke[0], ulke[1], i+1))		
	else:
		print "Database dosyasi var oldugu icin herhangi bir islem yapilmadi!"
