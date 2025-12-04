"""
Název projektu: Poznejte Karlov (Interaktivní Kiosk)
Autor: Tomáš Ungr
Datum: Prosinec 2024
Popis: Aplikace pro Raspberry Pi 5 prezentující historii čtvrti Karlov.
       Vytvořeno v frameworku Kivy.
"""

import os
import sys

# --- KONFIGURACE PRO PRODUKCI ---
from kivy.config import Config
Config.set('kivy', 'exit_on_escape', '0')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('kivy', 'log_level', 'error') # Logovat jen chyby pro výkon
Config.write()
# -----------------------------

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty, ObjectProperty
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.animation import Animation

# Importy pro fonty a preloading
from kivy.core.text import LabelBase
from kivy.core.image import Image as CoreImage

# --- DEFINICE CEST ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    """ Pomocná funkce pro získání cesty k souborům """
    return os.path.join(BASE_DIR, relative_path)

# ==========================================
# TEXTY (Zkráceno pro přehlednost - jsou stejné jako minule)
# ==========================================
TEXT_KAREL_SKODA = "Byl synem zakladatele Škodových závodů, Emila Škody. Po smrti otce nebyl jmenován generálním ředitelem závodu, protože byl považován za slabého. V roce 1907 byl po řadě stávek dělníků jmenován do čela závodu, aby se pokusil situaci vyřešit.\n\nKarel byl výrazně sociálnější než jeho otec a snažil se pečovat i o dělníky. Nechal založit [b]konzumní družstvo[/b], kde dělníci závodu mohli získat levnější potraviny. Nechal založit [b]kulturní dům Nebe[/b] v Kollárově ulici, aby se dělníci měli kde scházet. Nejvýznamnější investice byla výstavba [b]čtvrtě Karlov[/b] pro 2500 dělníků. Ta byla realizována v letech 1910-1912 a bylo zde vystavěno na 200 domů.\n\nZa Karla Škody byly vystavěny mnohé stavby. Celá východní a jižní část areálu. Nechal závod obehnat náročně řešenou [b]zdí[/b] od architektů Ludwiga Tremmela a Bohumila Chvojky. Nechal také vystavět budovu současné [b]Techmanie[/b] a [b]planetária[/b]."
TEXT_KARLOV_INTRO = "Karlov byla unikátní čtvrť pro zaměstnance Škodových závodů. Byla to čtvrť plná zeleně a života. V dobách největší slávy tu žilo 2300 lidí. Byla tu škola, hřiště, obchody a lidový dům. Karlov byl pojmenován na počest Karla Škody, který výstavbu čtvrtě inicializoval."
TEXT_B1_INTRO = "Vznik Karlova byl problematický. Čtvrť pro své zaměstnance chtěla Škoda umístit na katastr obce Skvrňany. Ty s tím však nesouhlasili, a tak byl Karlov stavěn na západním kraji areálu Škodovky s vidinou toho, že se sem jednou rozroste město."
TEXT_B1A = "Karlov stavěla firma Müller a Kapsa z Plzně v letech 1910-1912. Plán čtvrtě byl koncipován jako moderní zahradní město s důrazem na hygienu a životní prostor."
TEXT_B1B = "Bylo postaveno 217 domů s 594 byty. Domy byly navrženy do otevřených řad s jednoduchou výzdobou a čtyřmi velikostmi bytů, což odráželo hierarchii zaměstnanců."
TEXT_B1C = "Letecký snímek Karlova ukazuje unikátní urbanistické řešení. (Kliknutím na obrázek v bublině můžete porovnat historický stav se současným pohledem)."
TEXT_B2_INTRO = "Karlov byl svébytná čtvrť, která byla poměrně odříznutá od zbytku města. Lidé tu tak žili pospolu a naučili se zpříjemnit si život. Bylo tu slavné fotbalové družstvo, mnoho kroužků se zaměřením na sport, ale také divadelní spolky. Čtvrť měla školu, lidový dům, hřiště i dům dělnické tělovýchovné jednoty."
TEXT_B2A = "Školní budova na Karlově od architektů Josefa Farkače a Hanuše Zápala. Vznikla v roce 1914 a už v roce 1922 muselo být dostavěno patro."
TEXT_B2B = "Lidový dům byl postaven svépomocí a byl epicentrem kultury. Byly tu přednášky, kroužky, divadlo a soutěže."
TEXT_B2C = "Fotbal a sport se odehrával na místním hřišti. Součástí byla budova s restaurací, která je na Karlově dodnes."
TEXT_B3_INTRO = "Karlov zanikl nadvakrát. Nejdříve byl zasažen třemi většími nálety v době druhé světové války. Nejvíce utrpěl při náletu v dubnu 1945. Podruhé zanikl kvůli neuskutečněnému plánu na výstavbu hal těžkého strojírenství v průběhu osmdesátých let 20. století."
TEXT_B3A = "Nálety za druhé světové války poničily nejen Škodovku, ale i přilehlý Karlov. Při náletu byly zničeny tři z deseti bloků Karlova a už nebyly obnoveny."
TEXT_B3B = "Na počátku sedmdesátých let 20. století bylo rozhodnuto o zástavbě Karlova halami těžkého strojírenství. Plán se realizoval pomalu a demolice proběhla v několika etapách."

# ==========================================
# POMOCNÉ TŘÍDY
# ==========================================

class GalleryBlock(BoxLayout):
    img_source = StringProperty('')
    text_content = StringProperty('')
    click_action = ObjectProperty(None) 

class AutoCloseBehavior:
    timer_event = None
    
    def on_open(self):
        self.reset_timer()
        if hasattr(super(), 'on_open'): super().on_open()

    def reset_timer(self):
        if self.timer_event: self.timer_event.cancel()
        self.timer_event = Clock.schedule_once(self.dismiss, 10)

    def on_dismiss(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
        if hasattr(super(), 'on_dismiss'): super().on_dismiss()
    
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos): self.reset_timer()
        return super().on_touch_down(touch)

# ==========================================
# OBRAZOVKY
# ==========================================

class MainMenu(Screen): pass

class SectionA(Screen):
    text_content = StringProperty(TEXT_KAREL_SKODA)
    def show_detail(self, title, image_path, description):
        popup = DetailPopup(title=title, img_source=resource_path(image_path), desc_text=description)
        popup.open()

class SectionB(Screen):
    text_content = StringProperty(TEXT_KARLOV_INTRO)
    # Všechny obrázky pro slideshow
    slide_images = ListProperty([
        "assets/A1.jpg", "assets/A2.jpg", "assets/A3.jpg", 
        "assets/A4.jpg", "assets/A5.jpg", "assets/A6.jpg", "assets/A7.jpg",
        "assets/Ba.jpg", "assets/Bb.jpg", "assets/Bc.jpg",
        "assets/B1a.jpg", "assets/B1b.jpg", "assets/B1c.jpg",
        "assets/B2a.jpg", "assets/B2b1.jpg", "assets/B2c2.jpg",
        "assets/B3a.jpg", "assets/Soucasnost.jpg"
    ])
    current_slide_index = NumericProperty(0)

    def on_enter(self):
        if not self.slide_images: return
        if self.current_slide_index >= len(self.slide_images): self.current_slide_index = 0
        
        # Načteme s resource_path
        current_img_path = resource_path(self.slide_images[self.current_slide_index])
        if os.path.exists(current_img_path):
             self.ids.slideshow_image.source = current_img_path
             self.ids.slideshow_image.opacity = 1
        self.event = Clock.schedule_interval(self.rotate_slide, 4.0)

    def rotate_slide(self, dt):
        if not self.slide_images: return
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slide_images)
        next_image_path = resource_path(self.slide_images[self.current_slide_index])
        
        if not os.path.exists(next_image_path): return

        img_widget = self.ids.slideshow_image
        anim_out = Animation(opacity=0, duration=0.5, t='out_quad')
        def on_fade_out_complete(animation, widget):
            widget.source = next_image_path
            anim_in = Animation(opacity=1, duration=0.5, t='in_quad')
            anim_in.start(widget)
        anim_out.bind(on_complete=on_fade_out_complete)
        anim_out.start(img_widget)

    def on_leave(self):
        if hasattr(self, 'event'): self.event.cancel()

class SectionB1(Screen):
    intro_text = StringProperty(TEXT_B1_INTRO)
    desc_b1a = StringProperty(TEXT_B1A)
    desc_b1b = StringProperty(TEXT_B1B)
    desc_b1c = StringProperty(TEXT_B1C)
    def show_timed_popup(self, title, img_1, img_2=None):
        popup = TimedDetailPopup(title=title, img_source=resource_path(img_1), img_source_2=resource_path(img_2) if img_2 else '')
        popup.open()

class SectionB2(Screen):
    intro_text = StringProperty(TEXT_B2_INTRO)
    desc_b2a = StringProperty(TEXT_B2A)
    desc_b2b = StringProperty(TEXT_B2B)
    desc_b2c = StringProperty(TEXT_B2C)
    def show_timed_popup(self, title, img_1, img_2=None):
        popup = TimedDetailPopup(title=title, img_source=resource_path(img_1), img_source_2=resource_path(img_2) if img_2 else '')
        popup.open()

class SectionB3(Screen):
    intro_text = StringProperty(TEXT_B3_INTRO)
    desc_b3a = StringProperty(TEXT_B3A)
    desc_b3b = StringProperty(TEXT_B3B)
    def show_timed_popup(self, title, img_1, img_2=None):
        popup = TimedDetailPopup(title=title, img_source=resource_path(img_1), img_source_2=resource_path(img_2) if img_2 else '')
        popup.open()

# ==========================================
# POPUPY
# ==========================================

class DetailPopup(AutoCloseBehavior, ModalView):
    title = StringProperty("")
    img_source = StringProperty("")
    desc_text = StringProperty("")

class TimedDetailPopup(AutoCloseBehavior, ModalView):
    title = StringProperty("")
    img_source = StringProperty("")   
    img_source_main = StringProperty("") 
    img_source_2 = StringProperty("")   
    is_showing_main = BooleanProperty(True)
    
    def on_open(self):
        super().on_open()
        self.img_source_main = self.img_source
        self.is_showing_main = True

    def toggle_image(self):
        self.reset_timer()
        if self.is_showing_main:
            self.img_source = self.img_source_2
            self.is_showing_main = False
        else:
            self.img_source = self.img_source_main
            self.is_showing_main = True
            
    def on_dismiss(self):
        super().on_dismiss()
        if self.img_source_main:
             self.img_source = self.img_source_main
             self.is_showing_main = True

# ==========================================
# HLAVNÍ APLIKACE
# ==========================================

class KarlovApp(App):
    inactivity_event = None
    INACTIVITY_TIMEOUT = 120  # 2 minuty

    def build(self):
        # 1. REGISTRACE FONTŮ
        # Zde říkáme Kivy: "Když někdo chce font 'Roboto', použij tyto soubory."
        # Pokud nastavíš bold: True, Kivy automaticky sáhne po fn_bold.
        LabelBase.register(name='Roboto', 
                           fn_regular=resource_path('assets/fonts/Roboto-Regular.ttf'),
                           fn_bold=resource_path('assets/fonts/Roboto-Bold.ttf'))

        # 2. PRELOADING OBRÁZKŮ
        # Načteme obrázky do cache, aby se neškubaly při prvním zobrazení
        self.preload_images()

        kv_path = resource_path('design.kv')
        if os.path.exists(kv_path):
            Builder.load_file(kv_path)
        
        Window.show_cursor = False 
        
        self.sm = ScreenManager(transition=FadeTransition(duration=0.5))
        self.sm.add_widget(MainMenu(name='menu'))
        self.sm.add_widget(SectionA(name='section_a'))
        self.sm.add_widget(SectionB(name='section_b'))
        self.sm.add_widget(SectionB1(name='section_b1'))
        self.sm.add_widget(SectionB2(name='section_b2'))
        self.sm.add_widget(SectionB3(name='section_b3'))
        
        Window.bind(on_motion=self.on_user_activity)
        self.reset_inactivity_timer()
        return self.sm

    def preload_images(self):
        """Načte klíčové obrázky do paměti při startu"""
        images_to_load = [
            "assets/A1.jpg", "assets/Soucasnost.jpg",
            # + další z slideshow, pokud je to nutné, ale hlavní je ten první
        ]
        # Přidáme obrázky z slideshow sekce B
        screen_b = SectionB()
        images_to_load.extend(screen_b.slide_images)
        
        # Odstraníme duplicity
        images_to_load = list(set(images_to_load))

        print("Načítám obrázky do cache...")
        for img_rel_path in images_to_load:
            full_path = resource_path(img_rel_path)
            if os.path.exists(full_path):
                # CoreImage načte texturu do paměti
                CoreImage(full_path)

    def on_user_activity(self, window, etype, motionevent):
        self.reset_inactivity_timer()

    def reset_inactivity_timer(self):
        if self.inactivity_event: self.inactivity_event.cancel()
        self.inactivity_event = Clock.schedule_once(self.go_to_home_screen, self.INACTIVITY_TIMEOUT)

    def go_to_home_screen(self, dt):
        if self.sm.current != 'menu':
            for widget in Window.children[:]:
                if isinstance(widget, ModalView): widget.dismiss()
            self.sm.current = 'menu'

if __name__ == '__main__':
    KarlovApp().run()