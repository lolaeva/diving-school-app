CREATE SEQUENCE grup_id
START 1000
INCREMENT 1
MINVALUE 1000;


--DROP TABLE program;
CREATE TABLE program (
  program_id SERIAL, 
  program_adi  varchar(50),
  ucret numeric CHECK(ucret > 0),
  min_egt_seviye int,
  min_ogr_seviye int,
  primary key (program_id)
);

--DROP TABLE egitmen;
CREATE TABLE egitmen (
  tc_kimlik_no varchar(11) NOT NULL, 
  ad  varchar(50),
  soyad varchar(50),
  seviye int,
  maas numeric CHECK(maas > 0),
  komisyon numeric,
  primary key (tc_kimlik_no)
);

--DROP TABLE ogrenci;
CREATE TABLE ogrenci (
  tc_kimlik_no varchar(11) NOT NULL, 
  ad  varchar(50),
  soyad varchar(50),
  dogum_tarihi DATE CHECK (dogum_tarihi > '1900-01-01'),
  seviye int,
  referans_no varchar(11),
  primary key (tc_kimlik_no),
  FOREIGN KEY(referans_no) REFERENCES egitmen(tc_kimlik_no)
);

--DROP TABLE grup;
CREATE TABLE grup (
  grup_id int NOT NULL DEFAULT nextval('grup_id'), 
  program_id int NOT NULL,
  egitmen_no varchar(11) NOT NULL,
  gun varchar(11) NOT NULL,
  primary key (grup_id),
  FOREIGN KEY(egitmen_no) REFERENCES egitmen(tc_kimlik_no),
  FOREIGN KEY(program_id) REFERENCES program(program_id)
);

--DROP TABLE grup_ogr;
CREATE TABLE grup_ogr (
  grup_id int, 
  ogrenci_no varchar(11),
  FOREIGN KEY(grup_id) REFERENCES grup(grup_id),
  FOREIGN KEY(ogrenci_no) REFERENCES ogrenci(tc_kimlik_no)
);



-- VIEWS
DROP VIEW yaklasan_etkinlikler;

CREATE VIEW yaklasan_etkinlikler AS
	SELECT g.grup_id, p.program_adi, g.gun, concat(e.ad,' ', e.soyad) AS egitmeni,
		CASE gun
			WHEN 'Pazartesi' THEN 0
			WHEN 'Sali' THEN 1
			WHEN 'Carsamba' THEN 2
			WHEN 'Persembe' THEN 3
			WHEN 'Cuma' THEN 4
			WHEN 'Cumartesi' THEN 5
			WHEN 'Pazar' THEN 6
		END gun_rakam
	FROM grup g, program p, egitmen e
	WHERE g.program_id = p.program_id
	AND g.egitmen_no = e.tc_kimlik_no;


-- TRIGGER
-- gruba öğrenci ekleme kontrolü
CREATE or replace FUNCTION grup_ogrenci_ekleme() RETURNS trigger AS $$
BEGIN
  IF(SELECT seviye FROM ogrenci
	WHERE tc_kimlik_no = NEW.ogrenci_no) 
	<
	(SELECT min_ogr_seviye FROM grup g, program p
	WHERE g.program_id = p.program_id
	AND g.grup_id = NEW.grup_id)
  	THEN RAISE EXCEPTION 'Ogrenci Seviyesi Grup Min Seviyesinden Kucuk Olamaz';
	RETURN NULL;
  ELSEIF EXISTS (SELECT ogrenci_no FROM grup_ogr
	  WHERE ogrenci_no = NEW.ogrenci_no AND grup_id = NEW.grup_id)
  	THEN RAISE EXCEPTION 'Ogrenci Ayni Grupta Tekrar Yer Alamaz';
	RETURN NULL;
  ELSE
  	RETURN NEW;
  END IF;
END;
$$
LANGUAGE plpgsql;

CREATE TRIGGER grup_ogrenci_ekleme
BEFORE INSERT OR UPDATE ON grup_ogr
FOR EACH ROW EXECUTE PROCEDURE grup_ogrenci_ekleme();


-- öğrencinin katıldığı program in ücretinin %20'sini referans olan egitmene ver
CREATE OR REPLACE FUNCTION egitmen_komisyon () 
RETURNS TRIGGER AS $$ 
BEGIN 
IF EXISTS (select 1 from egitmen e, ogrenci o 
           where e.tc_kimlik_no = o.referans_no 
           and o.tc_kimlik_no = new.ogrenci_no) 
           THEN
           UPDATE egitmen 
           SET komisyon = komisyon + ((( select ucret from program p, grup g 
                                      where p.program_id = g.program_id
                                      and g.grup_id = new.grup_id) *20) / 100)
            where tc_kimlik_no = (select referans_no from ogrenci o 
                                  where o.tc_kimlik_no = new.ogrenci_no);
RETURN NEW;
ELSE RETURN NEW;
END IF;
END;
$$ LANGUAGE plpgsql;


CREATE TRIGGER grup_ogrenci_komisyon
AFTER INSERT ON grup_ogr
FOR EACH ROW EXECUTE PROCEDURE egitmen_komisyon ();


-- FUNCTION
-- egitmen silinmesi öncesinde grup kontrolü yapması için
CREATE OR REPLACE FUNCTION EGITMEN_DELETE (egitmenId egitmen.tc_kimlik_no%type)
RETURNS varchar AS $info_message$
declare
    info_message varchar;
BEGIN
   Select CASE WHEN
   (SELECT count(1) FROM grup where egitmen_no = egitmenId) > 0
   THEN 'bu egitmenin tanımlı olduğu grup vardır.' END into info_message ;
   RETURN info_message;
END;
$info_message$ LANGUAGE plpgsql;


-- egitmen ad soyad maas bilgisi dönüyor
CREATE TYPE egitmen_maas AS (ad VARCHAR(50), soyad VARCHAR(50), maas numeric);

CREATE OR REPLACE FUNCTION EGITMEN_MAAS (egitmenId egitmen.tc_kimlik_no%type)
RETURNS egitmen_maas AS $$
declare
    bilgi egitmen_maas;
BEGIN
   select ad, soyad, maas into bilgi from egitmen where tc_kimlik_no =  egitmenId;
   RAISE NOTICE 'Calisanin ismi: %-% , maasi: %TL dir', bilgi.ad, bilgi.soyad, bilgi.maas;
   RETURN bilgi;
END;
$$ LANGUAGE plpgsql;


-- programa toplam ödenen ücret
CREATE OR REPLACE FUNCTION PROGRAM_ODENEN_UCRET (programId program.program_id%type)
RETURNS NUMERIC AS $$
declare
    toplam_ucret NUMERIC;
    tutar_Curs CURSOR FOR SELECT p.ucret from program p, grup g, grup_ogr go, ogrenci o
    where p.program_id = g.program_id 
    and g.grup_id = go.grup_id
    and go.ogrenci_no = o.tc_kimlik_no
    and p.program_id = programId;
BEGIN
    toplam_ucret :=0;
   FOR satir IN tutar_Curs LOOP
           toplam_ucret := toplam_ucret + satir.ucret;
    END LOOP;
   RETURN toplam_ucret;
END;
$$ LANGUAGE plpgsql;