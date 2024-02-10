from datetime import datetime
class Cmn_Validation():
    
    def check_object_format(row):

        try:
            isinstance(row[0], str)
            isinstance(row[1], int)
            isinstance(row[2], int)
            isinstance(datetime.strptime(row[3], '%Y-%m-%d %H:%M'), datetime)
        except:
            raise