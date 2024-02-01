from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from time import sleep
from selenium.common.exceptions import WebDriverException, NoSuchElementException, TimeoutException, ElementNotInteractableException, StaleElementReferenceException

login = input("Введите логин от вашего аккаунта на Степике: ")
password = input("Введите пароль от вашего аккаунта на Степике: ")
link_1 = input("Введите ссылку страницы, с которой хотите начать очистку поля решений: ")
link_2 = input("Введите ссылку страницы, на которой хотите закончить очистку поля решений: ")
browser = webdriver.Chrome()
# browser - это переменная, которая ссылается на объект, с помощью методов  
# которого мы взаимодействуем с браузером
browser.implicitly_wait(5)  # эта команда заставляет программу ждать 
                            # до 5 секунд и проверять каждые 0.5 секунд, 
                            # если сразу не может найти нужный элемент
link = 'https://stepik.org/'
browser.get(link)  # метод get позволяет перейти на указанную страницу

button = browser.find_element(By.ID, "ember27")  # find_element ищет 
# необходимый элемент с помощью CSS-селектора
button.click()
input_login = browser.find_element(By.NAME, "login")
input_login.send_keys(login)  # логин на Степике
input_password = browser.find_element(By.NAME, "password")
input_password.send_keys(password)  # пароль от аккаунта на Степике
submit = browser.find_element(By.CSS_SELECTOR, 'button[type="submit"]')
submit.click()
sleep(5)



def cleaner(level=0):  # функция, которая очищает поле ввода кода,
    cur_url = None     # а затем нажимает кнопку "следующий шаг"
    try:
        try:
            decide_again = browser.find_element(By.CSS_SELECTOR, 'button[class="again-btn white"]')
            # decide_again - это имя переменной, которую мы даём элементу,
            decide_again.click()
        except NoSuchElementException:  # Если элемент не найден
            print('Кнопка "решить снова" не найдена, пытаемся вставить пустую строку в поле кода')
        try:
            code_field = browser.find_element(By.CSS_SELECTOR, 'div[class="CodeMirror-code"]')
            code_field.send_keys('')
        except ElementNotInteractableException:  # В элемент нельзя ничего вставить
            print('Вставить пустую строку в поле кода не удалось, переходим к следующей странице')
        except StaleElementReferenceException:  # самое странное исключение
            level += 1
            print(f'Элемент изменился во время взаимодействия с ним, запускаем функцию рекурсивно с уровнем вложенности {level}')
            if level < 3:
                cleaner(level)
        except NoSuchElementException:  # Ещё раз уже встречающееся выше исключение 
            print('Видимо, мы находимся в шаге с теорией, переходим на следующую страницу')
        sleep(1)
        next = browser.find_element(By.CSS_SELECTOR, 'button[class="lesson__next-btn button has-icon"]')
        next.click()
        cur_url = browser.current_url  # получаем текущий адрес страницы
        print('Текущий адрес страницы:', cur_url)
    except StaleElementReferenceException:
        # с этой ошибкой программа иногда завершалась спустя десятки пройденных шагов
        print('Программа пытается вылететь из-за изменения элемента во время взаимодействия с ним')
    except WebDriverException:  # на всякий случай обрабатываем все возможные ошибки
        print('Прошла ещё какая-то ошибка, попробуем запустить функцию рекурсивно')
        cleaner(level=1)

    return cur_url  # возвращает ссылку на текущую страницу

link = None



sleep(10)

def main():
    global link
    browser.get(link_1)
    sleep(5)
    while link != link_2:
    # пока текущая страница не равна этой ссылке, продолжать
        link = cleaner()

if __name__ == '__main__':
    main()
    print('Запускаем функцию main во второй раз')
    main()  # на всякий случай два раза проходимся по всем шагам



