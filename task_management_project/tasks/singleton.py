class TaskConfig:
    _instance = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(TaskConfig, cls).__new__(cls)
            cls._instance.config_data = {}
        return cls._instance
    
    def set_config(self, key, value):
        self.config_data[key] = value

    def get_config(self, key, default=None):
        return self.config_data.get(key, default)