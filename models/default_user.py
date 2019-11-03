"""
Models for default user for login purpose
"""
import binascii
import hashlib
import shelve
from settings.config import DEFAULT_ADMIN, DEFAULT_KEEPER, DEFAULT_TRADER, DIALOG, DialogState

class InitDialog:
    """
    class for shelve of dialog status
    and for some information storing during dialog with default user
    """

    def __init__(self, chat_id):
        self._dialog = shelve.open(DIALOG, writeback=True)
        self._id = str(chat_id)
        self._state = None
        self._check_state()

    def finish(self):
        self._dialog.close()

    def _check_state(self):
        """
        check if state of dialog status in shelve file, add if not
        :return:
        """
        if self._id in self._dialog:
            self._state = self._dialog[self._id]
        else:
            self.state = DialogState.NoDialog

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, dialog_status):
        self._state = dialog_status
        self._dialog[self._id] = self._state


class DefaultUser:
    def __init__(self, chat_id):
        self._chat_id = chat_id
        self._dialog = InitDialog(self._chat_id)

    def __del__(self):
        """
        close a dialog - shelve file
        :return:
        """
        self._dialog.finish()

    @property
    def chat_id(self):
        return self._chat_id

    @property
    def dialog_status(self):
        return  self._dialog.state

    @dialog_status.setter
    def dialog_status(self, dialog_status):
        self._dialog.state = dialog_status

    def check_password(self, password):
        pass_hash = _get_hash(password)
        check_hash = ''
        if self._dialog.state == DialogState.UserTrader:
            check_hash = DEFAULT_TRADER
        if self._dialog.state == DialogState.UserKeeper:
            check_hash = DEFAULT_KEEPER
        if self._dialog.state == DialogState.UserAdmin:
            check_hash = DEFAULT_ADMIN
        return pass_hash == check_hash

def _get_hash(password):
    """
    calculate hash on password
    :param password:
    :return hash:
    """
    hex_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), b'user', 100_000)
    return binascii.hexlify(hex_hash)
