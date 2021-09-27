# import datetime
# from error_handlers import errors
#
# @errors
# def age_user(date_of_birth):
#     '''
#     check Date Of Birth
#     :param date_of_birth:  date in dict info user vk, str
#     :return: int
#     '''
#
#
#
#     bdate = date_of_birth
#     bdate = datetime.datetime.strptime(bdate, '%d.%m.%Y')
#     bdate = bdate.strftime('%Y')
#     bdate = int(bdate)
#
#
#     print(bdate)
#
#     date_now = datetime.date.today()
#     date_now = datetime.datetime.strptime( f'{date_now}' , '%Y-%m-%d')
#     date_now = date_now.strftime('%Y')
#     date_now = int(date_now)
#     age = date_now - bdate
#     print(age)
#     return age
#
#
