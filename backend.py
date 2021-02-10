'''
connects to PostgreSQL database and returns queries
in functions which are then called in script.py
Requirements are in:
 * VIEW     - view
 * EXCEPT   - noGrpStd
 * HAVING   - getTrnStdCount
 * Function 1 - deleteTrn
 * Function 2 - getTrnNameSalary
 * Function 3 with cursor - getTotalPrice
 * Trigger 1 before insert or update - insertGrpStd 
 * Trigger 2 after insert - insertGrpStd
'''
import os
import psycopg2
from tkinter import *
from tkinter.ttk import *
import datetime

DATABASE_URL = "dbname='dalis_okulu_vt' user='postgres' password='postgres123' host='localhost' port='5432'"

''' **************************************************************************************
    ************************* MAIN WINDOW VIEW and HAVING *********************************
'''
def getUpcomingPrg():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = "SELECT * FROM yaklasan_etkinlikler\
          WHERE gun_rakam IN %s ORDER BY gun_rakam;"
  today = datetime.datetime.today().weekday()
  next_days = (str(today), str((today+1)%7), str((today+2)%7)) # modulo 7 because of cycle
  cur.execute(query, (next_days,))
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def getTrnStdCount():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = "SELECT ad, soyad, COUNT(ogrenci_no) AS ogrenci_sayisi\
          FROM egitmen e, grup g, grup_ogr go\
          WHERE tc_kimlik_no = egitmen_no\
            AND g.grup_id = go.grup_id\
          GROUP BY e.tc_kimlik_no\
          HAVING COUNT(ogrenci_no) >= 5;"
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

''' ************************************************************************
    ****************************** STUDENT *********************************
 '''
def showStd():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT tc_kimlik_no, ad, soyad, dogum_tarihi, seviye, referans_no FROM ogrenci ORDER BY ad'
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def deleteStd(tc):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'DELETE FROM ogrenci WHERE tc_kimlik_no=%s'
  cur.execute(query, (tc,))
  conn.commit()
  conn.close()
  return 'Ogrenci Silindi'

def getTrnNo(fname,lname):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT tc_kimlik_no FROM egitmen WHERE ad=%s AND soyad=%s'
  cur.execute(query, (fname,lname))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res[0][0]

def updateStd(std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  if std[-2] != 'None':
    query = 'UPDATE ogrenci \
           SET tc_kimlik_no=%s, ad=%s, soyad=%s, dogum_tarihi=%s, seviye=%s, referans_no=%s \
           WHERE tc_kimlik_no=%s'
    cur.execute(query, (std[0],std[1],std[2],std[3],std[4],std[5],std[0]))
  else:
    query = 'UPDATE ogrenci \
           SET tc_kimlik_no=%s, ad=%s, soyad=%s, dogum_tarihi=%s, seviye=%s, referans_no=NULL \
           WHERE tc_kimlik_no=%s'
    cur.execute(query, (std[0],std[1],std[2],std[3],std[4],std[0]))
  conn.commit()
  conn.close()
  return 'Ogrenci Bilgisi Guncellendi'

def getTrnName():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT ad, soyad, seviye FROM egitmen ORDER BY 1, 2, 3'
  cur.execute(query,())
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return [f'{a} {b} - {c}' for a,b,c in rows] 

def getStdLevel():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT DISTINCT seviye FROM ogrenci ORDER BY seviye'
  cur.execute(query,())
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return [val[0] for val in rows]

def insertStd(std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  if std[-2] != 'None':
    query = 'INSERT INTO ogrenci VALUES(%s,%s,%s,%s,%s,(SELECT e.tc_kimlik_no FROM egitmen e WHERE e.ad=%s AND e.soyad=%s))'
    cur.execute(query, (std[0],std[1],std[2],std[3],std[4],std[5],std[6]))
  else:
    query = 'INSERT INTO ogrenci VALUES(%s,%s,%s,%s,%s,NULL)'
    cur.execute(query, (std[0],std[1],std[2],std[3],std[4]))
  conn.commit()
  conn.close()
  return 'Ogrenci Eklendi ve Bilgileri Kaydedildi'

''' *********************************************************************************************
     ********************************** TRAINER *************************************************
'''
def showTrn():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT tc_kimlik_no, ad, soyad, maas, seviye, komisyon FROM egitmen ORDER BY ad'
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def deleteTrn(tc):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT EGITMEN_DELETE(%s);'  # function to check trainer
  cur.execute(query, (tc,))
  rows = cur.fetchall()
  if rows[0][0] != None: # If function result is not null, call function result
    conn.commit()
    conn.close()
    return rows[0][0]
  else:                 # else resume deleting
    query = 'DELETE FROM egitmen WHERE tc_kimlik_no = %s;'
    cur.execute(query, (tc,))
    conn.commit()
    conn.close()
    return 'Egimen Silindi'
    
def getTrnLevel():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT DISTINCT seviye FROM egitmen ORDER BY seviye'
  cur.execute(query,())
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return [val[0] for val in rows]

def updateTrn(trn):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  trn = [None if i == 'None' or i == '' else i for i in trn]
  query = 'UPDATE egitmen SET tc_kimlik_no=%s,ad=%s,soyad=%s,maas=%s,seviye=%s,komisyon=%s \
    WHERE tc_kimlik_no=%s'
  cur.execute(query, (trn[0], trn[1], trn[2], trn[3], trn[4], trn[5], trn[0]))
  conn.commit()
  conn.close()
  return 'Egitmen Guncellendi'

def insertTrn(trn):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  trn = [None if i == 'None' or i == '' else i for i in trn]
  query = 'INSERT INTO egitmen VALUES(%s,%s,%s,%s,%s,%s)'
  cur.execute(query, (trn[0],trn[1],trn[2],trn[4],trn[3],trn[5]))
  conn.commit()
  conn.close()
  return 'Egitmen Eklendi'


''' *********************************************************************************************************
    ****************************************** PROGRAM *****************************************************
 '''
def showPrg():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT program_id, program_adi, ucret, min_egt_seviye, min_ogr_seviye FROM program ORDER BY program_id'
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def deletePrg(id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'DELETE FROM program WHERE program_id=%s'
  cur.execute(query, (id,))
  conn.commit()
  conn.close()
  return 'Program silindi'

def updatePrg(prg):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  prg = [None if len(i) < 0 or i == 'None' else i for i in prg]
  query = 'UPDATE program SET program_adi=%s, ucret=%s,\
           min_egt_seviye=%s, min_ogr_seviye=%s\
           WHERE program_adi=%s'
  cur.execute(query, (prg[0],prg[1],prg[2],prg[3],prg[0]))
  conn.commit()
  conn.close()
  return 'Program Guncellendi'

def insertPrg(prg):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  prg = [i if len(i)>0 or i!='None' else None for i in prg]
  query = 'INSERT INTO program (program_adi, ucret, min_egt_seviye, min_ogr_seviye) VALUES(%s,%s,%s,%s)'
  cur.execute(query, (prg[0],prg[1],prg[2],prg[3]))
  conn.commit()
  conn.close()
  return 'Program Eklendi'

def showPrgInfo(prg_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT g.grup_id\
           FROM program p, grup g WHERE p.program_id = g.program_id AND p.program_id=%s \
           ORDER BY p.program_id'
  cur.execute(query, (prg_id,))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return [i[0] for i in res]

def getTotalPrice(prg_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT PROGRAM_ODENEN_UCRET(%s);'
  cur.execute(query, (prg_id,))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res

''' *****************************************************************************************************
    ******************************************* GROUP ***************************************************
'''
def showGrp():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT g.grup_id, p.program_adi, egitmen_no, gun, COUNT(ogrenci_no)\
          FROM grup g JOIN program p USING(program_id)\
          LEFT JOIN grup_ogr USING(grup_id)\
          GROUP BY 1, 2 ORDER BY 1;'
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def deleteGrp(id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'DELETE FROM grup WHERE grup_id=%s'
  cur.execute(query, (id,))
  conn.commit()
  conn.close()
  return 'Grup Silindi'

def updateGrp(grp):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  grp = [None if len(i) < 0 or i == 'None' else i for i in grp]
  query = 'UPDATE grup SET grup_id=%s, program_id=%s, gun=%s, egitmen_no=%s WHERE grup_id=%s'
  cur.execute(query, (grp[0], grp[1], grp[2], grp[3], grp[0]))
  conn.commit()
  conn.close()
  return 'Grup Guncellendi'

def insertGrp(grp):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  grp = [i if len(i)>0 or i!='None' else None for i in grp]
  query = 'INSERT INTO grup (program_id, egitmen_no, gun) VALUES((SELECT program_id FROM program p WHERE p.program_adi=%s), \
            (SELECT e.tc_kimlik_no FROM egitmen e WHERE e.ad=%s AND e.soyad=%s),%s)'
  cur.execute(query, (grp[0], grp[2], grp[3], grp[1]))
  conn.commit()
  conn.close()
  return 'Grup Eklendi'

def getTrnNameSalary(grp_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query0 = 'SELECT e.tc_kimlik_no FROM egitmen e, grup g\
           WHERE g.egitmen_no = e.tc_kimlik_no AND g.grup_id=%s;'
  cur.execute(query0, (grp_id,))
  res = cur.fetchall()
  query1 = 'SELECT EGITMEN_MAAS(%s);'
  cur.execute(query1, (str(res[0][0]),))
  name_salary = cur.fetchone()
  conn.commit()
  conn.close()
  return name_salary[0][1:-1] # eliminate parantheses

def getPrgName(grp_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT program_adi\
           FROM program p, grup g WHERE p.program_id = g.program_id AND g.grup_id=%s'
  cur.execute(query, (grp_id,))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res[0]

def getAllPrgName():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT program_adi FROM program'
  cur.execute(query)
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return [i[0] for i in res]


''' ****************************************************************************************************
    ************************************ GRUP STUDENT **************************************************
 '''
def showGrpStd():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT grup_id, ad, soyad, seviye\
           FROM grup_ogr, ogrenci WHERE ogrenci_no = tc_kimlik_no ORDER BY 1, 2, 3'
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def insertGrpStd(grp_std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'INSERT INTO grup_ogr VALUES(%s,(SELECT o.tc_kimlik_no FROM ogrenci o WHERE o.ad=%s AND o.soyad=%s))'
  cur.execute(query, (grp_std[0], grp_std[1].split()[0], grp_std[1].split()[1]))
  message = conn.notices[0][7:-1] 
  conn.commit()
  conn.close()
  return message

def deleteGrpStd(id, fname, lname):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'DELETE FROM grup_ogr WHERE grup_id=%s AND ogrenci_no=\
            (SELECT tc_kimlik_no FROM ogrenci WHERE ad=%s AND soyad=%s)'
  cur.execute(query, (id, fname, lname))
  conn.commit()
  conn.close()
  return 'Grup Ogrenci Silindi'

def updateGrpStd(grp_std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'UPDATE grup_ogr SET grup_id=%s, ogrenci_no=(SELECT o.tc_kimlik_no FROM ogrenci o WHERE o.ad=%s AND o.soyad=%s) \
          WHERE grup_id=%s AND ogrenci_no=(SELECT o.tc_kimlik_no FROM ogrenci o WHERE o.ad=%s AND o.soyad=%s)'
  cur.execute(query, (grp_std[0], grp_std[1].split()[0], grp_std[1].split()[1], grp_std[2], grp_std[3], grp_std[4]))
  conn.commit()
  conn.close()
  return 'Grup Ogrenci Guncellendi'

def noGrpStd():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = "SELECT ad, soyad, tc_kimlik_no, seviye FROM ogrenci\
          EXCEPT\
          SELECT ad, soyad, ogrenci_no, seviye FROM ogrenci, grup_ogr\
          WHERE ogrenci_no = tc_kimlik_no \
          ORDER BY seviye, ad, soyad;"
  cur.execute(query)
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

  
def getStdCount(group_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT COUNT(*) FROM grup_ogr \
           WHERE grup_id=%s GROUP BY grup_id'
  cur.execute(query, (group_id,))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res

def getStdName(std_no):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT ad, soyad FROM ogrenci WHERE tc_kimlik_no=%s'
  cur.execute(query, (str(std_no),))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res[0]

def getAllStdByLevel(level):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT ad, soyad FROM ogrenci WHERE seviye=%s ORDER BY 1, 2'
  cur.execute(query, (level))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return [i[0]+' '+i[1] for i in res]

def getAllStd():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT ad, soyad FROM ogrenci ORDER BY ad'
  cur.execute(query)
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return [i[0]+' '+i[1] for i in res]

def getAllGrpId():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT grup_id FROM grup'
  cur.execute(query)
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return [i[0] for i in res]
