#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
skupaj="Uporabnik je vpisal: /"
params = {}
a=0
b=0
oper ="+"
glavna_stevilka = 664



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
            tekst = "---Zmaga!!!---"
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
        #self.write(skupaj)
        params = {"vnos" : skupaj }
        return self.render_template("hello.html" , params=params)

class MathHandler(BaseHandler):
    def get(self):
        #params = {"vnos" : skupaj }
        return self.render_template("kalkulator.html")
    def post(self):
        a=self.request.get("prva")
        b=self.request.get("druga")
        operacija=self.request.get("oper")
        alfa = matematika(a,b,operacija)
        params={"rezultat":alfa}
        return self.render_template("kalkulator.html", params=params)

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



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/kalkulator', MathHandler),
    webapp2.Route('/random', RandomHandler),
    webapp2.Route('/pretvornik', PretvorHandler),
], debug=True)
