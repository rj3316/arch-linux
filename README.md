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

