-- baskentbilmece programinin schemasi

create table countries(
	id 	integer primary key autoincrement not null,
	ulke 	text,
	baskent	text,
	bolge 	int
);

create table users(
	id 	integer primary key autoincrement not null,
	name 	text default 'unknown',
	skor	int
);
