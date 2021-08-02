from application.salary import *
from application.people import *
from datetime import datetime


if __name__=='__main__':
    print(datetime.now())
    get_employees()
    calculate_salary()