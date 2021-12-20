# ARCH-LINUX CONFIGURATION FILES

# 0. INSTALACIÓN
Con USB conectado y en terminal USB-LIVE

Dejamos la instalación mínima de ArchLinux
 - Kernel
 - SO
 - NetworkManager
 - SW básico + Drivers

## 0.1 Formatear y particionar discos
cfdisk
 - /dev/sda1 -> /boot -> 512M Sistema EFI (FAT32)
 - /dev/sda2 -> swap  -> 2G   Linux swap
 - /dev/sda3 -> /     -> 40G  Sistema de ficheros Linux (ext4)
 - /dev/sda4 -> /home -> XG   Sistema de ficheros Linux (ext4)

## 0.2 Dar formato a las particiones
 - 0.2.1 Sistema EFI

mkfs.vfat -F32 /dev/sda1

 - 0.2.2 Swap

mkswap /dev/sda2
swapon /dev/sda2

 -  0.2.3 Sistema de ficheros Linux

mkfs.ext4 /dev/sda3

mkfs.ext4 /dev/sda4

## 0.3 Montar las particiones en la carpeta temporal /mnt
mount /dev/sda3 /mnt

mkdir -p /boot/efi

mkdir /home

mount /dev/sda1 /mnt/boot/efi

mount /dev/sda4 /mnt/home

## 0.4 Realizar la instalación de los paquetes
 - 0.4.1 Archivos base

pacstrap base base-devel linux linux-firmware networkmanager

 - 0.4.2 Paquetes adicionales + drivers

pacstrap grub efibootmgr

pacstrap gvfs gvfs-afc gvfs-mtp xdg-user-dirs

pacstrap xf86-input-synaptics

pacstrap netctl wpa_supplicant dialog

pacstrap vim neovim

## 0.5 Generar el archivo fstab para que monte las unidades autmáticamente
genfstab -pU /mnt >> /mnt/etc/fstab

# 1. A PARTIR DE AQUÍ, TENEMOS UNA INSTALACIÓN BÁSICA DE ARCHLINUX
## 1.0 Entrar en el root del nuevo SO instalado
arch-chroot /mnt

## 1.1 Asignar hostname
echo "hostname" >> /etc/hostname

## 1.2 Asignar localtime
ln -sf /usr/share/zoneinfo/Europe/Madrid /etc/localtime

## 1.3 Asignar idioma al sistema
vim /etc/locale.gen -> Descomentar es_ES.UTF-8 (o el idioma que corresponda)

echo LANG=es_ES.UTF-8 >> /etc/locale.conf

locale-gen

## 1.4 Ajustar el reloj HW del sistema
hwclock -w

## 1.5 Ajustar el idioma del teclado
echo KEYMAP=es > /etc/vconsole.conf

## 1.6 Instalar y configurar GRUB
grub-install --efi-directory=/boot/efi --bootloader-id='Arch Linux' --target=x86_64-efi

grub-mkconfig -o /boot/grub/grub.cfg

## 1.7 Crear usuario con permisos de root
useradd -m "user"

usermod -aG wheel "user"

vim /etc/sudoers -> Permitir grupo #wheel y #sudo ejecutar como sudo

reboot -> Reiniciar para que coja los permisos de usuarios

## 1.8 Instalar Servidor gráfico y Drivers
sudo pacman -S xorg-server xorg-xinit

sudo pacman -S xf86-video-intel intel-ucode

## 1.9 Instalar Gestor ventanas y Gestor sesiones
 - Gestor ventanas "tiling"

sudo pacman -S qtile xterm -> Xterm es la terminal por defecto de Qtile, instalamos para que nos permita empezar

setxkbmap es -> Establece idioma/distribución teclado en castellano

 - Gestor sesiones (ligthdm no funciona)
sudo pacman -S lxdm  

## 1.10 Instalar herramientas de consola y editor de texto
 - Consola

sudo pacman -S alacritty

 - Editor de texto

sudo pacman -S code

 - Tema de color:

	Atom One Dark

	ayu

 - Tema de icono de archivo:

	Material Icon Dark

## 1.11 Instalar lanzador de aplicaciones
 - Instalar paquete

sudo pacman -S rofi

 - Temas de rofi

rofi-theme-selector

 - Configurar atajos de teclado

vim ~/.config/qtile/config.py

#Añadir atajos para rofi

 - Reiniciar Qtile

mod + ctrl + r

## 1.12 Instalar Gestor wallpaper
sudo pacman -S feh

feh --bg-scale "FILE"

## 1.13 Instalar Gestor audio
 - Gestor Audio

sudo pacman -S pulseaudio

 - Habilitar la tarjeta de sonido para que funcione

sudo pacman -S alsa-utils

alsamixer -> F6 y elegir la tarjeta de sonido a utilizar

asoundconf list -> Lista tarjetas de sonido disponibles

asound set-default-card PARAMETER -> Establece como predeterminada una de las tarjetas

sudo systemctl start alsa-restore.service

sudo systemctl enable alsa-restore.service

pulseaudio

 - Interfaz gráfica para Gestor audio

sudo pacman -S pavucontrol

#Añadir atajos de teclado para subir/bajar/mute volumen

## 1.14 Instalar Gestor brillo
sudo pacman -S brightnessctl

#Añadir atajos de teclado para subir/bajar brillo

## 1.15 Instalar Compositor de imagen
Sirve para personalizar el aspecto gráfico de las ventanas (transparencia, bordes, sombras, etc.)

sudo pacman -S picom

## 1.16 Instalar herramientas útiles
 - Logo ArchLinux en terminal

sudo pacman -S neofetch

 - Procesos, CPU, memoria, etc.

sudo pacman -S htop

sudo pacman -S bpytop

## 1.17 Instalar Gestor paquetes Repositorio de Usuarios ArchLinux (AUR) - YAY
sudo pacman -Sy

sudo pacman -F "PAQUETE" -> Buscar un paquete

sudo pacman -S binutils

rm -rf /tmp/yay 2> /dev/null && mkdir /tmp/yay && cd /tmp/yay

git clone https://aur.archlinux.org/yay.git && cd yay

makepkg -si

## 1.18 Activar colores en pacman y yay
sudo sed -i '/^#Color/s/^#//' /etc/pacman/conf

## 1.19 Instalar fuentes para Qtile
 - Nerd Fonts

yay -S nerd-fonts-ubuntu-fonts

Las activamos en ~/.config/qtile/config.py
widgets_defaults -> font='UbuntuMono Nerd Font'

Cada widget tiene su propia configuración -> Qtile docs / Built-in-widgets
http://docs.qtile.org/en/latest/manual/ref/widgets.html?highlight=widgets

La barra la cambiamos de "bottom" a "top"

 - Volume icon

sudo pacman -S volumeicon

 - Battery icon

sudo pacman -S cbatticon

En lugar de meterlos en .xsession, que se ejecutarían con todos los gestores de ventanas, lo hacemos solo para Qtile

Creamos ~/.config/qtile/autostart.sh -> Script que se ejecuta la primera vez que se arranca Qtile

## 1.20 Logs Qtile
~/.local/share/qtile/qtile.log

Para borrar el log (no es recomendable) -> echo "" > ~/.local/share/qtile/qtile.log

Para evitar errores en qtile.log:

sudo pacman -S python-pip

sudo pip install dbus-next

## 1.21 Montar USB

- Automontador USB

sudo pacman -S udisks2

- Icono systray

sudo pacman -S udiskie

- Para poder montar unidades de disco duro, necesita poder leer FS NTFS

sudo pacman -S ntfs-3g

- El programa udiskie intenta enviar notificaciones push al escritorio. Por defecto no puede, por lo que hay que hacer:
 
sudo pacman -S notification-daemon

En ~/-profile añadir:

export XDG_DATA_HOME=$HOME/.local/share

mkdir -p $XDG_DATA_HOME/dbus-1/services

echo '
[D-BUS Service]
Name=org.freedesktop.Notifications
Exec=/usr/lib/notification-daemon-1.0/notification-daemon
' > $XDG_DATA_HOME/dbus-1/services/org.freedesktop.Notifications.service

Añadimos "udiskie -t" a ~/-xsession para que lo lance al arrancar

## 1.22 Instalar fuentes para terminal y navegador
sudo pacman -S ttf-dejavu ttf-liberation noto-fonts

## 1.23 Pantallas

sudo pacman -S xorg-xrandr

 - Mostrar listado de resoluciones de monitores conectados

xrandr

eDP1, HDMI1, VGA1...

 - Configurar resoluciones de los monitores

xrandr --output eDP1 --mode 1366x768 --output HDMI1 --mode 2560x1220

 - Modificar tamaño de la pantalla

xrandr -size 1366x768

 - Gestor pantallas gráfico

sudo pacman -S arandr

## 1.24 Gestor basura
sudo pacman -S trash-cli

Crear alias en ~/.bashrc:

alias rm='trash-put $1'

Crear variable en ~/.profile:

export TRASH=$XDG_DATA_HOME/Trash/files

## 1.25 Visor imagenes
sudo pacman -S imv

## 1.26 Visor videos
sudo pacman -S vlc

## 1.27 Screenshot
sudo pacman -S scrot

## 1.28 Modificar GTK
sudo pacman -S lxappearance

 - Archivos de configuracion

/usr/share/gtk-2.0/gtkrc

/usr/share/gtk-3.0/gtkrc

/etc/gtkrc

## 1.29 Instalar Gestor archivos terminal y Gestor archivos gráfico
sudo pacman -S thunar

## 1.30 Instalar funciones archivar / comprimimir
sudo pacman -S zip

sudo pacman -S tar
