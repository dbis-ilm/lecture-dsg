CREATE TABLE "ERZEUGER" (
    "Weingut"       varchar(20),
    "Anbaugebiet"   varchar(20),
    "Region"        varchar(20) NOT NULL,
    PRIMARY KEY ("Weingut")
);

INSERT INTO "ERZEUGER" VALUES
    ('Creek','Barossa Valley','South Australia'),
    ('Helena','Napa Valley','Kalifornien'),
    ('Chateau La Rose','Saint-Emilion','Bordeaux'),
    ('Chateau La Pointe','Pomerol','Bordeaux'),
    ('Müller','Rheingau','Hessen'),
    ('Bighorn','Napa Valley','Kalifornien');

CREATE TABLE "WEINE" (
    "WeinID"        int,
    "Name"         varchar(20) NOT NULL,
    "Farbe"         varchar(10),
    "Jahrgang"      int,
    "Weingut"       varchar(20),
    FOREIGN KEY ("Weingut") REFERENCES "ERZEUGER"("Weingut"),
    PRIMARY KEY ("WeinID")
);

INSERT INTO "WEINE" VALUES
    (1042,'La Rose Grand Cru','Rot',1998,'Chateau La Rose'),
    (2168,'Creek Shiraz','Rot',2003,'Creek'),
    (3456,'Zinfandel','Rot',2004,'Helena'),
    (2171,'Pinot Noir','Rot',2001,'Creek'),
    (3478,'Pinot Noir','Rot',1999,'Helena'),
    (4711,'Riesling Reserve','Weiß',1999,'Müller'),
    (4961,'Chardonnay','Weiß',2002,'Bighorn');

CREATE TABLE "R" (
    A INTEGER,
    B INTEGER,
    C INTEGER,
    PRIMARY KEY (A, B, C)
);

INSERT INTO "R" VALUES
    (1, 2, 3),
    (2, 3, 4);

CREATE TABLE "S" (
    A INTEGER,
    C INTEGER,
    D INTEGER,
    PRIMARY KEY (A, C, D)
);

INSERT INTO "S" VALUES
    (2, 3, 4),
    (2, 4, 5);

CREATE TABLE "REL" (
    A INTEGER,
    B INTEGER,
    C INTEGER,
    D INTEGER,
    PRIMARY KEY (A, B, C, D)
);

INSERT INTO "REL" VALUES
    (1, 2, 3, 4),
    (1, 2, 4, 5),
    (2, 3, 3, 4),
    (3, 3, 4, 5),
    (3, 3, 6, 7);

CREATE TABLE "BUSLINIE" (
    Abfahrt VARCHAR,
    Ankunft VARCHAR,
    Distanz INTEGER,
    PRIMARY KEY (Abfahrt, Ankunft)
);

INSERT INTO "BUSLINIE" VALUES
    ('Nuriootpa', 'Penrice', 7),
    ('Nuriootpa', 'Tanunda', 7),
    ('Tanunda', 'Seppeltsfield', 9),
    ('Tanunda', 'Bethany', 4),
    ('Bethany', 'Lyndoch', 14);

CREATE TABLE "LDATA" (
    Quartal INTEGER,
    Jahr    INTEGER,
    Umsatz  INTEGER,
    PRIMARY KEY (Quartal, Jahr)
);

INSERT INTO "LDATA" VALUES
    (1, 2020, 12),
    (2, 2020, 10),
    (3, 2020, 11),
    (4, 2020, 9),
    (1, 2021, 13),
    (2, 2021, 12);

CREATE TABLE "RDATA" (
    Jahr INTEGER PRIMARY KEY,
    Q1   INTEGER,
    Q2   INTEGER,
    Q3   INTEGER,
    Q4   INTEGER
);

INSERT INTO "RDATA" VALUES
    (2020, 12, 10, 11, 9),
    (2021, 13, 12, NULL, NULL);

CREATE TABLE "RACE" (
    Name    VARCHAR PRIMARY KEY,
    Distanz VARCHAR,
    Zeit    VARCHAR
);

INSERT INTO "RACE" VALUES
    ('Klaus', 'HM', '1:20'),
    ('Bernd', 'HM', '1:40'),
    ('Tanja', 'M', '3:58'),
    ('Franz', 'SM', '5:42'),
    ('Martina', 'M', '3:05'),
    ('Heike', 'HM', '1:34'),
    ('Corinna', 'SM', '5:53'),
    ('Jens', 'M', '2:51'),
    ('Herbert', 'SM', '6:07');

CREATE TABLE "SERIES" (
    Zeit VARCHAR PRIMARY KEY,
    Wert FLOAT
);

INSERT INTO "SERIES" VALUES
    ('0:01', 4.2),
    ('0:02', 4.3),
    ('0:03', 4.9),
    ('0:04', 4.4),
    ('0:05', 4.1),
    ('0:06', 3.9),
    ('0:07', 4.5),
    ('0:08', 4.3),
    ('0:09', 4.1);

CREATE TABLE "HOBBIES" (
    Name  VARCHAR,
    Hobby VARCHAR,
    PRIMARY KEY (Name, Hobby)
);

INSERT INTO "HOBBIES" VALUES
    ('Kevin', 'Schach'),
    ('Kevin', 'Musik'),
    ('Corinna', 'Parties'),
    ('Martin', 'Handball'),
    ('Martin', 'Musik'),
    ('Katja', 'Handball'),
    ('Katja', 'Musik');

CREATE TABLE "FAHRPLAN" (
    Buslinie INTEGER PRIMARY KEY,
    Abfahrt  TIME,
    Ankunft  TIME
);

INSERT INTO "FAHRPLAN" VALUES
    (10, '08:00:00', '09:20:00'),
    (11, '09:10:00', '10:35:00'),
    (12, '09:10:00', '11:00:00'),
    (13, '09:55:00', '10:45:00');

CREATE TABLE "STUDENTS" (
    Name        VARCHAR PRIMARY KEY,
    Studiengang VARCHAR
);

INSERT INTO "STUDENTS" VALUES
    ('Kevin', 'Informatik'),
    ('Heike', 'BWL'),
    ('Corinna', 'Mathematik'),
    ('Martina', 'BWL'),
    ('Ronny', 'BWL'),
    ('Katharina', 'Informatik');
