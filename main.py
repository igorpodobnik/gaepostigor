#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo,Forum
import time


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
skupaj="Uporabnik je vpisal: /"
params = {}
a=0
b=0
oper ="+"
glavna_stevilka = 664
sporocilo = "Obvezno vpisi kaj notri"
imeforum = "Neznanec"

class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))



def matematika(a,b,oper):
    if a.isdigit():
        a=int(a)
    else:
        a=0
    if b.isdigit():
        b=int(b)
    else:
        a=b
    if oper == "+":
        rez = a+b
    elif oper == "-":
        rez = a-b
    elif oper == "*":
        rez = a*b
    elif oper == "/":
        rez = (a+0.0)/(b+0.0)
    else:
        rez = "neveljavni operator!"
    return rez

def pretvorba(a,b,c):
    rez="Ni se zgodilo"
    if a.isdigit():
        a=int(a)
    else:
        rez = "Vnesi stevilko!!!"
    if b == "s":
        if c == "min":
            min = a / 60
            ostanek = a - (min *60)
            rez = str(min)+ " min in "+str(ostanek)+" sekund"
    elif b == "km":
        if c == "mi":
            vmestno = a*0.621
            rez = str(vmestno) + " milj"
    else:
        rez = "dej vnesi s/min ali pa km/mi"
    return rez

def randomm(stevilka):
    if stevilka.isdigit():
        stevilka=int(stevilka)
        if stevilka<glavna_stevilka:
            tekst = "Premajhna"
        elif stevilka>glavna_stevilka:
            tekst = "Prevelika"
        else:
            tekst = "--- Zmaga!!! ---"
    else:
        tekst="Vnesi stevilko"
    return tekst

class MainHandler(BaseHandler):
    def get(self):
        params = {"vnos" : skupaj }
        return self.render_template("hello.html" , params=params)

class RezultatHandler(BaseHandler):
    def post(self):
        dodatno = "Uporabnik je vpisal: "
        rezultat = self.request.get("vnos")
        skupaj = dodatno + rezultat  # zdruzimo zgornja dva stringa v enega
        params = {"vnos" : skupaj }
        sporocilo = Sporocilo(vnos=rezultat)
        sporocilo.put()
        return self.render_template("hello.html" , params=params)


class MathHandler(BaseHandler):
    def get(self):
        #params = {"vnos" : skupaj }
        return self.render_template("kalkulator_old.html")
    def post(self):
        a=self.request.get("prva")
        b=self.request.get("druga")
        operacija=self.request.get("oper")
        alfa = matematika(a,b,operacija)
        params={"rezultat":alfa}
        return self.render_template("kalkulator_old.html", params=params)

class PretvorHandler(BaseHandler):
    def get(self):
        return self.render_template("pretvornik.html")
    def post(self):
        d=self.request.get("stevilka")
        pe=self.request.get("prvaenota")
        de=self.request.get("drugaenota")
        gamma = pretvorba(d,pe,de)
        params={"koncnirezultat":gamma}
        return self.render_template("pretvornik.html", params=params)

class RandomHandler(BaseHandler):
    def get(self):
        return self.render_template("random.html")
    def post(self):
        c=self.request.get("ugibam")
        beta = "Vnesi stevilko"
        beta = randomm(c)
        params = {"visjemanjse":beta}
        return self.render_template("random.html", params=params)

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch()
        params = {"seznam" : seznam }
        return self.render_template("seznam.html" , params=params)

class ForumSporocilHandler(BaseHandler):
    def get(self):
        fseznam = Forum.query().fetch()
        params = {"forumseznam" : fseznam }
        return self.render_template("forum.html" , params=params)
    def post(self):
        imeforum = self.request.get("fime")
        print imeforum
        priimekforum = self.request.get("fpriimek")
        email = self.request.get("femail")
        sporocilo = self.request.get("fsporocilo")
        #params = {"fime" : imeforum }
        if sporocilo != "Obvezno vpisi kaj notri":
            forum = Forum(fime=imeforum, fpriimek=priimekforum, fsporocilo=sporocilo, femail=email)
            forum.put()
            time.sleep(1)
        fseznam = Forum.query().fetch()
        params = {"forumseznam" : fseznam }
        return self.render_template("forum.html" , params=params)


class PosameznoForumHandler(BaseHandler):
    def get(self, forum_id):
        sporocilo = Forum.get_by_id(int(forum_id))
        params = {"forum": sporocilo}
        self.render_template("posamezen-forum.html", params=params)



class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("posamezen.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/kalkulator', MathHandler),
    webapp2.Route('/random', RandomHandler),
    webapp2.Route('/pretvornik', PretvorHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler),
    webapp2.Route('/forum', ForumSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/forum/<forum_id:\d+>', PosameznoForumHandler),
], debug=True)

#TODO: prepreci dodatne vnose ko reloadasstran... sortiraj vnose po datumu