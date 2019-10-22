"""
Models for administrative users
"""
import shelve
from settings import config

INFO_KEY = 'info'

REGISTRY_CODE = (
    '01',
    '02',
    '03',
    '04',
    '05',
    '06',
    '07',
    '08',
    '10',
    '11',
    '12',
    '13',
    '14',
    '15',
    '16',
    '17',
    '18',
    '19',
    '20',
    '21',
    '22',
    '23',
    '24',
    '25',
    '26',
    '27',
    '28',
    '29',
    '31',
    '32',
    '50'
)


class Dialog:
    """
    class for shelve of dialog status and for some information storing during dialog with admin
    """
    def __init__(self, chat_id):
        self._dialog = shelve.open(config.DIALOG, writeback=True)
        self._id = str(chat_id)
        self._info = {}
        self._state = None
        self._check_state()
        self._check_info()

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
            self.state = config.DialogState.NoDialog

    def _check_info(self):
        """
        check if dict of company info in shelve file, add if not
        :return:
        """
        if INFO_KEY in self._dialog:
            self._info = self._dialog[INFO_KEY]
        else:
            self.info = self._info

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, dialog_status):
        self._state = dialog_status
        self._dialog[self._id] = self._state

    @property
    def info(self):
        return self._info

    @info.setter
    def info(self, company_info):
        self._info = company_info
        self._dialog[INFO_KEY] = self._info


class Admin:
    def __init__(self, chat_id):
        self._chat_id = chat_id
        self._dialog = Dialog(self._chat_id)

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

    def set_company_info(self, company_info):
        self._dialog.info = company_info

    def get_company_name(self):
        if 'name' in self._dialog.info:
            return self._dialog.info['name']
        else:
            return ''

    def set_company_name(self, company_name):
        """
        if company name is valid return True, else False
        :param company_name:
        :return True: is company name is valid, False: otherwise
        """
        self._dialog.info['name'] = company_name

    def get_company_taxpayer(self):
        if 'taxpayerID' in self._dialog.info:
            return self._dialog.info['taxpayerID']
        else:
            return ''

    def set_company_taxpayer(self, taxpayerID):
        """
        if tax payer ID is valid then return True, else return False
        :param taxpayerID:
        :return True: is tax payer ID is valid, False: otherwise
        """
        check = False
        if taxpayerID.isnumeric():
            if len(taxpayerID) == 10:
                coefficients10 = (2, 4, 10, 3, 5, 9, 4, 6, 8)
                check_num = self._calc_check_num(taxpayerID, coefficients10)
                check = check_num == int(taxpayerID[9])
            elif len(taxpayerID) == 12:
                coefficients11 = (7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
                check_num = self._calc_check_num(taxpayerID, coefficients11)
                check = check_num == int(taxpayerID[10])
                if check:
                    coefficients12 = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
                    check_num = self._calc_check_num(taxpayerID, coefficients12)
                    check = check_num == int(taxpayerID[11])
            if check:
                self._dialog.info['taxpayerID'] = taxpayerID
        return check

    def get_company_registry(self):
        if 'registrationID' in self._dialog.info:
            return self._dialog.info['registrationID']
        else:
            return ''

    def set_company_registry(self, registrationID):
        """
        if tax registry code is valid then return True, else return False
        :param registrationID:
        :return True: if registry code is valid, False: otherwise
        """
        check = False
        if registrationID.isnumeric():
            if len(registrationID) == 9:
                check = registrationID[4:6] in REGISTRY_CODE
        if check: self._dialog.info['registrationID'] = registrationID
        return check

    def _calc_check_num(self, taxpayerID, coefficients):
        check_sum = 0
        for n, k in zip(taxpayerID, coefficients):
            check_sum += int(n) * k
        return (check_sum % 11) % 10

