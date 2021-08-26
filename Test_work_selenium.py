import time as t
from selenium.webdriver import Chrome
import pytest

class Test_autorization_yandex:

    def setup_class(self):
        self.driver = Chrome()


    @pytest.mark.parametrize('phone_and_email, result',
                             [
                            ('||||||||', 'Такой логин не&nbsp;подойдет'),
                                 (r'"""""""""|||||||||@mail.ru', 'Такой логин не&nbsp;подойдет'),
                                 ('@gmail.com', 'Такой логин не&nbsp;подойдет'),
                                 ('12323435432434@yandex.ru', 'Такой логин не&nbsp;подойдет')
                             ]
                             )
    def test_autorization_yandex_login(self,phone_and_email, result):
        driver = self.driver
        driver.get('https://passport.yandex.ru/auth/')

        input_login = driver.find_element_by_xpath('//input[@data-t="field:input-login"]')
        input_login.send_keys(f'{phone_and_email}')

        buttom_enter = driver.find_element_by_id('passp:sign-in')
        buttom_enter.click()
        t.sleep(3)
        assert result in driver.page_source

    @pytest.mark.parametrize('password, result',[
        ('111111111', 'Введите символы с&nbsp;картинки'),
        ('fhhtghtyhtrtb', 'Введите символы с&nbsp;картинки'),
        ('@@@@@mail.ru', 'Введите символы с&nbsp;картинки')
        # ('____________', 'Неверный пароль'),
        # ('++++++++', 'Неверный пароль'),
        # ('467782584585-', 'Неверный пароль')
    ])
    def test_autorization_yandex_password(self, password, result):
        driver = self.driver
        driver.get('https://passport.yandex.ru/auth/')
        input_login = driver.find_element_by_xpath('//input[@data-t="field:input-login"]')
        input_login.send_keys(f'{89999999999}')

        buttom_enter = driver.find_element_by_id('passp:sign-in')
        buttom_enter.click()
        t.sleep(3)

        input_password = driver.find_element_by_xpath('//input[@data-t="field:input-passwd"]')
        input_password.send_keys(f'{password}')
        t.sleep(2)

        buttom_enter = driver.find_element_by_id('passp:sign-in')
        buttom_enter.click()
        t.sleep(3)

        assert result in driver.page_source

