#!/usr/bin/env python
import os
import jinja2
import webapp2


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)
skupaj="Uporabnik je vpisal: /"
params = {}

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
    if oper == "+":
        rez = a+b
    elif oper == "-":
        rez = a-b
    elif oper == "*":
        rez = a*b
    elif oper == "/":
        rez = (a+0.0)/(b+0.0)
    else:
        rez = 0
    return rez


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
        a=int(self.request.get("prva"))
        b=int(self.request.get("druga"))
        operacija=self.request.get("oper")
        alfa = matematika(a,b,operacija)

        params={"rezultat":alfa}
        return self.render_template("kalkulator.html", params=params)



app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/kalkulator', MathHandler),
], debug=True)
