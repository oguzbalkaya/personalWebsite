from wtforms import Form,StringField,TextAreaField,PasswordField,validators,IntegerField #form araçları
class ContactForm(Form):
    name = StringField("Adın ve Soyadın",validators=[validators.DataRequired("Adını ve soyadınızı yazmalısınız.")])
    email = StringField("E-posta adresin",validators=[validators.Email("Geçerli bir e-posta adresi girmelisiniz."),validators.DataRequired("Lütfen e-posta adresini gir.")])
    message = TextAreaField("İletmek istediklerin",validators=[validators.DataRequired("İletmek için birşeyler yazmalısınız.")])

class SubscribeForm(Form):
    email = StringField("",validators=[validators.DataRequired("E-Posta adresini girmelisin."),validators.Email("Geçerli bir e-posta adresi girmelisin.")])

class AdminLoginForm(Form):
    username = StringField("Kullanıcı adı",validators=[validators.DataRequired("Lütfen kullanıcı adınızı girin.")])
    password = PasswordField("Parola",validators=[validators.DataRequired("Lütfen parolanızı girin.")])

class AddArticleForm(Form):
    subject = StringField("Makale konusunu girin",validators=[validators.DataRequired("Lütfen konuyu girin")])
    image = StringField("Makale listesinde gözükecek resmin linkini girin.(Boş bırakırsanız resimsiz listelenir.)")
    text = TextAreaField("Makale")

class AnswerMessageForm(Form):
    subject = StringField("E-posta konusu",validators=[validators.DataRequired("Lütfen konuyu girin.")])
    text = TextAreaField("Mesajınızı girin",validators=[validators.DataRequired("LÜtfen mesajınızı girin.")])

class AddSchoolForm(Form):
    school = StringField("Okul adını girin",validators=[validators.DataRequired("Lütfen okul adını girin.")])
    start = StringField("Başlama tarihini girin",validators=[validators.DataRequired("Lütfen okula başlama tarihini girin.")])
    finish = StringField("Bitiş tarihini girin",validators=[validators.DataRequired("Lütfen okul bitiş tarihini girin.")])
    text = TextAreaField("Okul hakkında detay(Bölüm bilgisi vb gibi bilgiler girilebilir)")

class AddClubForm(Form):
    name = StringField("Kulüp adını girin",validators=[validators.DataRequired("Lütfen kulüp adını girin.")])
    text = TextAreaField("Kulüp hakkında detaylar, kulüpte alınan görevler vb.")

class AddTalentForm(Form):
    name = StringField("Yetenek adını girin",validators=[validators.DataRequired("Lütfen yetenek adını girin.")])
    purcent = IntegerField("Yeteneğinizdeki uzmanlığınızı 1-100 arasında değerlendirin",validators=[validators.DataRequired("Lütfen yeteneği değerlendirin."),validators.NumberRange(min=1,max=100)])
    text = TextAreaField("Okul hakkında detay(Bölüm bilgisi vb gibi bilgiler girilebilir)")

class AddWordForm(Form):
    name = StringField("İş adını girin",validators=[validators.DataRequired("Lütfen iş adını girin.")])
    start = StringField("Başlama tarihini girin",validators=[validators.DataRequired("Lütfen işe başlama tarihini girin.")])
    finish = StringField("Bitiş tarihini girin",validators=[validators.DataRequired("Lütfen iş bitiş tarihini girin.")])
    text = TextAreaField("İş hakkında detay(Çalışılan pozisyon vb gibi bilgiler girilebilir)")
