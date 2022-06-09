from psa_soporte.database import Base, engine
from psa_soporte.models import *

if __name__ == "__main__":
    Base.metadata.create_all(engine)