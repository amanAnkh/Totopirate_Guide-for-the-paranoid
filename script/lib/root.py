import subprocess

# comment all TTY devices the root user is allowed to login on
def securetty():
    p = subprocess.run(
        [
            "sed",
            "-i",
            r"s/^\([^#].*\)/# \1/g",
            "/etc/securetty"
        ])
    return True if (p == 0) else False


# Lock root account (TODO: optionnel lock account)
def lock_root():
    p = subprocess.Popen(["passwd", "-l", "root"])
    return True if (p == 0) else False

# uncomment `auth required pam_wheel.so use_uid`
def restriction_su():
    p = subprocess.run(
        [
            "sudo",
            "sed",
            "-i",
            "/#auth           required        pam_wheel.so use_uid/s/^#//g",
            "/etc/pam.d/su"
        ])
    return True if (p == 0) else False

def increase_num_hashing_rounds():
    p = subprocess.run(
        [
            "echo",
            "\"password required pam_unix.so sha512 shadow nullok rounds=65536\"",
            ">", 
            "test"
        ], capture_output=True, text=True)
    print("stdout:", p.stdout)
    print("stderr:", p.stderr)
    return True if (p == 0) else False