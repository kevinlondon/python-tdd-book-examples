from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random
import os

REPO_URL = "https://github.com/kevinlondon/python-tdd-book-examples.git"

def deploy():
    site = Site(host=env.host, user=env.user)
    site.create_directory_structure()
    site.get_latest_source()
    site.update()


class Site(object):

    def __init__(self, host, user):
        self.host = host
        self.user = user
        self.folder = os.path.join("/", "home", user, "sites", host, "source")
        self.superlists_folder = os.path.join(self.folder, "superlists")

    def create_directory_structure(self):
        for subfolder in ("database", "static", "virtualenv", "source"):
            run('mkdir -p %s/%s' % (self.folder, subfolder))

    def get_latest_source(self):
        if exists(self.folder + "/.git"):
            run("cd %s && git fetch" % self.folder)
        else:
            run("git clone %s %s" % (REPO_URL, self.folder))

        current_commit = local("git log -n 1 --format=%H", capture=True)
        run("cd %s && git reset --hard %s" % (self.folder, current_commit))

    def update(self):
        self.update_settings()
        self.update_virtualenv()
        self.update_static_files()
        self.update_database()

    def update_settings(self):
        settings_path = self.superlists_folder + "/superlists/settings.py"
        sed(settings_path, "DEBUG = True", "DEBUG = False")
        sed(settings_path, "DOMAIN = \"localhost\"", "DOMAIN = \"s\"" % self.host)
        secret_key_file = self.superlists_folder + "/superlists/secret_key.py"
        if not exists(secret_key_file):
            chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
            key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
            append(secret_key_file, "SECRET_KEY = '%s'" % key)

        append(settings_path, "\nfrom .secret_key import SECRET_KEY")

    def update_virtualenv(self):
        virtualenv_folder = self.folder + "/../virtualenv"
        if not exists(virtualenv_folder + "/bin/pip"):
            run("virtualenv --python=python3 %s" % virtualenv_folder)

        run("%s/bin/pip install -r %s/requirements.txt" % (
                virtualenv_folder, self.folder
        ))

    def update_static_files(self):
        run(("cd %s && ../../virtualenv/bin/python3 manage.py collectstatic "
             "--noinput" % self.superlists_folder))

    def update_database(self):
        run(("cd %s && ../../virtualenv/bin/python3 manage.py migrate "
             "--noinput" % self.superlists_folder))
