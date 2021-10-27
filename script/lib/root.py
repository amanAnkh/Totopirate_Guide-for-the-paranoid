import subprocess

#sed -e 's/^\([^#].*\)/# \1/g'

def securetty(void):
    p = subprocess.Popen(["sed", "-e", "'s/^\([^#].*\)/# \1/g'", "/etc/securetty"])