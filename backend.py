'''
connects to PostgreSQL database and returns queries
in functions which are then called in script.py
'''
import os
import urllib.parse as urlparse
import psycopg2
from tkinter import *
from tkinter.ttk import *
import datetime

# os.environ['DATABASE_URL'] = 'postgres://lmgcolusndmjrc:1c7860f3bdf2100c9137dea9692adfe15be2ec97eaaa5cb3411aa6c151d80008@ec2-3-233-206-99.compute-1.amazonaws.com:5432/dfie71fcq48391'
# DATABASE_URL = os.environ.get('DATABASE_URL')

# url = urlparse.urlparse(os.environ['DATABASE_URL'])
# dbname = url.path[1:]
# user = url.username
# password = url.password
# host = url.hostname
# port = url.port

# DATABASE_URL = psycopg2.connect(
#             dbname=dbname,
#             user=user,
#             password=password,
#             host=host,
#             port=port
#             )
# # DATABASE_URL = psycopg2.connect(DATABASE_URL, sslmode='require')

DATABASE_URL = "dbname='dalis_okulu_vt' user='postgres' password='postgres123' host='localhost' port='5432'"


# **************************************************************************************
# ************************* MAIN WINDOW VIEW and HAVING *********************************
def view():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = "SELECT grup_id, program_adi, gun, egitmeni FROM yaklasan_etkinlikler\
          WHERE gun_rakam IN %s ORDER BY gun_rakam;"
  today = datetime.datetime.today().weekday()
  next_days = (str(today), str((today+1)%7), str((today+2)%7))
  cur.execute(query, (next_days,))
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return rows

def having():
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

# *********************************************
# ****************** STUDENT ******************
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
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def getTrnNo(fname,lname):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT tc_kimlik_no FROM egitmen WHERE ad=%s AND soyad=%s'
  cur.execute(query, (fname,lname))
  res = cur.fetchall()
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  return res[0][0]

def updateStd(std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'UPDATE ogrenci \
           SET tc_kimlik_no=%s, ad=%s, soyad=%s, dogum_tarihi=%s, seviye=%s, referans_no=%s \
           WHERE tc_kimlik_no=%s'
  cur.execute(query, (std[0],std[1],std[2],std[3],std[4],std[5],std[0]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def getTrnName():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT ad, soyad FROM egitmen'
  cur.execute(query,())
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return [f'{a} {b}' for a,b in rows] 

def getStdLevel():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT DISTINCT seviye FROM ogrenci ORDER BY seviye'
  cur.execute(query,())
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  rows = cur.fetchall()
  conn.commit()
  conn.close()
  return [val[0] for val in rows]

def insertStd(std):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'INSERT INTO ogrenci VALUES(%s,%s,%s,%s,%s,(SELECT e.tc_kimlik_no FROM egitmen e WHERE e.ad=%s AND e.soyad=%s))'
  cur.execute(query, (std[0],std[1],std[2],std[3],std[4],std[5],std[6]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

# *********************************************************************************************
# ********************************** egitmen *************************************************
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
  query = 'DELETE FROM egitmen WHERE tc_kimlik_no=%s'
  cur.execute(query, (tc,))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def getTrnLevel():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT DISTINCT seviye FROM egitmen ORDER BY seviye'
  cur.execute(query,())
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
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


def insertTrn(trn):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  trn = [None if i == 'None' or i == '' else i for i in trn]
  query = 'INSERT INTO egitmen VALUES(%s,%s,%s,%s,%s,%s)'
  cur.execute(query, (trn[0],trn[1],trn[2],trn[3],trn[4],trn[5]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message


# **********************************************************************
# ****************************** PROGRAM *******************************
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
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def updatePrg(prg):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  prg = [None if len(i) < 0 or i == 'None' else i for i in prg]
  query = 'UPDATE program SET program_id=%s, program_adi=%s, ucret=%s,\
           min_egt_seviye=%s, min_ogr_seviye=%s\
           WHERE program_id=%s'
  cur.execute(query, (prg[0],prg[1],prg[2],prg[3],prg[4],prg[0]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def insertPrg(prg):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  prg = [i if len(i)>0 or i!='None' else None for i in prg]
  query = 'INSERT INTO program VALUES(%s,%s,%s,%s,%s)'
  cur.execute(query, (prg[0],prg[1],prg[2],prg[3],prg[4]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def showPrgInfo(prg_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT g.grup_id\
           FROM program p, grup g WHERE p.program_id = g.program_id AND p.program_id=%s \
           ORDER BY p.program_id'
  cur.execute(query, (prg_id,))
  res = cur.fetchall()
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  return [i[0] for i in res]

# *********************************************************************************************
# ********************************* GRUP ***************************************************
def showGrp():
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT grup_id, program_id, egitmen_no, gun\
           FROM grup ORDER BY grup_id'
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
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def updateGrp(grp):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  grp = [None if len(i) < 0 or i == 'None' else i for i in grp]
  query = 'UPDATE grup SET grup_id=%s, program_id=%s, gun=%s, egitmen_no=%s WHERE grup_id=%s'
  cur.execute(query, (grp[0], grp[1], grp[2], grp[3], grp[0]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  # return message

def insertGrp(grp):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  grp = [i if len(i)>0 or i!='None' else None for i in grp]
  query = 'INSERT INTO grup VALUES(%s,%s,(SELECT e.tc_kimlik_no FROM egitmen e WHERE e.ad=%s AND e.soyad=%s),%s)'
  cur.execute(query, (grp[0], grp[1], grp[3], grp[4], grp[2]))
  message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  return message

def showGrpInfo(grp_id):
  conn = psycopg2.connect(DATABASE_URL)
  cur = conn.cursor()
  query = 'SELECT e.ad, e.soyad\
           FROM egitmen e, grup g WHERE g.egitmen_no = e.tc_kimlik_no AND g.grup_id=%s'
  cur.execute(query, (grp_id,))
  res = cur.fetchall()
  conn.commit()
  conn.close()
  return res[0]

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


# *******************************************************************************
# ************************* GRUP STUDENT ****************************************
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
  message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
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
  print(grp_std[0], grp_std[1].split()[0], grp_std[1].split()[1], grp_std[2], grp_std[3], grp_std[4])
  query = 'UPDATE grup_ogr SET grup_id=%s, ogrenci_no=(SELECT o.tc_kimlik_no FROM ogrenci o WHERE o.ad=%s AND o.soyad=%s) \
          WHERE grup_id=%s AND ogrenci_no=(SELECT o.tc_kimlik_no FROM ogrenci o WHERE o.ad=%s AND o.soyad=%s)'
  cur.execute(query, (grp_std[0], grp_std[1].split()[0], grp_std[1].split()[1], grp_std[2], grp_std[3], grp_std[4]))
  # message = conn.notices[0][7:-1]  # get sql notice. sql notice output is ['NOTICE: -some message- \n']
  conn.commit()
  conn.close()
  return 'Grup Ogrenci Yenilendi'

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
