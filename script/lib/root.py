import subprocess

# comment all TTY devices the root user is allowed to login on
def securetty(void):
    p = subprocess.run(["sed", "-i", r"s/^\([^#].*\)/# \1/g", "/etc/securetty"])

# Lock root account (TODO: optionnel lock account)
def loock_root(void):
    p = subprocess.Popen(["passwd", "-l", "root"])