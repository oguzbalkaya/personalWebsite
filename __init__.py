from functools import wraps
from flask_mysqldb import MySQL
from flask import Flask,render_template,flash,redirect,url_for,session,request,send_file
from forms import *
from information import *
from datetime import datetime
from math import ceil
from mailsettings import SendMail

#### app
app = Flask(__name__)
app.secret_key = "oguzbalkayapersonalwebsite"
####

####MySQL Connection
app.config["MYSQL_HOST"] = info['MYSQL_HOST']
app.config["MYSQL_USER"] = info['MYSQL_USER']
app.config["MYSQL_PASSWORD"] = info['MYSQL_PASSWORD']
app.config["MYSQL_DB"] = info['MYSQL_DB']
app.config["MYSQL_CURSORCLASS"] = info['MYSQL_CURSORCLASS']
mysql = MySQL(app)

##### Decorators #####
def login_required(f):
    @wraps(f)
    def decorated_function(*args,**kwargs):
        if "logged_in" in session:

            return f(*args,**kwargs)
        else:
            return redirect(url_for("index"))
    return decorated_function

#### Pages

@app.route("/list")
@app.route("/list/")
def list_():
    return redirect("/list/1")
@app.route("/read")
@app.route("/read/")
def read_():
    return redirect("/list/1")


#######   Admin pages.    #########
@app.route("/admin",methods=["POST","GET"])
def admin():
    loginForm = AdminLoginForm(request.form)
    controlDatas = {}
    if request.method == "POST" and loginForm.validate():
        email = loginForm.username.data
        password = loginForm.password.data
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM admin WHERE username='{}' and password='{}'".format(email, password)
        cursor.execute(query)
        controlDatas = cursor.fetchall()
        if len(controlDatas) == 0:
            flash(message="Yanlış kullanıcı adı veya şifre.", category="warning")
        else:
            session["logged_in"] = True
            session["member_id"] = controlDatas[0]["id"]
            session["member_name"] = controlDatas[0]["name"]

            return redirect(url_for("dashboard"))
    return render_template("admin/admin.html", title="Yönetici Girişi", info=info, form=loginForm)


@app.route("/admin/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM admin WHERE id=%s"
    cursor.execute(query,(session["member_id"],))
    admininfo=cursor.fetchall()
    return render_template("admin/dashboard.html",info=info,title="Yönetici Paneli",admininfo=admininfo)


@app.route("/admin/addarticle",methods=["POST","GET"])
@login_required
def addarticle():
    form = AddArticleForm(request.form)
    if request.method=="POST" and form.validate():
        subject = form.subject.data
        image = form.image.data
        text = form.text.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO articles(subject,writenby,image,text) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,(subject,session["member_name"],image,text))
        mysql.connection.commit()
        query = "SELECT * FROM subscribers"
        cursor.execute(query)
        subscribers = cursor.fetchall()
        query = "SELECT * FROM articles ORDER BY id DESC "
        cursor.execute(query)
        articles = cursor.fetchall()
        lastarticleid = articles[0]["id"]
        mailtext = """
        {0} isimli kişisel bloğa {1} konulu yeni bir makale eklendi.Makaleyi okumak için <a href="{2}/read/{3}"> Tıkla </a><br>
        Abonelikten çıkmak için tıkla....
        """.format(info["sitename"],subject,info["link"],lastarticleid)
        for subs in subscribers:
            SendMail(subs["email"],"Yeni bir makale yayınlandı : {}".format(subject),mailtext)
        flash(message="Makale eklendi.",category="success")
        return redirect("/list/1")
    return render_template("admin/addarticle.html",info=info,title="Makale EKle",form=form)


@app.route("/admin/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/admin/messages")
@login_required
def messages():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM contactforms WHERE status=%s ORDER BY id DESC "
    cursor.execute(query,("Waiting",))
    messages = cursor.fetchall()
    return render_template("/admin/messages.html",info=info,title="Mesajlar",messages=messages)

@app.route("/admin/readmessage/<int:id>",methods=["GET","POST"])
@login_required
def readmessage(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM contactforms WHERE id=%s"
    cursor.execute(query,(id,))
    datas = cursor.fetchall()
    if len(datas)==0:
        redirect("/")
    form = AnswerMessageForm(request.form)

    if request.method == "POST" and form.validate():
        subject,text = form.subject.data,form.text.data
        try:

            SendMail(datas[0]["email"],subject,text)
            flash(message="E-posta yollandı.", category="success")
            query = "UPDATE contactforms SET status=%s"
            cursor.execute(query, ("Answered",))
            mysql.connection.commit()
        except:
            flash(message="E-posta yollanırken bir hata oluştu.",category="danger")
        return redirect(url_for("messages"))

    return render_template("/admin/readmessage.html",info=info,title="Mesaj oku",datas=datas,form=form)

@app.route("/admin/deletearticle/<int:id>",methods=["POST","GET"])
@login_required
def deletearticle(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE id=%s and status=%s"
    cursor.execute(query,(id,"Published"))
    article = cursor.fetchall()
    if request.method=="POST":
        query = "UPDATE articles SET status=%s WHERE id=%s"
        cursor.execute(query,("Unpublished",id))
        mysql.connection.commit()
        flash("Makale yayından kaldırıldı.",category="success")
        return redirect(url_for("index"))
    if len(article)==0:
        flash(message="Silmeye çalıştığınız makale yok yada yayında değil.",category="warning")
        return redirect(url_for("index"))
    return render_template("/admin/deletearticle.html",info=info,title="Makale siliniyor...",article=article)


@app.route("/admin/subscribers")
@login_required
def subs():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM subscribers"
    cursor.execute(query)
    subs = cursor.fetchall()
    return render_template("/admin/subscribers.html",subs=subs,title="Tüm Aboneler",info=info)


@app.route("/admin/addschool",methods=["POST","GET"])
@login_required
def addschool():
    form = AddSchoolForm(request.form)
    if request.method=="POST" and form.validate():
        school = form.school.data
        start = form.start.data
        finish = form.finish.data
        text = form.text.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO education(school,start,finish,text) VALUES (%s,%s,%s,%s) "
        cursor.execute(query,(school,start,finish,text))
        mysql.connection.commit()
        flash(message="Okul bilgisi eklendi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addschool.html",info=info,title="Okul Ekle",form=form)



@app.route("/admin/addtalent",methods=["POST","GET"])
@login_required
def addtalent():
    form = AddTalentForm(request.form)
    if request.method=="POST" and form.validate():
        name = form.name.data
        purcent = form.purcent.data
        text = form.text.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO talents(name,text,purcent) VALUES (%s,%s,%s) "
        cursor.execute(query,(name,text,purcent))
        mysql.connection.commit()
        flash(message="Yetenek bilgisi eklendi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addtalent.html",info=info,title="Yetenek Ekle",form=form)

@app.route("/admin/addwork",methods=["POST","GET"])
@login_required
def addwork():
    form = AddWordForm(request.form)
    if request.method=="POST" and form.validate():
        name = form.name.data
        start = form.start.data
        finish = form.finish.data
        text = form.text.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO workexperiences(name,start,finish,text) VALUES (%s,%s,%s,%s) "
        cursor.execute(query,(name,start,finish,text))
        mysql.connection.commit()
        flash(message="Çalışma bilgisi eklendi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addwork.html",info=info,title="İş Ekle",form=form)

@app.route("/admin/addclub",methods=["POST","GET"])
@login_required
def addclub():
    form = AddClubForm(request.form)
    if request.method=="POST" and form.validate():
        name = form.name.data
        text = form.text.data
        cursor = mysql.connection.cursor()
        query = "INSERT INTO clubmemberships(name,text) VALUES (%s,%s) "
        cursor.execute(query,(name,text))
        mysql.connection.commit()
        flash(message="Kulüp bilgisi eklendi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addclub.html",info=info,title="Kulüp Ekle",form=form)

@app.route("/admin/deleteschool/<int:id>",methods=["POST","GET"])
@login_required
def deleteschool(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM education WHERE id=%s"
    cursor.execute(query, (id,))
    datas = cursor.fetchall()
    if len(datas) == 0:
        flash(message="Böyle bir bilgi yok yada daha önce silinmiş.", category="warning")
        return redirect(url_for("about"))
    if request.method=="POST":
        query = "DELETE FROM education WHERE id=%s"
        cursor.execute(query,(id,))
        mysql.connection.commit()
        flash(message="Eğitim bilgisi silindi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/deleteschool.html",info=info,title="Eğitim bilgisi siliniyor...")

@app.route("/admin/deletework/<int:id>",methods=["POST","GET"])
@login_required
def deletework(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM workexperiences WHERE id=%s"
    cursor.execute(query, (id,))
    datas = cursor.fetchall()
    if len(datas) == 0:
        flash(message="Böyle bir bilgi yok yada daha önce silinmiş.", category="warning")
        return redirect(url_for("about"))
    if request.method=="POST":
        query = "DELETE FROM workexperiences WHERE id=%s"
        cursor.execute(query,(id,))
        mysql.connection.commit()
        flash(message="İş bilgisi silindi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/deletework.html",info=info,title="İş bilgisi siliniyor...")

@app.route("/admin/deletetalent/<int:id>",methods=["POST","GET"])
@login_required
def deletetalent(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM talents WHERE id=%s"
    cursor.execute(query, (id,))
    datas = cursor.fetchall()
    if len(datas) == 0:
        flash(message="Böyle bir bilgi yok yada daha önce silinmiş.", category="warning")
        return redirect(url_for("about"))
    if request.method=="POST":
        query = "DELETE FROM talents WHERE id=%s"
        cursor.execute(query,(id,))
        mysql.connection.commit()
        flash(message="Yetenek bilgisi silindi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/deletetalent.html",info=info,title="Yetenek bilgisi siliniyor...")

@app.route("/admin/deleteclub/<int:id>",methods=["POST","GET"])
@login_required
def deleteclub(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM clubmemberships WHERE id=%s"
    cursor.execute(query, (id,))
    datas = cursor.fetchall()
    if len(datas) == 0:
        flash(message="Böyle bir bilgi yok yada daha önce silinmiş.", category="warning")
        return redirect(url_for("about"))
    if request.method=="POST":
        query = "DELETE FROM clubmemberships WHERE id=%s"
        cursor.execute(query,(id,))
        mysql.connection.commit()
        flash(message="Kulüp bilgisi silindi.",category="success")
        return redirect(url_for("about"))
    return render_template("/admin/deleteclub.html",info=info,title="Kulüp bilgisi siliniyor...")

@app.route("/admin/editschool/<int:id>",methods=["POST","GET"])
@login_required
def editschool(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM education WHERE id=%s"
    cursor.execute(query,(id,))
    datas = cursor.fetchall()
    if len(datas)==0:
        flash(message="Böyle bir okul bilgisi bulunamadı.",category="warning")
        return redirect(url_for("about"))
    form = AddSchoolForm(request.form)

    if request.method=="GET":
        form.school.data = datas[0]["school"]
        form.start.data = datas[0]["start"]
        form.finish.data = datas[0]["finish"]
        form.text.data = datas[0]["text"]

    if request.method=="POST" and form.validate():
        query = "UPDATE education SET school=%s, start=%s, finish=%s, text=%s WHERE id=%s"
        cursor.execute(query,(form.school.data,form.start.data,form.finish.data,form.text.data,id))
        mysql.connection.commit()
        flash(message="Okul bilgisi güncellendi.", category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addschool.html",info=info,title="Okul bilgisi düzenleniyor...",form=form)

@app.route("/admin/edittalent/<int:id>",methods=["POST","GET"])
@login_required
def edittalent(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM talents WHERE id=%s"
    cursor.execute(query,(id,))
    datas = cursor.fetchall()
    if len(datas)==0:
        flash(message="Böyle bir yetenek bilgisi bulunamadı.",category="warning")
        return redirect(url_for("about"))
    form = AddTalentForm(request.form)
    if request.method=="GET":
        form.name.data = datas[0]["name"]
        form.purcent.data = datas[0]["purcent"]
        form.text.data = datas[0]["text"]

    if request.method=="POST" and form.validate():
        query = "UPDATE talents SET name=%s, purcent=%s, text=%s WHERE id=%s"
        cursor.execute(query,(form.name.data,form.purcent.data,form.text.data,id))
        mysql.connection.commit()
        flash(message="Yetenek bilgisi güncellendi.", category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addtalent.html",info=info,title="Yetenek bilgisi düzenleniyor...",form=form)

@app.route("/admin/editwork/<int:id>",methods=["POST","GET"])
@login_required
def editwork(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM workexperiences WHERE id=%s"
    cursor.execute(query,(id,))
    datas = cursor.fetchall()
    if len(datas)==0:
        flash(message="Böyle bir iş bilgisi bulunamadı.",category="warning")
        return redirect(url_for("about"))
    form = AddWordForm(request.form)
    if request.method=="GET":
        form.name.data = datas[0]["name"]
        form.start.data = datas[0]["start"]
        form.finish.data = datas[0]["finish"]
        form.text.data = datas[0]["text"]

    if request.method=="POST" and form.validate():
        query = "UPDATE workexperiences SET name=%s, start=%s, finish=%s, text=%s WHERE id=%s"
        cursor.execute(query,(form.name.data,form.start.data,form.finish.data,form.text.data,id))
        mysql.connection.commit()
        flash(message="İş bilgisi güncellendi.", category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addwork.html",info=info,title="İş bilgisi düzenleniyor...",form=form)


@app.route("/admin/editclub/<int:id>",methods=["POST","GET"])
@login_required
def editclub(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM clubmemberships WHERE id=%s"
    cursor.execute(query,(id,))
    datas = cursor.fetchall()
    if len(datas)==0:
        flash(message="Böyle bir kulüp bilgisi bulunamadı.",category="warning")
        return redirect(url_for("about"))
    form = AddClubForm(request.form)
    if request.method=="GET":
        form.name.data = datas[0]["name"]
        form.text.data = datas[0]["text"]

    if request.method=="POST" and form.validate():
        query = "UPDATE clubmemberships SET name=%s, text=%s WHERE id=%s"
        cursor.execute(query,(form.name.data,form.text.data,id))
        mysql.connection.commit()
        flash(message="Kulüp bilgisi güncellendi.", category="success")
        return redirect(url_for("about"))
    return render_template("/admin/addclub.html",info=info,title="Kulüp bilgisi düzenleniyor...",form=form)
############################



@app.route("/cv/<string:lang>")
def downloadCv(lang):
    if lang == "tr":
        cv = "OguzBalkaya_tr.pdf"
        return send_file(cv, as_attachment=True)
    elif lang == "en":
        cv = cv = "OguzBalkaya_tr.pdf"
        return send_file(cv, as_attachment=True)
    else:
        return redirect(url_for("index"))

@app.route("/unsubscribe/<string:shamail>", methods=["GET", "POST"])
def unsubscribe(shamail):
    # Farklır bir yöntem belirle.
    if (request.method == "GET"):
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM subscribers WHERE emailsha = %s"
        cursor.execute(query, (shamail,))
        datas = cursor.fetchall()
        if len(datas) > 0:
            query = "DELETE FROM subscribers WHERE emailsha = %s"
            cursor.execute(query, (shamail,))
            mysql.connection.commit()
            cursor.close()
            flash(message="Abonelikten ayrıldın.", category="warning")
            return redirect(url_for('index'))
        else:
            flash(message="Aboneliğin bulunmuyor.", category="warning")
            return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))


@app.errorhandler(404)
def not_found(e):
    return render_template('404.html', info=info, title="404 Not Found"), 404


@app.route("/read/<string:id>")
def read(id):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE id = %s"
    cursor.execute(query,(id,))
    article = cursor.fetchall()
    if len(article)==0:
        flash(message="Böyle bir makale bulunamadı.",category="warning")
        return redirect(url_for("index"))
    return render_template("read.html",article=article,title=article[0]['subject'],info=info)



    return render_template("read.html", id=id, info=info, title="Oku")


@app.route("/about")
def about():
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM talents"
    cursor.execute(query)
    talents = cursor.fetchall()
    query = "SELECT * FROM education ORDER BY id DESC"
    cursor.execute(query)
    education = cursor.fetchall()
    query = "SELECT * FROM workexperiences ORDER BY id DESC"
    cursor.execute(query)
    workexperiences = cursor.fetchall()
    query = "SELECT * FROM clubmemberships ORDER BY id DESC"
    cursor.execute(query)
    clubmemberships = cursor.fetchall()

    return render_template("about.html", info=info, title="Hakkımda", talents=talents, education=education,
                           workexperiences=workexperiences, clubmemberships=clubmemberships)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    form = ContactForm(request.form)
    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        message = form.message.data

        cursor = mysql.connection.cursor()
        query = "Insert into contactforms(name,email,message,date) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (name, email, message, datetime.now()))
        mysql.connection.commit()
        cursor.close()
        flash(message="Mesajını aldım.En kısa sürede dönüş yapacağım.", category="success")
        return redirect(url_for('contact'))
    else:
        return render_template("contact.html", info=info, title="Bana Ulaşın", form=form)



@app.route("/list/<int:page>")
def list(page):
    cursor = mysql.connection.cursor()
    query = "SELECT * FROM articles WHERE status=%s ORDER BY id DESC"
    cursor.execute(query,("Published",))
    articles=cursor.fetchall()
    lastpage=ceil(len(articles)/10)

    if page>lastpage or page<1:
        flash(message="Gitmeye çalıştığınız sayfa yok.",category="warning")
        return redirect(url_for("index"))

    if page==1:
        min,max = 0,10
    else:
        min = (page-1)*10
        max = min+10
    #if len(articles)<10:
    #    max=len(articles)
    statusnext,statusprevious="",""
    if lastpage==page:
        max=len(articles)
        statusnext="d-none"
    if page==1:
        statusprevious="d-none"

    return render_template("list.html",info=info,title="Makale Listesi",page=page,articles=articles,min=min,max=max,lastpage=lastpage,statusnext=statusnext,statusprevious=statusprevious,n=page+1,p=page-1)


@app.route("/", methods=["GET", "POST"])
def index():
    form = SubscribeForm(request.form)
    if request.method == "POST" and form.validate():
        email = form.email.data
        cursor = mysql.connection.cursor()
        query = "SELECT * FROM subscribers WHERE email = %s"
        cursor.execute(query, (email,))
        datas = cursor.fetchall()
        if len(datas) > 0:
            flash(message="Bloğuma daha önce zaten abone olmuşsun.", category="warning")
        else:
            query = "Insert into subscribers(email,emailsha) VALUES (%s,%s)"
            cursor.execute(query, (email, email))
            mysql.connection.commit()
            cursor.close()
            flash(message="Bloğuma abone oldun.Yeni yazılar eklendikçe seni e-posta ile bilgilendireceğim.",
                  category="success")

        return redirect(url_for('index'))
    else:
        return render_template("index.html", title="Ana Sayfa", info=info, form=form)


if __name__ == "__main__":
    app.run(debug=True)