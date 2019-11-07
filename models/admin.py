"""
Models for administrative users
"""
import json
import shelve
from DB.DBAlchemy import DBManager
from models.store import Store
from settings import config

INFO_KEY = 'info'
STORE_KEY = 'store'
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
        self._store = {}
        self._state = None
        self._check_state()
        self._check_info()
        self._check_type()

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

    def _check_store(self):
        """
        check if dict of store info in shelve file, add if not
        :return:
        """
        if STORE_KEY in self._dialog:
            self._store = self._dialog[STORE_KEY]
        else:
            self.store = self._store

    def _check_type(self):
        """
        check if dialog has a type parameter (bool: True is change dialog type, False: if add dialog type)
        :return:
        """
        if not 'type' in self._dialog:
            self._dialog['type'] = False

    @property
    def type(self):
        """
        get type status of dialog
        :return:
        """
        return self._dialog['type']

    @type.setter
    def type(self, dialog_type):
        """
        set type of dialog
        :param dialog_type:
        :return:
        """
        self._dialog['type'] = dialog_type

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

    @property
    def store(self):
        return  self._store

    @store.setter
    def store(self, store_info):
        self._store = store_info
        self._dialog[STORE_KEY] = self._store


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

    @property
    def dialog_type(self):
        return self._dialog.type

    @dialog_type.setter
    def dialog_type(self, dialog_type):
        self._dialog.type = dialog_type

    def dialog_info_save(self):
        """
        save info about company from dialog to json file
        :return:
        """
        with open(config.COMPANY_INFO, mode='w') as file_obj:
            json.dump(self._dialog.info, file_obj)

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
        check = True
        if check: self._dialog.info['name'] = company_name
        return check

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

    def get_company_address(self):
        if 'address' in self._dialog.info:
            return self._dialog.info['address']
        else:
            return ''

    def set_company_address(self, address):
        """
        if address is valid then return True, else return False
        :param address:
        :return True: if address is valid, False: otherwise
        """
        check = True
        if check: self._dialog.info['address'] = address
        return check

    def get_company_phone(self):
        if 'phone' in self._dialog.info:
            return self._dialog.info['phone']
        else:
            return ''

    def set_company_phone(self, phone):
        """
        if phone is valid then return True, else return False
        :param phone:
        :return True: if phone is valid, False: otherwise
        """
        check = True
        if check: self._dialog.info['phone'] = phone
        return check

    def get_company_email(self):
        if 'email' in self._dialog.info:
            return self._dialog.info['email']
        else:
            return ''

    def set_company_email(self, email):
        """
        if email is valid then return True, else return False
        :param email:
        :return True: if email is valid, False: otherwise
        """
        check = True
        if check: self._dialog.info['email'] = email
        return check

    def get_bank_name(self):
        if 'bank_account' in self._dialog.info:
            if 'name' in self._dialog.info['bank_account']:
                return self._dialog.info['bank_account']['name']
        else:
            return ''

    def set_bank_name(self, bank_name):
        """
        if bank name is valid then return True, else return False
        :param bank_name:
        :return True: if bank name is valid, False: otherwise
        """
        check = True
        if check:
            self._check_info_bank()
            self._dialog.info['bank_account']['name'] = bank_name
        return check

    def get_bank_id(self):
        if 'bank_account' in self._dialog.info:
            if 'id' in self._dialog.info['bank_account']:
                return self._dialog.info['bank_account']['id']
        else:
            return ''

    def set_bank_id(self, bank_id):
        """
        if bank id is valid then return True, else return False
        :param bank_id:
        :return True: if bank id is valid, False: otherwise
        """
        check = False
        if bank_id.isnumeric():
            check = len(bank_id) == 9
        if check:
            self._check_info_bank()
            self._dialog.info['bank_account']['id'] = bank_id
        return check

    def get_bank_account(self):
        if 'bank_account' in self._dialog.info:
            if 'account' in self._dialog.info['bank_account']:
                return self._dialog.info['bank_account']['account']
        else:
            return ''

    def set_bank_account(self, bank_account):
        """
        if bank account is valid then return True, else return False
        :param bank_account:
        :return True: if bank account is valid, False: otherwise
        """
        check = False
        if bank_account.isnumeric():
            if len(bank_account) == 20:
                check = self._check_account(bank_account)
        if check:
            self._check_info_bank()
            self._dialog.info['bank_account']['account'] = bank_account
        return check

    def get_bank_corr(self):
        if 'bank_account' in self._dialog.info:
            if 'corr_acc' in self._dialog.info['bank_account']:
                return self._dialog.info['bank_account']['corr_acc']
        else:
            return ''

    def set_bank_corr(self, bank_corr):
        """
        if bank corr account is valid then return True, else return False
        :param bank_corr:
        :return True: if bank corr account is valid, False: otherwise
        """
        check = False
        if bank_corr.isnumeric():
            if len(bank_corr) == 20:
                check = True
        if check:
            self._check_info_bank()
            self._dialog.info['bank_account']['corr_acc'] = bank_corr
        return check

    def _check_account(self, account):
        """
        if account number is valid then return True, else return False
        :param account:
        :return True: if account is valid, False: otherwise
        """
        check_sum = 0
        for n, k in zip(account, '713' * 8):
            check_sum += int(n) * int(k)
        return (check_sum % 10) == 0

    def _check_info_bank(self):
        if not 'bank_account' in self._dialog.info:
            self._dialog.info['bank_account'] = {}

    def dialog_store_save(self, db: DBManager):
        """
        save info about store from dialog to database
        :return:
        """
        store = Store()
        store.title = self._dialog.store['title']
        store.address = self._dialog.store['address']
        store.longitude = self._dialog.store['longitude']
        store.latitude = self._dialog.store['latitude']
        store.price_km = self._dialog.store['price']
        db.save_element(store)

    def set_store_info(self, store_info):
        self._dialog.store = store_info

    def get_store_title(self):
        if 'title' in self._dialog.store:
            return self._dialog.store['title']
        else:
            return ''

    def set_store_title(self, store_title):
        """
        if store title is valid return True, else False
        :param store_title:
        :return True: is store title is valid, False: otherwise
        """
        check = True
        if check: self._dialog.store['title'] = store_title
        return check

    def get_store_address(self):
        if 'address' in self._dialog.store:
            return self._dialog.store['address']
        else:
            return ''

    def set_store_address(self, store_address):
        """
        if store address is valid return True, else False
        :param store_address:
        :return True: is store address is valid, False: otherwise
        """
        check = True
        if check: self._dialog.store['address'] = store_address
        return check

    def get_store_longitude(self):
        if 'longitude' in self._dialog.store:
            return self._dialog.store['longitude']
        else:
            return ''

    def set_store_longitude(self, store_longitude):
        """
        if store longitude is valid return True, else False
        :param store_longitude:
        :return True: is store longitude is valid, False: otherwise
        """
        check = True
        if check: self._dialog.store['longitude'] = store_longitude
        return check

    def get_store_longitude(self):
        if 'longitude' in self._dialog.store:
            return self._dialog.store['longitude']
        else:
            return ''

    def set_store_latitude(self, store_latitude):
        """
        if store latitude is valid return True, else False
        :param store_latitude:
        :return True: is store latitude is valid, False: otherwise
        """
        check = True
        if check: self._dialog.store['latitude'] = store_latitude
        return check

    def get_store_price(self):
        if 'price' in self._dialog.store:
            return self._dialog.store['price']
        else:
            return ''

    def set_store_price(self, store_price):
        """
        if store delivery price per km is valid return True, else False
        :param price:
        :return True: is store delivery price per km is valid, False: otherwise
        """
        check = True
        if check: self._dialog.store['price'] = store_price
        return check