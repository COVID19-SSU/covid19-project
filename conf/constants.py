from datetime import datetime
import enum
class Type(enum.Enum):
    CITY = enum.auto()
    STATUS = enum.auto()
    GEN_AGE = enum.auto()



TODAY = datetime.today().strftime("%Y%m%d")

