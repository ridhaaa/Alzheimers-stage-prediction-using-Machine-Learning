from flask import Flask,render_template,request,redirect,session,jsonify
from sklearn.naive_bayes import GaussianNB
import datetime

from DBConnection import Db

app = Flask(__name__)
app.secret_key = "abcd"


@app.route('/',methods=['get','post'])
def index():
    return render_template("indexnew.html")


@app.route('/login',methods=['get','post'])
def login():
    if request.method=="POST":
        username=request.form['textfield']
        password=request.form['textfield2']
        db=Db()

        qry = db.selectOne("select * from login where uname='"+username+"' and password='"+password+"'")
        if qry is not None:
            if qry['user_type']=='admin':
                session['login_id'] = qry['login_id']

                session['log']="lin"
                return redirect('/home')
            if qry['user_type'] == 'neurologist':
                session['login_id'] = qry['login_id']

                session['log'] = "lin"
                return redirect('/neurologisthome')
            if qry['user_type'] == 'user':
                session['login_id'] = qry['login_id']

                session['log'] = "lin"
                return redirect('/uhome')
            if qry['user_type'] == 'caretaker':
                session['login_id'] = qry['login_id']

                session['log'] = "lin"
                return redirect('/carehome')
            else:
                return "invalid"
        return "invalid"
    else:
        return render_template("login_index.html")



@app.route('/home')
def home():
    # if session['log'] == "lin":
        return render_template("admin/indexnew.html")
    # else:
    #     return redirect('/')


@app.route('/add_noti',methods=['get','post'])
def add_noti():
    
        if request.method=="POST":
            notification=request.form['textarea']
            db=Db()
            db.insert("insert into notification(notifications,n_date) values('"+notification+"', curdate())")
            return '''<script>alert("added successfully");window.location="/home"</script>'''

        else:
            return render_template("admin/add_noti.html")
    # else:
    #     return redirect('/')



@app.route('/delete_noti/<n_id>')
def delete_noti(n_id):
    
        db = Db()
        db.delete("delete from notification where not_id='"+n_id+"'")
        return redirect('/notification')
    # else:
    #     return redirect('/')




@app.route('/view_approve')
def view_approve():

        db = Db()
        qry = db.select("select * from neurologist, login where neurologist.n_id = login.login_id  and login.user_type='neurologist' ")
        return render_template("admin/view_approved_neuro.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/caretaker')
def caretaker():
    
        db = Db()
        qry = db.select("select * from caretaker")
        return render_template("admin/view_caretaker.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/neuro')
def neuro():
    
        db = Db()
        qry = db.select("select * from neurologist, login where neurologist.n_id = login.login_id  and login.user_type='pending' ")
        return render_template("admin/view_neuro.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/approve/<id>')
def approve(id):

        db = Db()
        db.update("update login set user_type='neurologist' where login_id = '"+id+"'")
        return redirect('/neuro')
    # else:
    #     return redirect('/')



@app.route('/reject/<id>')
def reject(id):
    
        db = Db()
        db.delete("delete from neurologist where n_id='"+id+"'")
        db.delete("delete from login where login_id='"+id+"'")
        return redirect('/neuro')
    # else:
    #     return redirect('/')




@app.route('/notification')
def notification():
    
        db = Db()
        qry = db.select("select * from notification")
        return render_template("admin/view_notification.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/rating')
def rating():
    db = Db()
    res = db.select("select rating.rating,rating.date,caretaker.c_name,neurologist.n_name,rating.r_id from rating,neurologist,caretaker where rating.n_id=neurologist.n_id and rating.c_id = caretaker.cid")

    ar_rt = []

    for im in range(0, len(res)):
        val = str(res[im]['rating'])
        ar_rt.append(val)
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    arr = []

    for rt in ar_rt:
        print(rt)
        a = float(rt)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            arr.append(ar)

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            arr.append(ar)

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            arr.append(ar)

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            arr.append(ar)

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            arr.append(ar)

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            arr.append(ar)

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            arr.append(ar)

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            arr.append(ar)

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            arr.append(ar)

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            arr.append(ar)

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            arr.append(ar)
        print(arr)
    return render_template("admin/view_rating.html",resu=res, r1=arr, ln=len(arr))


@app.route('/accuracy')
def accuracy():

    import pandas as pd
    from sklearn.metrics import accuracy_score
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.svm import LinearSVC
    data = pd.read_csv(
        r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\features.csv")

    #   Extract attributes and labels
    attributes = data.values[1:, 0:5]
    labels = data.values[1:, 5]

    #   Split attributes and labels
    X_train, X_test, Y_train, Y_test = train_test_split(attributes, labels, test_size=0.2)

    # ==================================================================================================================

    rf = RandomForestClassifier()
    rf.fit(X_train, Y_train)
    qry = {'Random Forest':0,'Naive Bayes':0,'SVM':0}
    #   Predict result
    pred = rf.predict(X_test)
    acc=accuracy_score(Y_test, pred)
    print("\nAccuracy : ", round(acc*100, 2), "%")
    qry['Random Forest'] = round(acc * 100, 2)
    # qry.append({
    #     'algm': 'Random forest',
    #     'acc': round(acc * 100, 2)
    # })
    # ==================================================================================================================
    nb = GaussianNB()
    nb.fit(X_train, Y_train)
    #   Predict result
    pred = nb.predict(X_test)
    nbacc = accuracy_score(Y_test, pred)
    print("\nAccuracy : ", round(nbacc * 100, 2), "%")
    qry['Naive Bayes'] = round(nbacc * 100, 2)
    # qry.append({
    #     'algm': 'Naive bayes',
    #     'acc': round(nbacc * 100, 2)
    # })

    # ==================================================================================================================
    svm = LinearSVC()
    svm.fit(X_train, Y_train)

    #   Predict result
    pred = svm.predict(X_test)
    svmacc = accuracy_score(Y_test, pred)
    print("\nAccuracy : ", round(svmacc * 100, 2), "%")
    qry['SVM'] = round(svmacc * 100, 2)
    print(qry)
    # qry.append({
    #     'algm': 'SVM',
    #     'acc': round(svmacc * 100, 2)
    # })
    #

    # ==================================================================================================================





    return render_template("admin/accuracy.html", data=qry)
    # else:
    #     return redirect('/')


    # ==================================================================================================================





    #return render_template("admin/accuracy.html", data=qry)
    # else:
    #     return redirect('/')


#=========================================================================================================================
@app.route('/nregister',methods=['get','post'])
def nregister():
    
        if request.method=="POST":
            username=request.form['uname']
            email = request.form['email']
            phone = request.form['phone']
            password=request.form['pass']

            db=Db()
            qry = db.insert("insert into login(uname,password,user_type) VALUES( '" + username + "' ,'" + password + "', 'pending' )")
            qry = db.insert("insert into neurologist(n_id,n_name,email,phone) VALUES('"+str(qry)+"','"+username+"','"+email+"','"+phone+"')")
            return '''<script>alert("added successfully");window.location="/"</script>'''

        else:
            return render_template("neurologist1/register.html")
    # else:
    #         return redirect('/')


@app.route('/neurologisthome')
def neurologisthome():
    
        return render_template("neurologist1/indexnew.html")
    # else:
    #     return redirect('/')



@app.route('/profile')
def profile():
    
        db=Db()
        qry = db.selectOne("select * from neurologist where n_id='"+str(session['login_id'])+"'")
        return render_template("neurologist1/view_profile.html",data = qry)
    # else:
    #     return redirect('/')


@app.route('/schedule',methods=['get','post'])
def schedule():
    
        if request.method == "POST":
            dates = request.form['dates']
            totime = request.form['totime']
            ftime = request.form['ftime']
            db=Db()
            qry = db.insert("insert into schedule(s_id,n_id,dates,to_time,f_time) VALUES('' ,'"+str(session['login_id'])+"','" + dates + "' ,'" + totime + "', '"+ftime+"' )")
            return '''<script>alert("added successfully");window.location="/schedule"</script>'''
        else:
            db = Db()
            qry = db.select("select * from schedule where schedule.n_id='"+str(session['login_id'])+"'")
            return render_template("neurologist1/add_schedule.html", data=qry)
            # else:
            #     return redirect('/')


@app.route('/delete_schedule/<uid>')
def delete_schedule(uid):
    db = Db()
    db.delete("delete from schedule where s_id='" + uid + "'")
    return redirect('/schedule')
    # else:
    #     return redirect('/')

@app.route('/appointment/')
def appointment():
    db = Db()
    res=db.select("select app_id,caretaker.c_name,patient.uname,schedule.dates,schedule.f_time,schedule.to_time from appointment,caretaker,schedule ,patient where appointment.c_id=patient.user_id and appointment.s_id=schedule.s_id and caretaker.cid=patient.c_id and schedule.n_id='"+str(session['login_id'])+"'" )
    return render_template("neurologist1/view_appointment.html",data=res)



@app.route('/tips', methods=['get', 'post'])
def tips():
    
        if request.method == "POST":
            tip = request.form['tips']
            db = Db()
            qry = db.insert("insert into tips(tip_id, tip) VALUES('', '"+tip+"' )")
            return '''<script>alert("added successfully");window.location="/tips"</script>'''
        else:
            db = Db()
            qry = db.select("select * from tips")
            return render_template("neurologist1/add_tips.html", data=qry)
            # else:
            #     return redirect('/')


@app.route('/delete_tips/<uid>')
def delete_tips(uid):
    db = Db()
    db.delete("delete from tips where tip_id='" + uid + "'")
    return redirect('/tips')
    # else:
    #     return redirect('/')

@app.route('/exercise/<uid>', methods=['get', 'post'])
def exercise(uid):
    
        if request.method == "POST":
            exercise = request.form['exercise']
            db = Db()
            qry = db.insert("insert into suggest VALUES('', '"+exercise+"','"+uid+"' )")
            return '''<script>alert("added successfully");window.location="/appointment"</script>'''
        else:
            return render_template("neurologist1/suggest_excerise.html")

    # else:
    #     return redirect('/')

@app.route('/nnotification')
def nnotification():
    
        db = Db()
        qry = db.select("select * from notification")
        return render_template("neurologist1/view_notification.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/nrating')
def nrating():

    db = Db()
    res = db.select("select * from rating,caretaker where caretaker.cid = rating.c_id and n_id = '"+str(session['login_id'])+"'")
    ar_rt = []

    for im in range(0, len(res)):
        val = str(res[im]['rating'])
        ar_rt.append(val)
    fs = "/static/star/full.jpg"
    hs = "/static/star/half.jpg"
    es = "/static/star/empty.jpg"
    arr = []

    for rt in ar_rt:
        print(rt)
        a = float(rt)

        if a >= 0.0 and a < 0.4:
            print("eeeee")
            ar = [es, es, es, es, es]
            arr.append(ar)

        elif a >= 0.4 and a < 0.8:
            print("heeee")
            ar = [hs, es, es, es, es]
            arr.append(ar)

        elif a >= 0.8 and a < 1.4:
            print("feeee")
            ar = [fs, es, es, es, es]
            arr.append(ar)

        elif a >= 1.4 and a < 1.8:
            print("fheee")
            ar = [fs, hs, es, es, es]
            arr.append(ar)

        elif a >= 1.8 and a < 2.4:
            print("ffeee")
            ar = [fs, fs, es, es, es]
            arr.append(ar)

        elif a >= 2.4 and a < 2.8:
            print("ffhee")
            ar = [fs, fs, hs, es, es]
            arr.append(ar)

        elif a >= 2.8 and a < 3.4:
            print("fffee")
            ar = [fs, fs, fs, es, es]
            arr.append(ar)

        elif a >= 3.4 and a < 3.8:
            print("fffhe")
            ar = [fs, fs, fs, hs, es]
            arr.append(ar)

        elif a >= 3.8 and a < 4.4:
            print("ffffe")
            ar = [fs, fs, fs, fs, es]
            arr.append(ar)

        elif a >= 4.4 and a < 4.8:
            print("ffffh")
            ar = [fs, fs, fs, fs, hs]
            arr.append(ar)

        elif a >= 4.8 and a <= 5.0:
            print("fffff")
            ar = [fs, fs, fs, fs, fs]
            arr.append(ar)
        print(arr)
    return render_template("neurologist1/view_rating.html", resu=res, r1=arr, ln=len(arr))
#=========================================================================================================================
@app.route('/uregister',methods=['get','post'])
def uregister():
    if request.method=="POST":
        username=request.form['uname']
        email = request.form['email']
        phone = request.form['phone']
        password=request.form['pass']

        db=Db()
        qry = db.insert("insert into login(uname,password,user_type) VALUES( '" + username + "' ,'" + password + "', 'user' )")
        qry = db.insert("insert into user(user_id,username,email) VALUES('"+str(qry)+"','"+username+"','"+email+"')")
        return '''<script>alert("added successfully");window.location="/"</script>'''

    else:
        return render_template("user/register.html")

@app.route('/uhome')
def uhome():
    
        return render_template("user/uhome.html")
    # else:
    #     return redirect('/')


@app.route('/uprofile')
def uprofile():
    
        db=Db()
        qry = db.selectOne("select * from user where user_id = '"+str(session['login_id'])+"'")
        return render_template("user/view_user.html",data = qry)
    # else:
    #     return redirect('/')


#=========================================================================================================================
@app.route('/cregister',methods=['get','post'])
def cregister():

    if request.method=="POST":
        username=request.form['uname']
        email = request.form['email']
        phone = request.form['phone']
        password=request.form['pass']

        db=Db()
        qry = db.insert("insert into login(uname,password,user_type) VALUES( '" + username + "' ,'" + password + "', 'caretaker' )")
        qry = db.insert("insert into caretaker(cid,c_name,email,phone) VALUES('"+str(qry)+"','"+username+"','"+email+"','"+phone+"')")
        return '''<script>alert("added successfully");window.location="/"</script>'''

    else:
        return render_template("caretaker/caretaker_register.html")

@app.route('/carehome')
def carehome():
    
        return render_template("caretaker/indexnew.html")
    # else:
    #     return redirect('/')


@app.route('/cprofile')
def cprofile():
    
        db=Db()
        qry = db.selectOne("select * from caretaker where cid = '"+str(session['login_id'])+"'")
        return render_template("caretaker/caretaker_view_profile.html",data = qry)
    # else:
    #     return redirect('/')


@app.route('/addpatient',methods=['get','post'])
def addpatient():
    
        if request.method == "POST":
            username = request.form['name']
            email = request.form['email']
            password = request.form['pass']
            db = Db()
            qry = db.insert("insert into login(uname,password,user_type) VALUES( '" + username + "' ,'" + password + "', 'user' )")
            db.insert("insert into patient VALUES( '"+str(qry)+"','" + username + "' ,'" + email + "','"+str(session['login_id'])+"','"+password+"')")

            return '''<script>alert("added successfully");window.location="/viewpatient#aaa"</script>'''
        else:
            return render_template("caretaker/add_user.html")
    # else:
    #     return redirect('/')


@app.route('/viewpatient')
def viewpatient():
    
        db = Db()
        qry = db.select("select patient.uname,patient.user_id,patient.email from patient, caretaker where patient.c_id = caretaker.cid and patient.c_id='"+str(session['login_id'])+"' ")
        return render_template("caretaker/view_user.html", data=qry)
    # else:
    #     return redirect('/')
    #

@app.route('/cnotification')
def cnotification():
    
        db = Db()
        qry = db.select("select * from notification")
        return render_template("caretaker/view_notificat.html",data=qry)
    # else:
    #     return redirect('/')


@app.route('/userdetails/<uid>')
def userdetails(uid):
    session['uid']=uid
    return render_template("caretaker/userhome.html", uid=uid)
    # else:
    #     return redirect('/')


@app.route('/add_dates/<uid>',methods=['get','post'])
def add_dates(uid):
    
        if request.method == "POST":
            dates = request.form['dates']
            description = request.form['description']
            db = Db()
            qry = db.insert("insert into imp_date(date_id,user_id,dates,description) VALUES( '','"+uid+"','" + dates + "' ,'" + description + "' )")

            return '''<script>alert("added successfully");window.location="/userdetails/<uid>#aaa"</script>'''
        else:
            db = Db()
            qry = db.select("select * from imp_date where user_id = '"+ uid +"'")
            return render_template("caretaker/add_imp_date.html",data=qry)
    # else:
    #     return redirect('/')


# @app.route('/view_imp_date')
# def view_imp_date():
#     db = Db()
#     qry = db.select("select * from imp_date")
#     return render_template("caretaker/add_imp_date.html", data=qry)
    # else:
    #     return redirect('/')


@app.route('/delete_imp_date/<uid>')
def delete_imp_date(uid):
    db = Db()
    db.delete("delete from imp_date where date_id='" + uid + "'")
    return redirect('/add_dates/<uid>#aaa')
    # else:
    #     return redirect('/')


@app.route('/add_notes/<uid>', methods=['get', 'post'])
def add_notes(uid):
    
        if request.method == "POST":
            notes = request.form['notes']
            db = Db()
            qry = db.insert("insert into imp_notes(note_id,user_id,dates,notes) VALUES( '','" + uid + "',curdate() ,'" + notes + "' )")

            return '''<script>alert("added successfully");window.location="/userdetails/<uid>#aaa"</script>'''
        else:
            db = Db()
            qry = db.select("select * from imp_notes where user_id = '"+ uid +"'")
            return render_template("caretaker/add_imp_notes.html", data=qry)
            # else:
    #     return redirect('/')

@app.route('/delete_imp_notes/<uid>')
def delete_imp_notes(uid):
    db = Db()
    db.delete("delete from imp_notes where note_id='" + uid + "'")
    return redirect('/add_notes/<uid>#aaa')
    # else:
    #     return redirect('/')

@app.route('/deletepatient/<uid>')
def deletepatient(uid):
    
        db = Db()
        db.delete("delete from login where login_id='" + uid + "'")
        db.delete("delete from patient where user_id='" + uid + "'")
        return redirect('/viewpatient#aaa')
    # else:
    #     return redirect('/')

@app.route('/fam_person/<uid>', methods=['get', 'post'])
def fam_person(uid):
    
        if request.method == "POST":
            pname = request.form['name']
            photo = request.files['photo']
            relation = request.form['relation']
            date=datetime.datetime.now().strftime("%y%m%d-%H%M%S")
            photo.save(r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\pic\\"+date+'.jpg')
            w="/static/pic/"+date+'.jpg'
            db = Db()
            db.insert("insert into familiar_person(fam_id,user_id,pname,photo,relation) VALUES( '','"+uid+"','" + pname + "' ,'" + str(w) + "' ,'" + relation + "' )")

            return '''<script>alert("added successfully");window.location="/userdetails/<uid>#aaa"</script>'''
        else:
            return render_template("caretaker/add_familiar_person.html")
    # else:
    #     return redirect('/')


@app.route('/viewperson/<id>')
def viewperson(id):
    
        db = Db()
        qry = db.select("select pname,photo,relation,fam_id from familiar_person where user_id = '"+ id +"' ")
        return render_template("caretaker/view_familiar_person.html", data=qry)
    # else:
    #     return redirect('/')


@app.route('/deletefam/<uid>')
def deletefam(uid):
    db = Db()
    db.delete("delete from familiar_person where fam_id='" + uid + "'")
    return '<script>alert("Removed successfully");window.location="/viewperson/' + str(session['iid']) + '"</script>'

@app.route('/view_neurologist/<id>')
def view_neurologist(id):
    db = Db()
    qry = db.select("select * from neurologist")
    return render_template("caretaker/view_neurologist.html", data=qry)


@app.route('/send_rating/<id>',methods=['get','post'])
def send_rating(id):
    if request.method=="POST":
        db = Db()
        rating=request.form['star']
        db.insert("insert into rating  (c_id,n_id,rating,date)VALUES ('"+str(session['login_id'])+"','"+id+"','"+rating+"',curdate())")
        return '''<script>alert("send successfully");window.location="/view_neurologist/<id>#aaa"</script>'''
    else:

        return render_template("Caretaker/rate.html")
@app.route('/view_schedule/<id>')
def view_schedule(id):
    db = Db()
    qry = db.select("select s_id,dates,f_time,to_time from schedule where  schedule.n_id = '"+id+"' ")
    return render_template("caretaker/view_schedule.html", data=qry)


    # else:
    #     return redirect('/')
@app.route('/view_appointments/<id>')
def view_appointments(id):
    session['iid']=id
    db = Db()
    qry = db.select("select app_id,neurologist.n_name,schedule.dates,f_time,to_time from appointment,neurologist,schedule where neurologist.n_id = schedule.n_id and appointment.s_id = schedule.s_id and appointment.c_id = '"+id+"'")
    print("select app_id,neurologist.n_name,schedule.dates,f_time,to_time from appointment,neurologist,schedule where neurologist.n_id = schedule.n_id and appointment.c_id = '"+id+"'")
    return render_template('caretaker/view_appointments.html',data=qry)

@app.route('/book/<s_id>')
def book(s_id):
    db = Db()
    db.insert("insert into appointment(c_id,dates,s_id,app_id) VALUES ( '"+str(session['uid'])+"' , curdate() , '"+s_id+"','' )")
    return redirect('/view_appointments/'+str(session['uid']))

@app.route('/remove/<id>')
def remove(id):
    db = Db()
    db.delete("delete from appointment where app_id='" + id + "'")
    return '<script>alert("Removed successfully");window.location="/view_appointments/'+str(session['iid'])+'"</script>'


@app.route('/view_exercise/<id>')
def view_exercise(id):
    db = Db()
    qry = db.select("select app_id,suggest,tip from suggest,tips  ")
    return render_template("Caretaker/view_suggest.html", data=qry)



@app.route('/logout')
def logout():
    # session.clear()
    session['log']=""
    return redirect('/')
#=========================================================================================================================


# =========================================USER MODULE========================================================================
@app.route('/andlogin',methods=['post'])
def andlogin():
    username=request.form['name']
    password=request.form['password']
    db=Db()
    res=db.selectOne("select * from login where uname='"+username+"' and password='"+password+"'")
    return jsonify(status="ok",lid=res['login_id'],type=res['user_type'])
@app.route('/impdate',methods=['post'])
def impdate():
    login=request.form['id']
    db=Db()
    res= db.select("select * from imp_date where user_id='"+login+"'")
    return jsonify(status="ok",data=res)
@app.route('/impnote',methods=['post'])
def impnote():
    login=request.form['id']
    db=Db()
    res= db.select("select * from imp_notes where user_id='"+login+"'")
    return jsonify(status="ok",data=res)

@app.route('/viewprofile',methods=['post'])
def viewprofile():
    login=request.form['login']
    db=Db()
    res=db.selectOne("select patient.email as em,patient.*,caretaker.* from patient,caretaker where patient.c_id=caretaker.cid and user_id='"+login+"' ")
    return jsonify(status="ok", data=res)

@app.route('/viewfamperson',methods=['post'])
def viewfamperson():
    login=request.form['lid']
    db=Db()
    res=db.select("select * from patient,familiar_person where patient.user_id=familiar_person.user_id and familiar_person.user_id='"+login+"' ")
    return jsonify(status="ok", data=res)


@app.route('/viewprediction',methods=['post'])
def viewprediction():
    login=request.form['id']
    db=Db()
    res=db.select("select  prediction_id,report,result from prediction  where prediction.user_id='"+login+"' order by prediction_id  desc")
    return jsonify(status="ok", data=res)

@app.route('/viewsuggestion',methods=['post'])
def viewsuggestion():
    login=request.form['lid']
    db=Db()
    res=db.select("select * from suggest,appointment,patient where suggest.app_id=appointment.app_id and appointment.c_id=patient.user_id and patient.user_id='"+login+"'")
    return jsonify(status="ok", data=res)

####################################################


@app.route('/predict/<uid>', methods=['get','post'])
def predict(uid):
    if request.method == "POST":
        photo = request.files['photo']
        d=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        photo.save(r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\pic\\" +d+ '.jpg')
        from test import test_image
        obj=test_image(r"C:\Users\hp\Dropbox\PC\Desktop\alzher\static\pic\\" +d+ '.jpg')
        if obj == "MildDemented" or obj == "ModerateDemented" or obj == "VeryMildDemented":
            print("Result : Yes")
            print("Stage: ", obj)
        elif obj == "NonDemented":
            print("Result : No")
        path='/static/pic/'+d+'.jpg'
        db=Db()
        db.insert("insert into prediction(prediction_id,report,user_id,result,date) VALUES ('','"+path+"','"+str(uid)+"','"+str(obj)+"',curdate())")
        return render_template("caretaker/predict.html",data=obj)
    else:
        return render_template("caretaker/predict.html")



@app.route('/prediction/<uid>')
def prediction(uid):
    db = Db()
    qry = db.select("select prediction_id,report,user_id,result,date from prediction where user_id = '"+uid+"' ")
    return render_template("caretaker/prediction.html", data=qry)









if __name__ == '__main__':
    app.run(debug=True,port=4000,host="0.0.0.0")
