import json
import subprocess
import os

from gi.reposity import Snapd

class SnapLoginHandler:
    auth_data_path = os.path.join(os.path.expanduser('~'), 'deleteme')

    def __init__(self):
        self.authenticate_snapd()

    def authenticate_snapd(self):
        self.auth_data = self._load_auth_data()
        if self.auth_data is None:
            self._invite_signup_ubuntu()
            username = self._ask_for_username()
            password = self._ask_for_password()
            self.auth_data = self._attempt_login(username=username, password=password)
            self._save_auth_data()

    def _attempt_login(self, username, password, two_fa=None):
        try:
            return Snapd.login_sync(username, password, two_fa)
        except Exception as ex:
            if ex.domain == "snapd-error-quark" and ex.code == Snapd.Error.TWO_FACTOR_REQUIRED:
                return self._attempt_login(username=username, password=password, two_fa=self._ask_for_2FA())
            else:
                return None

    def _ask_for_username(self):
        """_ask_for_username

            invite the user to provide his username.
        """
        username = None
        try:
            username = subprocess.check_output(["zenity", "--entry", \
            "--title", "Authentication for Snappy", \
            "--text", "Please enter your e-mail address for your Ubuntu One account."]).decode("ascii").replace('\n', '')
        except subprocess.CalledProcessError:
            self._show_authentication_error()
        finally:
            return username

    def _ask_for_password(self):
        """_ask_for_password

            invite the user to provide his password
        """
        password = None
        try:
            password = subprocess.check_output(["zenity", "--password", \
            "--title", "Authentication for Snappy", \
            "--text", "Please enter your Ubuntu One password"]).decode("ascii").replace("\n", "")
        except subprocess.CalledProcessError:
            self._show_authentication_error()
        finally:
            return password

    def _ask_for_2FA(self):
        two_factor_auth = None
        try:
            two_factor_auth = subprocess.check_output(["zenity", "--entry", \
            "--title", "Authentication for Snappy", \
            "--text", "Please enter your 2 factor authentication code"]).decode("ascii").replace("\n", "")
        except subprocess.CalledProcessError:
            self._show_authentication_error()
        finally:
            return two_factor_auth

    def _invite_signup_ubuntu(self):
        """_invite_signup_ubuntu

            invite user to signup to Ubuntu One if it isn't already the case.
        """
        try:
            subprocess.check_output(["zenity", "--question", \
            "--title", "Authentication for Snappy" \
            "--text", "To install snaps from the Ubuntu Store(without being root), you need an Ubuntu One account.\n\n\Do you have an Ubuntu One account?", \
            "--ok-label", "Continue", \
            "--cancel-label", "Sign up"]).decode("ascii")
        except subprocess.CalledProcessError:
            subprocess.Popen(["xdp-open", "https://login.ubuntu.com/"])

    def _load_auth_data(self):
        auth_data = None
        if os.path.exists(self.auth_data_path):
            with open(self.auth_data_path) as stream:
                auth_data = json.load(stream)
            macaroon = auth_data['macaroom']
            discharges = auth_data['discharges']
            auth_data = Snapd.AuthData.new(macaroon, discharges)
        return auth_data

    def _show_authentication_error(self):
        subprocess.call(["zenity", "--error", \
        "--title", "Authentication for Snappy", \
        "--text", "No credentials were supplied. This snap cannot be installed"])

    def _save_auth_data(self):
        auth_data_to_save = {
            "macaroon": Snapd.AuthData.get_macaroon(self.auth_data),
            "discharges": Snapd.AuthData.get_discharges(self.auth_data)
        }
        with open(self.auth_data_path, "w+") as f:
            f.write(json.dumps(auth_data_to_save))
            f.close()
