#! /usr/bin/python
# -*- coding: utf-8 -*-

import sys
import sqlite3 as lite
from random import randint

def randomUlke(ulkeler):
	# 4 tane ulke ve baskent
	l = []
	while len(l) != 4:
		sayi = randint(0,len(ulkeler)-1)
		ulke = ulkeler[sayi]
		if not ulke in l:
			l.append(ulke)
	return l

def secKaristir(sec):	
	# secenekleri olustuyor
	for i in range(10):
		sayi1 = randint(0,3)
		sayi2 = randint(0,3)
		temp = sec[sayi1]
		sec[sayi1] = sec[sayi2]
		sec[sayi2] = temp
	secDic = {
	'A' : sec[0][2],
	'B' : sec[1][2],
	'C' : sec[2][2],
	'D' : sec[3][2],
	}

	return secDic

def bekle(msg):
	raw_input(msg)

def intro():
	print """
		=========  BaskentiNeresi ===========

		[[[ Menu ]]]
		1 - Yeni Oyun
		2 - Skor Tabelasi
		3 - Yardim
		0 - Cikis
	"""

	return  int(raw_input("Seciminiz > "))

def yeniOyun():
	print """
		Hangi bolgeden soru isterseniz ? 
	
		1 - Avrupa		5 - Afrika
		2 - Asya		6 - Kuzey Amerika
		3 - Uzak Dogu		7 - Guney Amerika
		4 - Okyanusya		8 - Karisik
	"""
	return int(raw_input("Seciminiz > "))

def getUsers(cursor):
	q = "select * from users"
	cursor.execute(q)
	
	liste = cursor.fetchall()
	if len(liste) == 0:
		print "\tSkor listesinde henuz kimse yok!"
	else:
		print "\t   Name          Skor"
		print "\t----------    ----------"
		for user in liste:
			print "\t%s\t\t%d" % (user[1], user[2])
	bekle("Devam etmek icin Enter... ")
	

def yardim():
	print """
	Yeni Oyun : Yeni oyun :)
	Skor Tabelasi : Varsa isimlerle beraber skor listesini gosterir.
	Cikis : Programdan cikis yapar.
	
	Ulkeler bolgelere gore ayrilmis durumda.
	Karisik secenegini secerek her bolgeden ulke icin sorulari cevaplayabilirsiniz.
	Yanlis cevap verdikten sonra skorunuzun kaydedilmesini istiyorsaniz bir isim giriniz.
	Iyı eglenceler :) 
	"""
	bekle("Devam etmek icin Enter...")
dbFile = "myDB.db"
conn = lite.connect(dbFile)
cursor = conn.cursor()

while True:
	secim = intro()
	if secim == 0: 
		sys.exit()	
	elif secim == 2:
		getUsers(cursor)
	elif secim == 3:
		yardim()
	elif secim == 1: 
		bolge = yeniOyun()
		if bolge == 8:
			q = "select * from countries"
			cursor.execute(q)
		else:
			q = "select * from countries where bolge = ?"	
			cursor.execute(q, (bolge,))
		ulkeler = cursor.fetchall()

		skor = 0
		devam = True
		while devam:

			# diger secenekler
			sec = randomUlke(ulkeler)
			secDic = secKaristir(sec)

			sorulacakUlkeList = sec[randint(0,3)]
			ulke = sorulacakUlkeList[1]
			baskent = sorulacakUlkeList[2]
			
			# dictionary keylerini sırala
			keys = secDic.keys()
			keys.sort()
			
			print "\n\t%s baskenti neresidir?" % ulke
			for key in keys:
				print "\t  %s - %s" % (key,secDic[key])

			cevap = raw_input("Cevap > ").upper()
			if secDic[cevap] == baskent:
				print "Tebrikler!Dogru cevap."
				skor += 1
				bekle("Bir sonraki soru icin Enter...")
			else:
				print "Yanlis! %s baskenti: %s" % (ulke, baskent)
				devam = False
				print "%s tane dogru bildin." % skor	
				isim = raw_input("Kaydedilirken kullanilacak isim > ")
				
				q = "insert into users(name, skor) values(?,?)"
				cursor.execute(q, (isim, skor))
				conn.commit()
				print "Skorunuz basariyla kaydedildi."
				bekle("Ana menuye donmek icin Enter...")	
	else: 
		yardim()
