#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo,Forum
import time
from matematicni import matematika, pretvorba, randomm
from google.appengine.api import users
#import jasona
import json
# import urlfetch da lahko z naslova jasone pobiramo
from google.appengine.api import urlfetch


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)




skupaj="Uporabnik je vpisal: /"
params = {}
sporocilo = "Obvezno vpisi kaj notri"
imeforum = "Neznanec"

def is_logged_in():
    user = users.get_current_user()
    if user:
        logiran = True
        logout_url = users.create_logout_url('/forum')
        print user.nickname()
        print user.user_id()
        print "glej gor"
        paramsif = {"logiran": logiran, "logout_url": logout_url, "user": user}
    else:
        logiran = False
        login_url = users.create_login_url('/forum')
        paramsif = {"logiran": logiran, "login_url": login_url, "user": user}
    return paramsif

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
        #tole spodaj mi preveri ce je user prijavljen
        paramsif = is_logged_in()
        #spodnje je vse pober
        #fseznam = Forum.query().fetch()
        #v query das notri pogoj
        fseznam = Forum.query(Forum.deleted == False).fetch()
        # SORT order takole zgleda... reverse za najvecjega navzdol
        fseznam = sorted(fseznam, key=lambda dat:dat.nastanek, reverse=True)
        params = {"forumseznam" : fseznam }
        #zdruzi dva dictionarija
        params.update(paramsif)
        return self.render_template("forum.html" , params=params)


class ForumPostSporocilHandler(BaseHandler):
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

        print fseznam
        print "gor glej"
        params = {"forumseznam" : fseznam }
        return self.render_template("forum.html" , params=params)


class redirectHandler(BaseHandler):
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
        print fseznam
        params = {"forumseznam" : fseznam }
        return self.render_template("redirect.html" , params=params)




class PosameznoForumHandler(BaseHandler):
    def get(self, forum_id):
        sporocilo = Forum.get_by_id(int(forum_id))
        paramsif = is_logged_in()
        params = {"forum": sporocilo}
        params.update(paramsif)
        self.render_template("posamezen-forum.html", params=params)



class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))
        params = {"sporocilo": sporocilo}
        self.render_template("posamezen.html", params=params)


class ForumEditHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Forum.get_by_id(int(sporocilo_id))
        params = {"forum": sporocilo}
        paramsif = is_logged_in()
        params.update(paramsif)
        #tale forum gre potem v html vse forum.neki itd.
        self.render_template("urediforum.html", params=params)
    def post(self, sporocilo_id):
        vnosi = self.request.get("ime")
        vnosp = self.request.get("priimek")
        vnose = self.request.get("email")
        vnoss = self.request.get("sporocilo")
        if not vnosi:
            vnosi="Neznanec"
        vmesnoime = Forum.get_by_id(int(sporocilo_id))
        vmesnoime.fime = vnosi
        vmesnoime.fpriimek = vnosp
        vmesnoime.femail = vnose
        vmesnoime.fsporocilo = vnoss
        vmesnoime.put()
        time.sleep(1)
        self.redirect_to("forum1")
        #TODO: dej tale redirect se malo prestudiraj


class ForumZbrisiHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Forum.get_by_id(int(sporocilo_id))
        params = {"forum": sporocilo}
        #tale forum gre potem v html vse forum.neki itd.
        paramsif = is_logged_in()
        params.update(paramsif)
        self.render_template("zbrisiforum.html", params=params)

    def post(self, sporocilo_id):
        izbris = Forum.get_by_id(int(sporocilo_id))
        #vmesnoime.key.delete()
        izbris.deleted=True
        izbris.put()
        time.sleep(1)
        self.redirect_to("forum1")

class JSONHandler(BaseHandler):
    def get(self):
        #prebiranje json fajla
        data = open("people.json", "r").read()
        json_data = json.loads(data)

        paramsif = is_logged_in()
        params = {"seznam": json_data}
        params.update(paramsif)

        self.render_template("json.html", params)

class WeatherHandler(BaseHandler):
    def get(self):
        #v urlju so parametri ki jih zelimo videti loceni z ikonco &
        # novo mesto 3194350 , 3239318 Ljubljana
        url = "http://api.openweathermap.org/data/2.5/group?id=3196359,3194351&units=metric&appid=29fb19f38dde3e3bfe9f2c2536b414b0"
        #zgornji je za vecmest, spodnji je za samo eno mesto
        #url = "http://api.openweathermap.org/data/2.5/weather?q=Ljubljana&units=metric&appid=29fb19f38dde3e3bfe9f2c2536b414b0"
        result = urlfetch.fetch(url)
        podatki = json.loads(result.content)
        params = {"podatki": podatki}
        paramsif = is_logged_in()
        params.update(paramsif)

        self.render_template("weather.html", params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/kalkulator', MathHandler),
    webapp2.Route('/random', RandomHandler),
    webapp2.Route('/pretvornik', PretvorHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler),
    webapp2.Route('/forum', ForumSporocilHandler, name = "forum1"),
    webapp2.Route('/redirect', redirectHandler),
    webapp2.Route('/forum/<sporocilo_id:\d+>/uredi', ForumEditHandler),
    webapp2.Route('/forum/<sporocilo_id:\d+>/zbrisi', ForumZbrisiHandler),
    webapp2.Route('/forumpost', ForumPostSporocilHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/forum/<forum_id:\d+>', PosameznoForumHandler),
    webapp2.Route('/json', JSONHandler),
    webapp2.Route('/weather', WeatherHandler),
], debug=True)

#TODO: