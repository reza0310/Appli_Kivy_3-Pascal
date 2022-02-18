__author__ = "reza0310"

from kivy.app import App
from kivy.uix.widget import Widget
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.core.text import Label
from kivy.core.text.markup import MarkupLabel

layout = []

nbre = 10
hundred = 1000//nbre

class JEU():

    def initialiser(self):
        self.bonus = [0]*nbre**2
        for x in range(nbre):
            for y in range(nbre):
                hud.bind((x*hundred+hundred//2, y*hundred+hundred//2), (hundred, hundred), f"jeu.bonus[{x*nbre+y}] += 1")
        link = open("premiers.txt", "r")
        self.premiers = [int(x) for x in link.readline().split(" ")]
        self.clock = Clock.schedule_interval(self.actualiser, 1/FPS)  # 60 fps

    def actualiser(self, dt):
        self.valeurs = [0]*nbre**2
        for y in range(nbre-1, -1, -1):
            for x in range(nbre):
                val = self.valeurs[x*nbre+y]
                if x > 0 and y < nbre-1:
                    val += self.valeurs[(x-1)*nbre+y+1]
                if y < nbre-1:
                    val += self.valeurs[x*nbre+y+1]
                val += self.bonus[x*nbre+y]
                self.valeurs[x*nbre+y] = val
                categories = [0]
                if val % 2 == 0:
                    categories.append(1)
                if val in self.premiers:
                    categories.append(2)
                for i in range(len(categories)):
                    hud.show(x*hundred+(hundred//len(categories)*i), y*hundred, hundred//len(categories), hundred, f"{categories[i]}.jpg")
                hud.show(x*hundred, y*hundred, hundred, hundred, "cadre.png")
                hud.texte(x*hundred+hundred//2, y*hundred+hundred//4, "[color=#000000]"+str(val)+"[/color]") #f"x:{x} / y:{y}"



class HUD:

    def __init__(self):
        self.longueur, self.largeur = Window.size
        self.boutons = []

    def bind(self, emplacement, taille, action, type="Bouton"):
        print("Binding",action,'sur x variant de',(emplacement[0]-(taille[0]//2), emplacement[0]+(taille[0]//2)),'et y',(emplacement[1]-(taille[1]//2), emplacement[1]+(taille[1]//2)))
        self.boutons.append({"type": type, "x": (emplacement[0]-(taille[0]//2), emplacement[0]+(taille[0]//2)), "y": (emplacement[1]-(taille[1]//2), emplacement[1]+(taille[1]//2)), "action": action})

    def unbind(self, unbin="all"):
        if unbin == 'all':
            self.boutons = []
        else:
            for bouton in self.boutons:
                if bouton["action"] == unbin:
                    self.boutons.remove(bouton)

    def press(self, touch):
        for bouton in self.boutons:
            if bouton["x"][0] < touch.spos[0]*1000 < bouton["x"][1] and bouton["y"][0] < touch.spos[1]*1000 < bouton["y"][1]:
                print(bouton["action"])
                exec(bouton["action"])  # Handle joysticks

    def recoordonner(self, tupl):
        return int((tupl[0] / 1000) * self.longueur), int((tupl[1] / 1000) * self.largeur)

    def recoordonner_double(self, tupl):
        return int((tupl[0] / 1000) * self.longueur), int((tupl[1] / 1000) * self.largeur), int((tupl[2] / 1000) * self.longueur), int((tupl[3] / 1000) * self.largeur)

    def texte(self, x, y, texte, remove=True):
        label = MarkupLabel(markup=True, text=str(texte), font_size=20)
        label.refresh()
        text = label.texture
        rec = Rectangle(size=text.size, pos=self.recoordonner((x, y)), texture=text)
        layout.canvas.add(rec)
        if remove:
            def rmv(dt):
                layout.canvas.remove(rec)
            Clock.schedule_once(rmv, 1/30)

    def show(self, x, y, x2, y2, truc, remove=True):
        rec = Rectangle(size=self.recoordonner((x2, y2)), pos=self.recoordonner((x, y)), source=truc)
        layout.canvas.add(rec)
        if remove:
            def rmv(dt):
                layout.canvas.remove(rec)
            Clock.schedule_once(rmv, 1/30)


hud = HUD()
jeu = JEU()
FPS = 60


class Layout(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def add_entity(self, entity):
        self.entities.add(entity)
        self.canvas.add(entity.image)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)
            self.canvas.remove(entity.image)

    def on_touch_down(self, touch):
        hud.press(touch)


class ODAAMEApp(App):
    def build(self):
        global layout
        Window.clearcolor = (1, 1, 1, 1)
        self.title = 'O.D.A.A.M.E.'
        layout = Layout()
        jeu.initialiser()
        return layout


ODAAMEApp().run()