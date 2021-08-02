from application import people
from application import salary
from datetime import datetime



if __name__=='__main__':
    print(datetime.now())
    people.get_employees()
    salary.calculate_salary()
    