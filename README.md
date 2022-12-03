# aiogram_Digit 
![Telegram](https://cdn-icons-png.flaticon.com/128/2504/2504941.png)      ![Team](https://cdn-icons-png.flaticon.com/128/9016/9016297.png)
## _Корпоративный продукт для TeamBilding'a_

aiogram_Digit - это продукт, разаботанный спецально для Кейса от копании Onellect. Решение кейса представляет собой Telegram бота:
- Подбирающего людей со схожими интересами, для неформального общения 
- А также помогает таким людям определиться со временем встречи

## Client
##### &emsp;Клиентская часть
Команда начала диалога с ботом - `/start`. После её ввода появится следующее меню:![Telegram](https://sun1-56.userapi.com/impg/CgrI1CsGopKEuivwOssCVl4j0msxQKwn3hRj5Q/epZoxlnjSNo.jpg?size=846x490&quality=96&sign=3d51990b97e57672c6d926b454b05212&type=album)

- `DashBoard`| В меню компания может добавить свои основные контакты для связи. В данный момент в этом меню находится маленькое описание команды разработчиков.
- `Создать🚀` | Данная кнопка переводит на создание анкеты, где нужно указать основную информацию о себе, а также опциональную.

![Telegram](https://sun9-85.userapi.com/impg/IfYuV8cmTFbhj242DfCLdFJRDAtwa9IKZvmvJw/OGXk9QOmm6c.jpg?size=852x615&quality=96&sign=7662c2c4b56145517bb934ab4cf43c84&type=album!)
![Telegram](https://sun9-78.userapi.com/impg/2aR24QVwFjfO4CZ2cZhUXHosOg43NQ2F1iwDig/i-mb9cg24io.jpg?size=854x234&quality=96&sign=ddac3dff5aac9dd9003de6e1972c3e4e&type=album)

После заполнения анкеты выводится глваное меню, через которое пользователь имеет доступ ко всем основным функциям бота.

![Telegram](https://sun9-14.userapi.com/impg/YWv_iO4u_2Urf4FYPEZgdCrThDYS8ZBVQzIxYQ/HEQSDw1-tRs.jpg?size=458x198&quality=96&sign=c5c6d653b9fc35bbc566b71f6db0db5c&type=album)

Рассмотрим подробнее каждый раздел:
- `Оценить проект`| это раздел для обратной связи, в котором пользователь может оценить проект от 1 до 5 (Раздел Demo версии).
- `Последние встречи` | Данная кнопка выводит список последних пользователей, с которыми вы договорились на встречу.
- `Events` | Показательный раздей, который не имеет никакого функционала. В зависимости от необходимости может быть доработан. Онасовная идея раздела: наличие общих мероприятий (аналогия миникорпоративу). Само меню:
![Telegram](https://sun9-77.userapi.com/impg/rhDQcF19e49mxVqiKOKv_Kyoy2y9kMjMvibaNQ/Sq38l-4T8JY.jpg?size=454x196&quality=96&sign=91f0940cd216b7649f6317e70eca1d1e&type=album)
- `Новая анкета` | Данная функция предлагает пользователю создать новый профиль, или отредактировать старый.
- `Моя анкета` | Выводит пользователю его анкету. Само меню:
![Telegram](https://sun9-76.userapi.com/impg/Mc3MTegPBCefzHi0wHTv_y7Mb56QPcFmHjKC-A/pQlGFEZ6SOg.jpg?size=426x563&quality=96&sign=471be9202794b1b1544688f3fb51d488&type=album)
- `Смотреть анкеты` | Основная функция бота. В данном разделе пользователю предстваляется циклический подбор анкет. После нажатия на кнопку, бот показывает анкету другого пользователя. На анкету можно отреагироавть 3-мя кнопками:
    - `👍` - Отправить предложение о встречи. В случае, если пользователь указал удобное ему время, предлогается выбор по времени, в ином случае, данный пункт пропускается:
    ![Telegram](https://sun9-14.userapi.com/impg/D3h4xspkJxH2I_xhvyzk7TIBoXLSCDMq4wjeeg/lpzPlHcLYGM.jpg?size=852x372&quality=96&sign=c5a22f6d765531dde828e864cab0b4b4&type=album)
    
    После выбора времени, предложение отправляется:
    
    ![Telegram](https://sun9-45.userapi.com/impg/Y_IMYYDx3gaL-rZOlXYsagzFE8s9tYSDEsH4qA/_3TVBYbzP9Y.jpg?size=441x56&quality=96&sign=cf1618183b165bf8b62f689e7e8dba9f&type=album)
    
    - `👎` - Пропустить анкету. Переход к следующей анкете.
    - `🛑` - Выходит из выбора анкет в `Главное веню`.

## Server
##### &emsp;Серверная часть
Проект состоит из 3-х папок: `/DataBase`, `/KeyBoard`, `/metric_api`, - и двух файлов инициации: `main_client.py` и `/metric_api/json_api.py`. 
- `main_client.py` - инициирует запуск telegram бота. Команда запуска:
    ```python
    python3 main_client.py
    ```
- `/metric_api/json_api.py` - инициирует запуск сервера метрик. Подробнее в раздели `Метрики`.
    ```python
    python3 metric_api/json_api.py
    ```
