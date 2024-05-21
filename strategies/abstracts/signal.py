class SignalException(Exception):
    pass


class SignalExistenceException(SignalException):
    def __init__(self, attr_name):
        message = f"{attr_name}, must be filled"
        super().__init__(message)


class SignalValidityException(SignalException):
    def __init__(self, attr_name, valid_list):
        valid_list_str = str(valid_list)
        message = f"{attr_name} value is not valid, must be one of {valid_list_str}"
        super().__init__(message)


class SignalTypeException(SignalException):
    def __init__(self, attr_name, expected_type):
        message = f"{attr_name} type is not valid, must be {expected_type}"
        super().__init__(message)


class Signal:

    strategy_name: str = ""
    symbol: str = ""
    symbol_type: str = ""
    session: str = ""
    timeframes: list = []
    timestamps_discovery: dict = {}
    timestamps_open: dict = {}
    timestamps_finish: dict = {}
    direction: str = ""
    status: str = ""
    activate_type: str = ""
    entry: float = 0
    sl: float = 0
    tp_not_done: list = []
    tp_done: list = []
    indicators_info: dict = {"meta_data": {}, "data": {}}

    def validate(self):
        self._check_existence()
        self._check_type()
        self._check_validity()

    def to_dict(self):
        return self.__dict__

    def _check_existence(self):
        not_existence = {
            "strategy_name": "",
            "symbol": "",
            "symbol_type": "",
            "session": "",
            "timeframes": [],
            "timestamps_discovery": {},
            "timestamps_open": {},
            "timestamps_finish": {},
            "tp_not_done": [],
            "tp_done": [],
        }

        for attr_name, attr_not_exist in not_existence.items():
            if getattr(self, attr_name) == attr_not_exist:
                raise SignalExistenceException(attr_name)

        if self.status == "pending":
            if self.entry == 0:
                raise SignalExistenceException("entry")
            if self.sl == 0:
                raise SignalExistenceException("sl")
            if self.activate_type == "":
                raise SignalExistenceException("activate_type")

    def _check_validity(self):
        valid_inputs = {
            "direction": ["bullish", "bearish"],
            "status": ["pending", "active", "closed", "stopped", "expired"],
            "activate_type": ["normal", "reversed"],
            "session" : ["Tokyo", "Sydney", "London", "NewYork"]
        }

        for attr_name, attr_valid in valid_inputs.items():
            if getattr(self, attr_name) not in attr_valid:
                raise SignalValidityException

    def _check_type(self):
        expected_types = {
            "strategy_name": str,
            "symbol": str,
            "symbol_type": str,
            "session": str,
            "timeframes": list,
            "timestamps_discovery": dict,
            "timestamps_open": dict,
            "timestamps_finish": dict,
            "direction": str,
            "status": str,
            "activate_type": str,
            "entry": float,
            "sl": float,
            "tp_not_done": list,
            "tp_done": list,
            "indicators_info": dict,
        }

        for attr_name, attr_type in expected_types.items():
            if not isinstance(getattr(self, attr_name), attr_type):
                raise SignalTypeException
