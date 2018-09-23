import json


class Config:
    data_directory = './data'

    @staticmethod
    def load_data(file, default):
        try:
            with open('%s/%s' % (Config.data_directory, file), 'r', encoding='utf8') as io:
                result = json.load(io)
            return result
        except:
            return default

    @staticmethod
    def dump_data(file, data):
        try:
            with open('%s/%s' % (Config.data_directory, file), 'w', encoding='utf8') as io:
                json.dump(data, io, ensure_ascii=False, indent=4)
            return True
        except:
            return False
