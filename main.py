import os
# --- KONFIGURACE (MacBook) ---
from kivy.config import Config
Config.set('graphics', 'resizable', False)
Config.set('graphics', 'width', '1280')
Config.set('graphics', 'height', '720')
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
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
from kivy.animation import Animation

# --- TEXTY ---
TEXT_KAREL_SKODA = (
    "Byl synem zakladatele Škodových závodů, Emila Škody. Po smrti otce nebyl jmenován "
    "generálním ředitelem závodu, protože byl považován za slabého. V roce 1907 byl po "
    "řadě stávek dělníků jmenován do čela závodu, aby se pokusil situaci vyřešit.\n\n"
    "Karel byl výrazně sociálnější než jeho otec a snažil se pečovat i o dělníky. "
    "Nechal založit [b]konzumní družstvo[/b], kde dělníci závodu mohli získat levnější potraviny. "
    "Nechal založit [b]kulturní dům Nebe[/b] v Kollárově ulici, aby se dělníci měli kde scházet. "
    "Nejvýznamnější investice byla výstavba [b]čtvrtě Karlov[/b] pro 2500 dělníků. "
    "Ta byla realizována v letech 1910-1912 a bylo zde vystavěno na 200 domů.\n\n"
    "Za Karla Škody byly vystavěny mnohé stavby. Celá východní a jižní část areálu. "
    "Nechal závod obehnat náročně řešenou [b]zdí[/b] od architektů Ludwiga Tremmela a Bohumila Chvojky. "
    "Nechal také vystavět budovu současné [b]Techmanie[/b] a [b]planetária[/b]."
)

TEXT_KARLOV_INTRO = (
    "Karlov byla unikátní čtvrť pro zaměstnance Škodových závodů. Byla to čtvrť plná "
    "zeleně a života. V dobách největší slávy tu žilo 2300 lidí. Byla tu škola, hřiště, "
    "obchody a lidový dům. Karlov byl pojmenován na počest Karla Škody, který výstavbu "
    "čtvrtě inicializoval."
)

# --- TEXTY B1 ---
TEXT_B1_INTRO = (
    "Vznik Karlova byl problematický. Čtvrť pro své zaměstnance chtěla Škoda umístit na "
    "katastr obce Skvrňany. Ty s tím však nesouhlasili, a tak byl Karlov stavěn na západním "
    "kraji areálu Škodovky s vidinou toho, že se sem jednou rozroste město."
)
TEXT_B1A = "Karlov stavěla firma Müller a Kapsa z Plzně v letech 1910-1912. Plán čtvrtě byl koncipován jako moderní zahradní město s důrazem na hygienu a životní prostor."
TEXT_B1B = "Bylo postaveno 217 domů s 594 byty. Domy byly navrženy do otevřených řad s jednoduchou výzdobou a čtyřmi velikostmi bytů, což odráželo hierarchii zaměstnanců."
TEXT_B1C = "Letecký snímek Karlova ukazuje unikátní urbanistické řešení. (Kliknutím na obrázek v bublině můžete porovnat historický stav se současným pohledem)."

# --- TEXTY B2 ---
TEXT_B2_INTRO = (
    "Karlov byl svébytná čtvrť, která byla poměrně odříznutá od zbytku města. Lidé tu tak žili "
    "pospolu a naučili se zpříjemnit si život. Bylo tu slavné fotbalové družstvo, mnoho kroužků "
    "se zaměřením na sport, ale také divadelní spolky. Čtvrť měla školu, lidový dům, hřiště "
    "i dům dělnické tělovýchovné jednoty."
)
TEXT_B2A = "Školní budova na Karlově od architektů Josefa Farkače a Hanuše Zápala. Vznikla v roce 1914 a už v roce 1922 muselo být dostavěno patro."
TEXT_B2B = "Lidový dům byl postaven svépomocí a byl epicentrem kultury. Byly tu přednášky, kroužky, divadlo a soutěže."
TEXT_B2C = "Fotbal a sport se odehrával na místním hřišti. Součástí byla budova s restaurací, která je na Karlově dodnes."

# --- TEXTY B3 ---
TEXT_B3_INTRO = (
    "Karlov zanikl nadvakrát. Nejdříve byl zasažen třemi většími nálety v době druhé světové války. "
    "Nejvíce utrpěl při náletu v dubnu 1945. Podruhé zanikl kvůli neuskutečněnému plánu na "
    "výstavbu hal těžkého strojírenství v průběhu osmdesátých let 20. století."
)
TEXT_B3A = "Nálety za druhé světové války poničily nejen Škodovku, ale i přilehlý Karlov. Při náletu byly zničeny tři z deseti bloků Karlova a už nebyly obnoveny."
TEXT_B3B = "Na počátku sedmdesátých let 20. století bylo rozhodnuto o zástavbě Karlova halami těžkého strojírenství. Plán se realizoval pomalu a demolice proběhla v několika etapách."


# --- TŘÍDA PRO BLOK GALERIE ---
class GalleryBlock(BoxLayout):
    img_source = StringProperty('')
    text_content = StringProperty('')
    click_action = ObjectProperty(None) 

class MainMenu(Screen):
    pass

class SectionA(Screen):
    text_content = StringProperty(TEXT_KAREL_SKODA)
    def show_detail(self, title, image_path, description):
        popup = DetailPopup(title=title, img_source=image_path, desc_text=description)
        popup.open()

class SectionB(Screen):
    text_content = StringProperty(TEXT_KARLOV_INTRO)
    # VŠECHNY OBRÁZKY PRO SLIDESHOW
    slide_images = ListProperty([
        "assets/Karlov.jpg", "assets/A1.jpg", "assets/A2.jpg", "assets/A3.jpg", 
        "assets/A4.jpg", "assets/A5.jpg", "assets/A6.jpg", "assets/A7.jpg",
        "assets/Ba.jpg", "assets/Bb.jpg", "assets/Bc.jpg",
        "assets/B1a.jpg", "assets/B1b.jpg", "assets/B1c.jpg",
        "assets/B2a.jpg", "assets/B2b1.jpg", "assets/B2c2.jpg",
        "assets/B3a.jpg", "assets/Soucasnost.jpg"
    ])
    current_slide_index = 0

    def on_enter(self):
        if self.slide_images and os.path.exists(self.slide_images[0]):
             self.ids.slideshow_image.source = self.slide_images[0]
             self.ids.slideshow_image.opacity = 1
        self.event = Clock.schedule_interval(self.rotate_slide, 4.0)

    def rotate_slide(self, dt):
        if not self.slide_images: return
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slide_images)
        next_image_path = self.slide_images[self.current_slide_index]
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

# --- SEKCE B1 ---
class SectionB1(Screen):
    intro_text = StringProperty(TEXT_B1_INTRO)
    desc_b1a = StringProperty(TEXT_B1A)
    desc_b1b = StringProperty(TEXT_B1B)
    desc_b1c = StringProperty(TEXT_B1C)

    def show_timed_popup(self, title, img_1, img_2=None):
        # Už neposíláme description, protože ho v popupu nechceme
        popup = TimedDetailPopup(
            title=title, 
            img_source=img_1, 
            img_source_2=img_2 if img_2 else ''
        )
        popup.open()

# --- SEKCE B2 ---
class SectionB2(Screen):
    intro_text = StringProperty(TEXT_B2_INTRO)
    desc_b2a = StringProperty(TEXT_B2A)
    desc_b2b = StringProperty(TEXT_B2B)
    desc_b2c = StringProperty(TEXT_B2C)

    def show_timed_popup(self, title, img_1, img_2=None):
        popup = TimedDetailPopup(
            title=title, 
            img_source=img_1, 
            img_source_2=img_2 if img_2 else ''
        )
        popup.open()

# --- SEKCE B3 ---
class SectionB3(Screen):
    intro_text = StringProperty(TEXT_B3_INTRO)
    desc_b3a = StringProperty(TEXT_B3A)
    desc_b3b = StringProperty(TEXT_B3B)

    def show_timed_popup(self, title, img_1, img_2=None):
        popup = TimedDetailPopup(
            title=title, 
            img_source=img_1, 
            img_source_2=img_2 if img_2 else ''
        )
        popup.open()

# --- POPUPY ---
class DetailPopup(ModalView):
    title = StringProperty("")
    img_source = StringProperty("")
    desc_text = StringProperty("")

class TimedDetailPopup(ModalView):
    title = StringProperty("")
    img_source = StringProperty("")   
    # desc_text odstraněn, není potřeba
    
    img_source_main = StringProperty("") 
    img_source_2 = StringProperty("")   
    is_showing_main = BooleanProperty(True)
    
    timeout_event = None
    time_remaining = NumericProperty(10)

    def on_open(self):
        self.img_source_main = self.img_source
        self.timeout_event = Clock.schedule_interval(self.update_timer, 1.0)
    
    def update_timer(self, dt):
        self.time_remaining -= 1
        if self.time_remaining <= 0:
            self.dismiss()

    def reset_timer(self):
        self.time_remaining = 10

    def toggle_image(self):
        self.reset_timer()
        if self.is_showing_main:
            self.img_source = self.img_source_2
            self.is_showing_main = False
        else:
            self.img_source = self.img_source_main
            self.is_showing_main = True

    def on_dismiss(self):
        if self.timeout_event:
            self.timeout_event.cancel()

class KarlovApp(App):
    def build(self):
        if os.path.exists('design.kv'):
            Builder.load_file('design.kv')

        Window.show_cursor = True 
        sm = ScreenManager(transition=FadeTransition(duration=0.5))
        sm.add_widget(MainMenu(name='menu'))
        sm.add_widget(SectionA(name='section_a'))
        sm.add_widget(SectionB(name='section_b'))
        sm.add_widget(SectionB1(name='section_b1'))
        sm.add_widget(SectionB2(name='section_b2'))
        sm.add_widget(SectionB3(name='section_b3'))
        return sm

if __name__ == '__main__':
    KarlovApp().run()