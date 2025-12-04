# Poznejte Karlov - Interaktivní Exponát

Aplikace pro dotykový kiosek běžící na Raspberry Pi 5. Seznamuje návštěvníky s osobností Karla Škody a historií čtvrti Karlov.

## 🛠 Technologie
* **Hardware:** Raspberry Pi 5 (16GB), Dotykový displej (HDMI/USB nebo DSI)
* **Jazyk:** Python 3.x
* **Framework:** Kivy (vybráno pro nativní podporu dotyku a GPU akceleraci)
* **Rozlišení:** Responzivní (škáluje se automaticky na FullHD i 4K)

## 📦 Instalace

1.  **Příprava systému (Raspberry Pi OS - Bookworm):**
    ```bash
    sudo apt update && sudo apt upgrade
    sudo apt install python3-pip python3-kivy xserver-xorg-input-evdev
    ```

2.  **Klonování repozitáře:**
    ```bash
    git clone [https://github.com/vase-jmeno/poznejte-karlov.git](https://github.com/vase-jmeno/poznejte-karlov.git)
    cd poznejte-karlov
    ```

3.  **Spuštění:**
    ```bash
    python3 main.py
    ```

## 🚀 Postup automatického spuštění (Autostart)

Na Raspberry Pi 5 (Wayland/Wayfire) je postup odlišný od starších verzí X11.

1.  Vytvořte soubor pro autostart v `~/.config/wayfire.ini` (nebo odpovídající konfiguraci desktopu):
    ```ini
    [autostart]
    kiosk_app = python3 /home/pi/poznejte-karlov/main.py
    ```

2.  **Alternativní metoda (Systemd Service - doporučeno pro stabilitu):**
    Vytvořte soubor `/etc/systemd/system/kiosk.service`:
    ```ini
    [Unit]
    Description=Kiosk Application
    After=graphical.target

    [Service]
    User=pi
    Environment=DISPLAY=:0
    ExecStart=/usr/bin/python3 /home/pi/poznejte-karlov/main.py
    Restart=always
    RestartSec=3

    [Install]
    WantedBy=graphical.target
    ```
    Aktivace: `sudo systemctl enable kiosk.service`

## 💡 Poznámky k implementaci

* **Dotyk vs. Myš:** Kivy používá vlastní input provider. Aplikace je nastavena tak, aby `on_release` reagoval na zvednutí prstu, což je standardní chování pro dotykové displeje.
* **Škálování:** Veškeré pozice a velikosti jsou definovány pomocí `size_hint` a `pos_hint` (relativní jednotky), nikoliv v pixelech.

## ⚠️ Řešení UI/UX chyb ze zadání
1.  **Zavírání bublin:** Místo malého křížku lze bublinu zavřít klepnutím kamkoliv mimo ni (implementováno přes `auto_dismiss=True`).
2.  **Klikatelné oblasti:** Zvětšili jsme aktivní plochy pro prokliky, aby nebylo nutné trefovat pouze slova v textu.