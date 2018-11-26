#######################################################
# ---- WIP ----> Check jupyter container in hoffcloud #
#######################################################

from database import Database
import uuid

class Functions(object):


    #### Private Methods ####

    def __init__(self):
        self._db = Database()
        self._init_data, self._init_data_order = \
            self._initial_data()

    def _initial_data(self):
        aDict = {"username": [],
                 "hash": [],
                 "seed": [],
                 "queue": [],
                 "trigger": []}

        order = ["username",
                 "hash",
                 "seed",
                 "queue",
                 "trigger"]

        return aDict, order

    def _create_table(self):
        self._db.create("functions",
                        self._init_data,
                        order=self._init_data_order)


    #### Public Methods ####

    def create(self):
        self._create_table()


    def queue(self):
        pass

    def show(self, aTableName):
        data = self._db.read(aTableName)
        return data
