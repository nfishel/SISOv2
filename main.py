from flask import Flask, render_template, request, redirect, flash
import queries as q
import os

app = Flask(__name__)
app.secret_key = os.getenv("MSG_KEY")

@app.route("/")
def home():
  return render_template("index.html")

@app.route("/delete/<int:id>", methods=["GET","POST"])
def delete(id):
  if request.method == "POST":
    #first grab the student id and check it
    student_id = request.form.get("stu_id").upper()
    if student_id == q.get_student_id(id): 
      # the student id from the form matches the one in the database for that pass
      num_rows = q.delete_pass(id)
    else:
      num_rows = 0
    if num_rows > 0: # at least one pass was deleted
      flash(f"You have successfully deleted {num_rows} pass")
    else:
      flash("No Passes Were Deleted, The Pass ID did not match!")
    return redirect("/all")
  else: #GET request --> add confirmation page
    return render_template("delete_confirm.html", id=id)
    


@app.route("/all")
def all():
  rows = q.get_all_passes()
  # rows will be a LIST of DICT items
  # each DICT will be one row from our databse
  # the keys of the DICT will be the column names from the table
  return render_template("all.html", rows=rows)

@app.route("/today")
def today():
  today = q.get_today()
  rows = q.get_todays_passes(today.get("c_date"))
  return render_template("day.html", rows=rows, day=today.get("c_date"))
  # make a template page for this route that shows a table of the 
  # returned data, but only show the first and last name,
  # location and times (in and out) in order by out_time

@app.route("/summary")
def summary():
  rows = q.get_summary()
  return render_template("summary.html", rows=rows)

@app.route("/summary/<string:stu_id>")
def stu_summary(stu_id):
  student_name = q.get_student_name(stu_id)
  rows = q.get_student_summary(stu_id)
  return render_template("stu_summary.html", rows=rows, stu_name=student_name)

@app.route("/summary/<string:stu_id>/<string:loc>")
def stu_loc_summary(stu_id, loc):
  student_name = q.get_student_name(stu_id)
  rows = q.get_student_location_summary(stu_id, loc)
  return render_template("stu_loc_summary.html", rows=rows, stu_name=student_name, location=loc, stu_id=stu_id)
  
@app.route("/student", methods=["GET","POST"])
def student():
  if request.method == "GET": # SHOW THE FORM
    rows = q.get_all_students()
    return render_template("stu_form.html", rows=rows)
  else: # PROCESS THE FORM
    stu_id = request.form.get("s_id")
    return redirect(f"/summary/{stu_id}")

@app.route("/signin", methods=["GET","POST"])
def signin():
  # GET Request --> clicked the link
  if request.method == "GET":
    # show a form that allows the user to enter their student id
    return render_template("signinform.html")
  else: # PROCESS FORM
    stu_id = request.form.get("stu_id").upper() #get the student id from the form
    # use the stu_id to see if they have any passes to sign in for
    row_id = q.check_for_pass(stu_id)

    if row_id == 0:
      flash(f"The student id of {stu_id} was not found or hasn't signed out.")
      return redirect("/signin")
    elif row_id == -1:
      flash("ERROR!!! PLEASE SEE MR. FISHEL!!!")
      return redirect("/")
    else: # only one pass found
      # we need to update the passes table
      result = q.sign_back_in(row_id)
      if result == 1: # 1 row was updated
        stu_name = q.get_student_name(stu_id)
        flash(f"Thanks! {stu_name} you have now signed back in!")
        return redirect("/all")
      else:
        return "ERROR - Please contact the webmaster"

@app.route("/signout", methods=["GET","POST"])
def signout():
  if request.method == "GET": 
    # show the form so the student can fill it out
    return render_template("signoutform.html")
  else: 
    # process the form data
    pass_data = {
      # collect the data from the form
      "stu_id" : request.form.get("stu_id").upper(),
      "first" : request.form.get("first").title(),
      "last" : request.form.get("last").title(),
      "loc" : request.form.get("loc"),
      # date and time we will get from our function
      "pass_date" : q.get_today().get("c_date"),
      "out_time" : q.get_today().get("c_time")
    }
    # use a function in queries.py to insert the row to the table
    pass_id = q.insert_pass(pass_data)
    if pass_id:
      flash(f"Pass {pass_id} for {pass_data.get('first')} was created successfully!")
      return redirect("/")
    return "THERE WAS SOME ERROR - NO NEW PASS CREATED!"


@app.route("/pass/<int:id>")
def show_pass(id):
  data = q.get_pass_by_id(id)
  if data:
    return render_template("pass.html", data=data)
  else:
    flash("No pass found!")
    return redirect("/student")

@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_pass(id):
  data = q.get_pass_by_id(id)
  if data:
    if request.method == "GET":
      return render_template("editpass.html", data=data)
    else:
      pass_data = {
        # collect the data from the form
        "student_id" : request.form.get("student_id").upper(),
        "f_name" : request.form.get("f_name").title(),
        "l_name" : request.form.get("l_name").title(),
        "location" : request.form.get("location"),
        "pass_date" : request.form.get("pass_date"),
        "out_time" : request.form.get("out_time"),
        "in_time" : request.form.get("in_time")
      }
      num = q.update_full_pass(id, pass_data)
      if num == 1:
        flash("Update successful!")
        return redirect(f"/pass/{id}")
      else:
        flash("ERROR - Pass was NOT updated")
        return redirect("/")
  else:
    flash("ERROR")
    return redirect("/")
    





if __name__ == "__main__":
  app.run("0.0.0.0", debug=True)