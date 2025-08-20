class ConfigModel:
    def __init__(self):
        self.interval = 60 * 1
        self.log_title_format = "# %Y-%m-%d"
        self.base_log_path = "logs"
        self.log_file = f"{self.base_log_path}/log.md"

    @property
    def interval(self):
        return self._interval

    @property
    def log_title_format(self):
        return self._log_title_format

    @property
    def base_log_path(self):
        return self._base_log_path

    @property
    def log_file(self):
        return self._log_file

    @interval.setter
    def interval(self, value):
        self._interval = value

    @log_title_format.setter
    def log_title_format(self, value):
        self._log_title_format = value

    @base_log_path.setter
    def base_log_path(self, value):
        self._base_log_path = value

    @log_file.setter
    def log_file(self, value):
        self._log_file = value
