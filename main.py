from flask import Flask, render_template, request, redirect, url_for, flash, session
from Model import db, Users, Admin, RankM, Indawo, Complaint, TaxiDriver
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS
# from flask_login import (
#     LoginManager,
#     UserMixin,
#     login_user,
#     logout_user,
#     login_required
# )

manager = Flask(__name__)

CORS(
    manager,
    resources={
        r"/*": {
            "origins": "*"
        }
    }
)
manager.secret_key = "ntando'sg_group_change_later"

manager.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
manager.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# login_manager = LoginManager()
# login_manager.init_app(manager)
# login_manager.login_view = "SignIn"

db.init_app(manager)

with manager.app_context():
    db.create_all()


# with manager.app_context():
#     Indawo.__table__.drop(db.engine, checkfirst=True)

@manager.route("/")
def home():
    return render_template("1_Home.html")

@manager.route("/usebase")
def userdashboard():
    return render_template("10.0_userbase.html")

@manager.route("/managerbase")
def managerbase():
    return render_template("11.0_manager.html")

@manager.route("/adminprofile")
def adminProfile():
    return render_template("8_admin_profile.html")

@manager.route("/login")
def login():
    return render_template("3_Login.html")

@manager.route("/about")
def about():
    return render_template("4_About.html")

@manager.route("/taxidrivers")
def taxi_drivers():
    users = TaxiDriver.query.all()
    return render_template("taxi_drivers.html", users=users)

@manager.route("/addtaxidriver")
def add_taxi_drivers():
    return render_template("addTaxiDriver.html")

@manager.route("/feature")
def feature():
    return render_template("2_Features.html")

def count_users(users):
    number = 0
    for user in users:
        number+=1
    return number

@manager.route("/5_AdminDashboard")
def dash():
    no_d=TaxiDriver.query.all()
    taxiDriver=count_users(no_d)
    no_admin=Admin.query.all()
    admin=count_users(no_admin)
    no_commuter=Users.query.all()
    commuter=count_users(no_commuter)
    no_mngr=RankM.query.all()
    mngr=count_users(no_mngr)
    return render_template("5_AdminDashboard.html", taxiDriver=taxiDriver, admin=admin, commuter=commuter, mngr=mngr)

@manager.route("/manager_profile")
def manager_profile():
    return render_template("11.3_manager_profile.html")

@manager.route("/register_admin")
def reg_admin():
    users = Admin().query.all()
    return render_template("7_register_admin.html", users=users)
@manager.route("/api/add")
def add():
    return render_template("/add.html")

@manager.route("/requests")
def requests():
    izindawo = Indawo().query.all()
    available_drivers = TaxiDriver.query.all()
    return render_template("11.1_requests.html", izindawo=izindawo, available_drivers=available_drivers)

@manager.route("/user_complaints")
def user_complaints():
    complaints = Complaint.query.all()
    return render_template("11.2_complaints.html", complaints=complaints)

@manager.route("/rankManager")
def rankM():
    page = request.args.get('page', 1, type=int)
    
    pagination = RankM.query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    managers = pagination.items

    return render_template("6_RankManager.html", managers=managers,
        pagination=pagination)




@manager.route('/edit_manager/<int:manager_id>', methods=["POST", "GET"])
def edit_manager(manager_id):

    manager = RankM.query.get_or_404(manager_id)
    
    if request.method == 'POST':

        manager.name = request.form['name']
        manager.surname = request.form['surname']
        manager.email = request.form['email']
        manager.phone_no = request.form['phone_no']

        db.session.commit()
    return render_template("edit_manager.html", manager=manager)


@manager.route('/changepassword/<int:admin_id>', methods=['GET', 'POST'])
def admin_change_password(admin_id):

    errors = {}

    user = Admin.query.filter_by(id=admin_id).first()

    if not user:
        return "Admin not found", 404

    if request.method == 'POST':

        old_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        conf_password = request.form.get("confirm_password", "")

        if new_password != conf_password:
            flash("The passwords do not match.", "conf_password")
            return render_template(
                "8_admin_profile.html",
                
            )

        if not check_password_hash(user.password, old_password):
            flash("Incorrect current password.", "curr_pass")
            return render_template(
                "8_admin_profile.html",
                
            )

        if errors:
            return render_template(
                "8_admin_profile.html",
                
            )

        user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Successfully changed password!", "changed")

        return redirect(url_for('adminProfile',
                                admin_id=admin_id))

    return render_template(
        "8_admin_profile.html",
        errors=errors
    )


@manager.route('/managerchangepassword/<int:manager_id>', methods=['GET', 'POST'])
def manager_change_password(manager_id):

    errors = {}

    user = RankM.query.filter_by(id=manager_id).first()

    if not user:
        return "manager not found", 404

    if request.method == 'POST':

        old_password = request.form.get("current_password", "")
        new_password = request.form.get("new_password", "")
        conf_password = request.form.get("confirm_password", "")

        if new_password != conf_password:
            flash("The passwords do not match.", "conf_password")
            return render_template(
                "11.3_manager_profile.html",
                
            )

        if not check_password_hash(user.password, old_password):
            flash("Incorrect current password.", "incorrect")
            return render_template(
                "11.3_manager_profile.html",
                
            )

        if errors:
            return render_template(
                "11.3_manager_profile.html",
                
            )

        user.password = generate_password_hash(new_password)

        db.session.commit()

        flash("Successfully changed password!", "shintshekile")

        return redirect(url_for('manager_profile',
                                manager_id=manager_id))

    return render_template(
        "11.3_manager_profile.html",
        errors=errors
    )



    

@manager.route('/delete-manager/<int:manager_id>', methods=['POST'])
def delete_manager(manager_id):
    user = RankM.query.get_or_404(manager_id)
    
    db.session.delete(user)
    db.session.commit()

    # flash("User deleted successfully.", "success")

    
    return redirect(url_for('rankM'))


@manager.route("/add_rmanager")
def add_rmanager():
    return render_template("Add_RManager.html")

@manager.route("/addManagerDetails", methods=["POST", "GET"])
def addManagerDetails():

    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    password=request.form["password"]
    phone_no=request.form["phone_no"]

    manager = RankM(
        name = name,
        surname = surname,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no
    )

    db.session.add(manager)
    db.session.commit()

    flash("Successfully added", "success")

    return redirect(url_for("rankM"))

@manager.route("/commuter")
def commuters():

    page = request.args.get('page', 1, type=int)

    pagination = Users.query.paginate(
        page=page,
        per_page=10,
        error_out=False
    )

    users = pagination.items

    return render_template("/commuters.html", users=users,
        pagination=pagination)

@manager.route("/addcommuter")
def addCommuter():
    return render_template("addcommmuter.html")

@manager.route("/addCommuterDetails", methods=["POST", "GET"])
def addCommuterDetails():

    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    password=request.form["password"]
    phone_no=request.form["phone_no"]

    commuter = Users(
        name = name,
        surname = surname,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no
    )

    db.session.add(commuter)
    db.session.commit()

    flash("Successfully added", "success")

    return redirect(url_for("commuters"))


@manager.route("/addTaxiDriver", methods=["POST", "GET"])
def addTaxiDriver():

    name=request.form["name"]
    surname=request.form["surname"]
    email=request.form["email"]
    password=request.form["password"]
    phone_no=request.form["phone_no"]
    taxi_no=request.form["taxi_no"]

    taxiDriver = TaxiDriver(
        name = name,
        surname = surname,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no,
        taxi_no = taxi_no
    )

    db.session.add(taxiDriver)
    db.session.commit()

    flash("Successfully added", "success")

    return redirect(url_for("taxi_drivers"))




@manager.route("/assign-driver/<int:location_id>", methods=["POST"])
def assignDriver(location_id):
    location = Indawo.query.get_or_404(location_id)

    driver_id = request.form.get("driver_id", type=int)

    if driver_id is None:
        flash("Please select a driver.", "error")
        return redirect(url_for("requests"))

    driver = TaxiDriver.query.get(driver_id)

    if driver is None:
        flash("Selected driver does not exist.", "error")
        return redirect(url_for("requests"))

    try:
        location.assigned_driver = driver.name
        db.session.commit()
        print(location)

        flash(
            f"Driver {driver.name} {driver.surname} assigned successfully.",
            "success"
        )

    except Exception as e:
        db.session.rollback()
        print("Driver assignment error:", e)
        flash("Failed to assign driver.", "error")

    return redirect(url_for("requests"))



# for users

@manager.route("/commuterDetails", methods=["POST", "GET"])
def CommuterDetails():

    name=request.form["name"]
    # surname=request.form["surname"]
    email=request.form["email"]
    password=request.form["password"]
    phone_no=request.form["phone_no"]

    commuter = Users(
        name = name,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no
    )

    db.session.add(commuter)
    db.session.commit()

    flash("Successfully added", "success")

    return redirect(url_for("login"))


@manager.route("/dailyActiviy")
def dailyActiviy():
    locations=Indawo().query.all()
    return render_template("dailyActivities.html", locations=locations)

@manager.route("/delete-admin/<int:admin_id>", methods=["POST"])
def delete_admin(admin_id):

    admin = Admin.query.get_or_404(admin_id)

    db.session.delete(admin)
    db.session.commit()

    flash("Administrator deleted successfully.", "success")

    return redirect(url_for("reg_admin"))

@manager.route("/api/add")
@manager.route("/add_admin", methods = ["POST", "GET"])
def add_admin():
    name =request.form["name"]
    surname =request.form["surname"]
    email = request.form["email"]
    password =request.form["password"]
    phone_no=request.form["phone_no"]

    existing_admin = Admin.query.filter_by(email=email).first()

    if existing_admin:
        flash("An admin with this email already exists.", "danger")
        return redirect(url_for("add_admin"))

    new_admin=Admin(
        name=name,
        surname=surname,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no
    )

    db.session.add(new_admin)
    db.session.commit()

    flash("Successfully added", "success")

    return redirect(url_for("reg_admin"))

@manager.route("/signIn", methods=["POST", "GET"])
def SignIn():

    email = request.form["email"]
    password = request.form["password"]

    user = Admin.query.filter_by(email=email).first()
    commuter = Users.query.filter_by(email=email).first()
    manager = RankM.query.filter_by(email=email).first()
    txdvr = TaxiDriver.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        # session["user_id"] = user.id
        session["user_id"] = user.id
        session["name"] = user.name
        session["surname"] = user.surname
        session["email"] = user.email
        session["phone"] = user.phone_no

        no_d=TaxiDriver.query.all()
        taxiDriver=count_users(no_d)
        no_admin=Admin.query.all()
        admin=count_users(no_admin)
        no_commuter=Users.query.all()
        commuter=count_users(no_commuter)
        no_mngr=RankM.query.all()
        mngr=count_users(no_mngr)

        name = user.name

        return render_template("5_AdminDashboard.html", taxiDriver=taxiDriver, admin=admin, commuter=commuter, mngr=mngr)

    if commuter  and check_password_hash(commuter.password, password):
    
            session["user_id"] = commuter.id

            session["name"] = commuter.name
    
            name = commuter.name
    
            return render_template("10.0_userbase.html", name = name)

    if manager and check_password_hash(manager.password, password):
    
            session["user_id"] = manager.id
            session["name"] = manager.name
            session["surname"] = manager.surname
            session["email"] = manager.email
            session["phone"] = manager.phone_no

            available_drivers = TaxiDriver.query.all()


    
            name = manager.name
    
            return redirect(url_for('requests', name = name, available_drivers=available_drivers))

    if txdvr  and check_password_hash(txdvr.password, password):
        
                session["user_id"] = txdvr.id
    
                session["name"] = txdvr.name
        
                name = txdvr.name
        
                return redirect(url_for("driver_dashboard"))
    

    flash("Invalid username or password", "danger")
    return redirect(url_for("login"))

@manager.route('/delete-request/<int:request_id>', methods=['POST'])
def delete_request(request_id):

    request = Indawo.query.get_or_404(request_id)
    locations=Indawo.query.all()

    db.session.delete(request)
    db.session.commit()

    flash("request deleted successfully.", "success")

    return render_template("dailyActivities.html", locations=locations)


@manager.route('/delete-user/<int:user_id>', methods=['POST'])
def delete_user(user_id):

    user = Users.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    flash("User deleted successfully.", "success")

    return redirect(url_for('commuters'))

@manager.route('/delete-taxidriver/<int:taxid_id>', methods=['POST'])
def delete_taxidriver(taxid_id):

    user = TaxiDriver.query.get_or_404(taxid_id)

    db.session.delete(user)
    db.session.commit()

    flash("taxi driver deleted successfully.", "success")

    return redirect(url_for('taxi_drivers'))



@manager.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):

    user = Users.query.get_or_404(user_id)

    if request.method == 'POST':

        user.name = request.form['name']
        user.surname = request.form['surname']
        user.email = request.form['email']
        user.phone_no = request.form['phone_no']

        db.session.commit()

        # flash("User updated successfully.", "success")

        return redirect(url_for('commuters'))

    return render_template(
        'edit.html',
        user=user
    )

@manager.route("/signInCommuter", methods=["POST"])
def SignInCommuter():

    data = request.get_json()

    email = data["email"]
    password = data["password"]
    

    user = Users.query.filter_by(email=email).first()

    if user and check_password_hash(user.password, password):

        session["user_id"] = user.id

        return {
            "success": True,
            "name": user.name
        }

    return {
        "success": False,
        "message": "Invalid username or password"
    }


@manager.route("/register_commuter", methods = ["POST", "GET"])
def regisiterUser():
    data = request.get_json()
    
    email = data["email"]
    password = data["password"]
    phone_no = data["phone"]
    name = data["name"]

    exist_commuter = Users.query.filter_by(email=email).first()

    if exist_commuter:
        return {
                "success": False,
                "message": "commuter with this email already exist"
            }

    commuter=Users(
        name=name,
        email = email,
        password = generate_password_hash(password),
        phone_no=phone_no
    )

    db.session.add(commuter)
    db.session.commit()

    return {
                "success": True,
                "name": commuter.name
            }


@manager.route("/register_user")
def register_commuter():
    return render_template('3.1_Register.html')


@manager.route("/complaint", methods=["GET", "POST"])
def file_complaint():

    if request.method == "POST":

        name = request.form["name"]
        complaint_type = request.form["complaint_type"]
        location = request.form["location"]
        details = request.form["details"]

        complaint = Complaint(
            name=name,
            complaint_type=complaint_type,
            location=location,
            details=details,
            status="Pending"
        )

        db.session.add(complaint)
        db.session.commit()

        return redirect(url_for("file_complaint"))

    return render_template("10.1_file_complint.html")


@manager.route("/request_taxi", methods=["GET", "POST"])
def request_taxi():

    if request.method == "POST":

        location = request.form["location"]
        how_many = request.form["how_many"]
        fk_id=request.form["fk_id"]
        

        Request = Indawo(
           
            location=location,
            how_many= how_many,
            fk_id=fk_id,
        )

        db.session.add(Request)
        db.session.commit()
        flash("successfully submitted", "success")

        return redirect(url_for("request_taxi"))

    return render_template("10.0_userbase.html")



@manager.route("/update-complaint-status/<int:complaint_id>", methods=["POST"])
def update_complaint_status(complaint_id):

    complaint = Complaint.query.get_or_404(complaint_id)

    complaint.status = request.form["status"]

    db.session.commit()

    return redirect(url_for("user_complaints"))



@manager.route("/logout")
def logout():

    session.clear()

    flash("You have been logged out successfully.", "success")

    return redirect(url_for("login"))


# Ama endpoint ka Driver

@manager.route("/api/driver_base")
def d_home():
    return render_template('driver/driver_base.html')


def bala(List):
    bangaki=0
    for i in List:
        bangaki+=1
    return bangaki

@manager.route("/api/driver_dashboard")
def driver_dashboard():
    current_jobs = Indawo.query.filter(
    Indawo.status != "Completed",
    Indawo.assigned_driver == session["name"]
    ).count()

    completed = Indawo.query.filter(Indawo.assigned_driver == session["name"], Indawo.status=="Completed").all()
    bangaki = bala(completed)
    return render_template('driver/dashboard.html', current_jobs=current_jobs, bangaki=bangaki)

@manager.route("/api/currentjob")
def currentJob():
    current_jobs = Indawo.query.filter_by(assigned_driver=session["name"]).all()
    return render_template('driver/current_job.html', current_jobs=current_jobs)




@manager.route("/update_trip_status/<int:job_id>", methods=["POST"])
def update_trip_status(job_id):

    indawo = Indawo.query.get_or_404(job_id)

    indawo.status = request.form["status"]

    db.session.commit()

    return redirect(url_for("currentJob"))


@manager.route("/myrequests", methods=["POST", "GET"])
def myRequests():
    if request.method == "GET":

        requests = Indawo.query.filter(Indawo.fk_id==session["user_id"]).all()
        for req in requests:
            print(req.assigned_driver)
        return render_template("10.2_my_requests.html", requests=requests)
    

@manager.route("/deleterequests/<int:request_id>", methods=["POST", "GET"])
def deleteRequest(request_id):
    
    if request.method == "POST":
        requests = Indawo.query.filter_by(id=request_id).first()
        db.session.delete(requests)
        db.session.commit()

        flash("successfully deleted", "deleted")
        return redirect(url_for('myRequests'))

    



if __name__ == "__main__":
    manager.run(debug=True, port = 8080)