from cs50 import SQL
from datetime import datetime
import pytz

# create a database object to connect to our db
db = SQL("sqlite:///signinout.db")

def get_today():
  # set the timezone to our timezone
  indytz = pytz.timezone("America/Indiana/Indianapolis")
  today = datetime.now(indytz) #get the current date and time
  cur_date = today.strftime("%m-%d-%Y") #date format 04-12-2023
  cur_time = today.strftime("%-I:%M %p") #time format 3:05 PM
  #return a dict with the current date and time
  return {'c_date':cur_date,'c_time':cur_time}

def delete_pass(id):
  sql = "DELETE FROM passes WHERE id = ?"
  # this is removing 1 row from the passes table becasue the id should be unique
  number_of_rows_deleted = db.execute(sql, id)
  return number_of_rows_deleted

def get_student_id(id):
  # this will return just the student's id number given a pass id
  sql = "SELECT student_id FROM passes WHERE id = ?"
  rows = db.execute(sql, id)
  if len(rows) == 0: # no matching data found
    return None
  else:
    return rows[0].get("student_id") # the first item in the list
  






# this function will get all the passes from the database
def get_all_passes():
  sql = """
  SELECT *
    FROM passes
    ORDER BY pass_date DESC, out_time DESC
  """
  results = db.execute(sql)
  return results

# get just the passes for today
def get_todays_passes(today):
  sql = "SELECT * FROM passes WHERE pass_date = ?"
  return db.execute(sql, today)



# get a summary of how many passes each student has used
def get_summary():
  sql = """SELECT COUNT(*) as total, f_name, l_name, student_id
  FROM passes
  GROUP BY student_id ORDER BY total DESC"""
  return db.execute(sql)

def get_student_summary(stu_id):
  sql = """SELECT COUNT(id) as total, location, student_id
  FROM passes
  WHERE student_id = ?
  GROUP BY location ORDER BY total DESC"""
  return db.execute(sql, stu_id)

def get_student_name(stu_id):
  sql = "SELECT f_name, l_name FROM passes WHERE student_id = ?"
  result = db.execute(sql, stu_id)[0]
  # there is only one student DICT in the list so use [0]
  student_name = result.get('f_name') + ' ' + result.get('l_name')
  return student_name

def get_student_location_summary(stu_id, loc):
  sql = """SELECT id, pass_date, out_time, in_time
  FROM passes
  WHERE student_id = ? AND location = ?
  ORDER BY pass_date DESC, out_time DESC"""
  return db.execute(sql, stu_id, loc)

def get_all_students():
  sql = """SELECT DISTINCT(student_id) as s_id, f_name, l_name 
  FROM passes
  ORDER BY l_name, f_name"""
  return db.execute(sql)

def check_for_pass(stu_id):
  # probably should only get passes from today
  sql = """SELECT id FROM passes 
  WHERE student_id = ? AND in_time IS NULL"""
  results = db.execute(sql, stu_id)
  # check to see if there is only 1 pass
  # 0 passes
  if len(results) == 0: #no passes or wrong id
    return 0
  elif len(results) == 1: #there was one pass
    return results[0].get("id")
  else: #multiple passes 
    return -1

def sign_back_in(pass_id):
  sql = """UPDATE passes SET in_time = ?
  WHERE id = ?"""
  current_time = get_today().get("c_time")
  return db.execute(sql, current_time, pass_id)



def insert_pass(pass_data):
  sql = """INSERT INTO passes 
    (student_id, f_name, l_name, location, pass_date, out_time)
    VALUES
    (?,?,?,?,?,?)"""
  pass_id = db.execute(sql, 
                       pass_data.get("stu_id"),
                       pass_data.get("first"),
                       pass_data.get("last"),
                       pass_data.get("loc"),
                       pass_data.get("pass_date"),
                       pass_data.get("out_time")
                      )
  return pass_id


def get_pass_by_id(id):
  sql = "SELECT * FROM passes WHERE id = ?"
  rows = db.execute(sql, id)
  if len(rows) == 1:
    return rows[0]
  else:
    return None

def update_full_pass(id, pass_data):
  sql = """UPDATE passes SET
  student_id = ?,
  f_name = ?,
  l_name = ?,
  pass_date = ?,
  location = ?,
  out_time = ?,
  in_time = ?
  WHERE id = ?"""
  return db.execute(sql,
                    pass_data.get("student_id"),
                    pass_data.get("f_name"),
                    pass_data.get("l_name"),
                    pass_data.get("pass_date"),
                    pass_data.get("location"),
                    pass_data.get("out_time"),
                    pass_data.get("in_time"),
                    id)






























  