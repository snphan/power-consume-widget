#!/usr/bin/env python3
# Ubuntu 20.04: sudo apt-get install gir1.2-appindicator3-0.1
# From https://github.com/metalevel-tech/powerNow/blob/master/powerNow.py
import signal
import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, AppIndicator3, GObject, GLib
import time
from threading import Thread

def htop(self):
    return os.system("gnome-terminal -- bash -c 'if [[ -f /usr/bin/htop ]]; then htop; else echo sudo apt install htop ? && sudo apt install htop && htop; fi; exec bash'")

def sudohtop(self):
    return os.system("gnome-terminal -- bash -c 'if [[ -f /usr/bin/htop ]]; then sudo htop; else echo sudo apt install htop ? && sudo apt install htop && sudo htop; fi; exec bash'")

def sudopowertop(self):
    return os.system("gnome-terminal -- bash -c 'if [[ -f /usr/sbin/powertop ]]; then sudo powertop; else echo sudo apt install powertop ? && sudo apt install powertop && sudo powertop; fi; exec bash'")

def sudotlpstat(self):
    return os.system("gnome-terminal -- bash -c 'if [[ -f /usr/sbin/tlp ]]; then sudo tlp-stat | less; else echo sudo apt install tlp ? && sudo apt install tlp && sudo tlp-stat | less; fi; exec bash'")

def monitor_temperature(self):
    return os.system("gnome-terminal -- bash -c 'if [[ -f /usr/sbin/sensors-detect ]]; then sudo watch sensors; fi; exec bash'")

class Indicator():
    def __init__(self):
        self.app = 'Current Power Consumption'

        self.indicator = AppIndicator3.Indicator.new(
            self.app, "help-about",
            AppIndicator3.IndicatorCategory.OTHER)
        self.indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)       
        self.indicator.set_menu(self.create_menu())
        self.indicator.set_label("PowerNow", self.app)
        # the thread:
        self.update = Thread(target=self.show_seconds)
        # daemonize the thread to make the indicator stopable
        self.update.setDaemon(True)
        self.update.start()

    def create_menu(self):
        menu = Gtk.Menu()
        # menu item 1
        item_1 = Gtk.MenuItem('htop')
        item_1.connect('activate', htop)
        menu.append(item_1)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # menu item 2
        item_2 = Gtk.MenuItem('sudo htop')
        item_2.connect('activate', sudohtop)
        menu.append(item_2)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # menu item 3
        item_3 = Gtk.MenuItem('sudo powertop')
        item_3.connect('activate', sudopowertop)
        menu.append(item_3)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # menu item 4
        item_4 = Gtk.MenuItem('sudo tlp-stat')
        item_4.connect('activate', sudotlpstat)
        menu.append(item_4)
        # menu item 5
        item_5 = Gtk.MenuItem('Monitor Temperature')
        item_5.connect('activate', monitor_temperature)
        menu.append(item_5)
        # separator
        menu_sep = Gtk.SeparatorMenuItem()
        menu.append(menu_sep)
        # quit
        item_quit = Gtk.MenuItem('Quit')
        item_quit.connect('activate', self.stop)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def show_seconds(self):
        # power_path = '/sys/class/power_supply/BAT0/power_now'
        # voltage_path = '/sys/class/power_supply/BAT0/voltage_now'
        current_path = '/sys/class/power_supply/BAT0/current_now'
        total_bat_path = '/sys/class/power_supply/BAT0/charge_now'
            
        amps = ""
        while True:
            if os.path.exists(current_path):
                with open(current_path, 'r') as current_file:
                    current = int(int(current_file.readline())/1000)
                    amps = f"{current} mA | "
                with open(total_bat_path, 'r') as battery_charge_file:
                    current_battery = int(int(battery_charge_file.readline())/1000)
                    amps += f"{current_battery} mAh"

            else :
                amps = "PowerNow"
            # apply the interface update using  GObject.idle_add()
            GLib.idle_add(
                self.indicator.set_label,
                amps, self.app,
                priority=GLib.PRIORITY_DEFAULT
                )
            time.sleep(2)

    def stop(self, source):
        Gtk.main_quit()

Indicator()
# this is where we call GObject.threads_init()
signal.signal(signal.SIGINT, signal.SIG_DFL)
Gtk.main()
