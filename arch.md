# Summary du guide du parnanoyaque (BTW i use arch)
___

## 0. Bootloaders UEFI

### Introduction

blablabla

### overviews

Even the person you most despise is able to
to launch a shell on your bootlooder using a very
a very sophisticated technique (that's not true) "init=/bin/bash" as kernel boot parameter. It is therefore very important to avoid this kind of stupid access to a physical opponent. 
Encrypt your /boot or set a password to your bootloader. 


But, chiffre votre /boot ne vous protege pas des attaques sur les bootloader (keylogger/bootkit/ ect)
De plus il est possible d'identifier l'os que vous utiliser (hash du bootloader (version et distribution) ou simplement si vous utilise GRUB il a fort a parier que vous utilise un linux)

Theoriquement si votre bootloader est compromis, donc en amont de votre dechifrement vous ne pouvez rien faire contre cela. Nous allons donc parler des deux methode (Il en existe surement d'autre que ne connais pas !)



### Boot process UEFI
Explciation du fonctionement pour introduire les attaques

![EDK2 Bootsequence](edk2_bootsequence.png)

#### Security (SEC)

La SEC phaze contient la premiere partie du code execute par le CPU
Le code est executer directement dans  la SPI-Flash il utilise le CPU cache (donc memoire temporaire) pour la memoire, ce code va chercher le loader PEI  

#### Pre-EFI Initialization (PEI)

Initialisation du chipset, configuration du controleur memoire, 

(pas compris) -> initialisation du handle S3 resume process

Jusquaceque le memory controller soit initialise tout le code runer en memoire temporaire.
Par la suite il est executer en memoire permanantes.

#### Driver Execution Environement (DXE)

Initializes System Management Mode (SMM) et les DXE Services (Drivers, dispatcher, ...) sont chargee

#### Boot Device Selection (BDS)

Enumere les disque physique par les bus PCI qui peuvent contenir un bootloader EFI compatible.

#### Transient System Load (TSL) and Runtime (RT)

The Transient System Load (TSL) is primarily the OS vendor provided boot loader. Both the TSL and the Runtime Services (RT) phases may allow access to persistent content, via UEFI drivers and UEFI applications. Drivers in this category include PCI Option ROMs.


#### After Life (AL)

The After Life (AL) phase consists of persistent UEFI drivers used for storing the state of the system during the OS orderly shutdown, sleep, hibernate or restart processes.


#### Trouver un titre : 

Tout les composant utilisee dans le boot process sont se trouve dans la SPI Flash, 
A l'exception de OS loader qui lui est sur le filesytem du disque.
Il est trouver par la phaze DXE/BDS grace au path stoquer dans la NVRAM UEFI.

### OS Loader

TODO : 
Installer un linux efi loader
Decrire le fonctionnement
Trouver la structure EFI Entry
-> deux pointeur faire le shemas
Trouver les service load (EFI service) de la hall.dll
Reading the boot configuration data
Shemas transferring control vers l equivalent du winloader
Definition des etape du loader
View IDA de la fonction OSLPMAIN equivalent linux
Description de la vue
conclusion UEFI


### Bootkit UEFI

Les point les plus interessant pour des bootkit sont le SMM et le DXE initialisation.


- Ce passer de bootloader (toto power)

## 0.1 Secure boot

### Kesako ?



## 0.1 GRUB

- Password
- Encrypt /boot
- Yubikey ??

## 0.2 Syslinux

## 0.3 systemd-boot

## 1. Kernel

- Sysctl
- Boot Parameters
- Hide PID
- Linux-hardened

## 2. Mandatory Access Control (MAC)
- SELinux et Apparmor (SELinux > aopparmor mais pas suporter par arch)

SELinux regarde pour le coter utilisation
Apparmor existe en fait sous arch et plus simple a utiliser
A creuser , tester les deux et voir aa-utils pour apparmor

## 3. Sandboxes

A voir les quel sont les mieux
- bubblewrap 

### 3.1 Sandboxing Xorg
- Le temps avance et les moeurs aussi -> Voir wayland

## 4. The Root Account

### 4.1 /etc/securetty
/etc/securetty -> vide pas de conection root depuis un tty

### 4.2 Restricting su

Weel `The term was derived from the slang phrase big wheel, referring to a person with great power or influence. wikipedia `

Par default su (switch user i gest) tente une connexion au compte root. Nous ne voulons aucun changement de compte si vous ne faite pas partie du group weel. 

Limiter su au group wheel
`auth required pam_wheel.so use_uid`

### 4.3 Locking the root account (optionel)
`passwd -l root`

### 4.4 Denying Root Login via SSH

edit /etc/ssh/sshd_config `PermitRootLogin no`


### 4.5 Increase the Number of Hashing Rounds
"You can increase the number of hashing rounds that shadow can use. This can increase the security of your hashed passwords. It makes an attacker have to compute a lot more hashes to crack your password. By default shadow uses 5000 rounds but you can increase this to as many as you want. The more rounds it does the slower it wil be to login. Edit /etc/pam.d/passwd and add the rounds option"
`password required pam_unix.so sha512 shadow nullok rounds=65536`

This makes shadow perform 65536 rounds.

Your passwords are not automatically rehashed after applying this setting so you need to reset the password with

`passwd username`
Replace 'username' with the user whose password you are changing.

This can be applied to your user account or the root account.

Source : https://wiki.archlinux.org/title/SHA_password_hashes

## 5. Systemd Sandboxing

Systemd has the ability to sandbox services so they can only access what they need.
A creuser


## 6. Hostnames and Usernames

Do not put anything uniquely indentifying in your hostname or username. It is recommended to keep them as generic names such as "host" and "user" so you can't be identified by them.

## 7. RADIO

### 7.1 Wireless Devices (Optional)
`rfkill block all`
- Pensez a faire un bouton on off

### 7.2 Bluethoo (Optional)

You can also blacklist certain modules to prevent them from loading. For example, to blacklist the bluetooth module, create /etc/modprobe.d/blacklist-bluetooth.conf and add

`install btusb /bin/true
install bluetooth /bin/true`

You should always use install (module) /bin/true instead of blacklist (module) as modules blacklisted via blacklist can still be loaded if another module depends on it.

## Umask

Umasks set the default file permissions for newly created files. [40] The default is 022 which is not very secure. This gives read access to every user on the system for newly created files. Edit /etc/profile and change the umask to 0077 which makes new files not readable by anyone other than the owner.

___
# NETWORK


## 8. Firewalls

### ICMP Timestamps
Jerry is an unpleasant person, if you ask him the time he won't
he won't stop to answer you.
Be like Jerry, don't give out your fingerprints.
The easiest way is to block all
ICMP connections at the firewall level

## 9. Tor

### 9.1 Tor browser

You should use apparmor with the Tor Browser to increase security.

### 9.2 Torsocks

Stream isolation makes programs use different Tor circuits from each other to prevent identity correlation. [34] To enable this edit /etc/tor/torrc and configure more SocksPorts. 9050 is the default SocksPort. Once you have made more, configure your programs to use those new ports and you will have stream isolation.

Pacman can use stream isolation by editing /etc/pacman.conf. Add this to /etc/pacman.conf

`XferCommand = /usr/bin/curl --socks5-hostname localhost:9062 --continue-at - --fail --output %o %u`
Replace 9062 with your SocksPort.

### 9.4 Transparent Proxy

You can configure your whole system to use Tor by default with a transparent proxy to anonymize all internet traffic.

### 9.5 Configuring the Tor Browser to prevent Tor over Tor

https://www.whonix.org/wiki/Other_Operating_Systems#Configure_Tor_Browser_Settings

## 10. NTP

NTP sucks because it is neither authenticated nor encrypted. This means that nobody likes NTP. A man-in-the-middle attack on your connection to give you a false time will be fingerprinted, because an attacker can give you a unique time and thus track you down. It also means that you are vulnerable to (replay attack [source:https://en.wikipedia.org/wiki/Replay_attack])

NTP leaks your local computer time in NTP timestamp format which can be used for clock skew fingerprinting. This can be used to de-anonymize users and onion services.
Source : https://murdoch.is/papers/ccs06hotornot.pdf (tltr but its suck for you)

There is authentication for NTP called autokey but this is insecure and doesn't solve the problem of clock skew fingerprinting. (<- a etudiez)

Vous pouvez désactiver cette fonction et utiliser votre système local et votre horloge matérielle, bien que cela vous rende plus vulnérable à la prise d'empreintes de l'horloge. Vous pouvez également vous regarder à sdwdate de Whonix.

Uninstall any NTP clients and disable it by running
`timedatectl set-ntp 0` && `systemctl disable systemd-timesyncd.service`


## IPv6
Pas envie


## 10. MAC Address Spoofing

`macchanger -e (network interface)`
- BVOutton pour changer de mac addr auto

___

## USB 
It is best to block all newly connected USBs by default to prevent these attacks. USBGuard is good for this.

You could use "nousb" as a boot parameter to disable all USB support.

If using linux-hardened, set the kernel.deny_new_usb=1 sysctl.

## XX. DMA Attacks


## Core Dumps

Core dumps contain the recorded state of a program at the time it crashed. They can contain information such as passwords and encryption keys (and you don't want that). It is therefore recommended by totopirate to deactivate them

There are three ways to disable them. With sysctl, systemd and ulimit. The sysctl method may not properly disable core dumps because systemd overrides it. I use all three methods to make sure that core dumps are disabled.
Source |: https://wiki.archlinux.org/title/Core_dump
https://linux-audit.com/understand-and-configure-core-dumps-work-on-linux/

### Sysctl
edit /etc/sysctl.conf `kernel.core_pattern=|/bin/false

### Systemd

Create /etc/systemd/coredump.conf.d/custom.conf 

`[Coredump]
Storage=none` 

### Ulimit

In /etc/security/limits.conf add `* hard core 0`

### Disabling setuid processes from dumping their memory

Process that run with elevated privileges (setuid) may still dump their memory even after these settings. To prevent them from doing this create /etc/sysctl.d/suid_dumpable.conf and add

``fs.suid_dumpable=0``

BTW arch make this by default, so you have chose the good way

## Microcode Updates

Microcode updates are important. They can fix CPU vulnerabilities such the Meltdown and Spectre bugs. But of course you don't no the plan of NSA.


## PAM
-Yubikey