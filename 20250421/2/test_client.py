from unittest.mock import patch, MagicMock
from mood.client import MUD


def test_attack_with_weapon():
    # Создаем мок объекта MUD
    mock_send = MagicMock()
    player = MUD("test_player")
    player.send = mock_send  # Мокаем метод send

    # Эмулируем ввод команды
    with patch('builtins.input', return_value='attack dragon with axe'):
        player.do_attack("dragon with axe")

    # Проверяем, что отправлена правильная команда
    mock_send.assert_called_with("attack dragon 20")


def test_attack_default_weapon():
    mock_send = MagicMock()
    player = MUD("test_player")
    player.send = mock_send

    with patch('builtins.input', return_value='attack dragon'):
        player.do_attack("dragon")

    mock_send.assert_called_with("attack dragon 10")  # sword -> 10


def test_addmon_valid():
    mock_send = MagicMock()
    player = MUD("test_player")
    player.send = mock_send

    # Эмулируем ввод: addmon jgsbat hp 100 coords 3 4 hello "Boo!"
    with patch('builtins.input', return_value='addmon default hp 100 coords 3 4 hello "Boo!"'):
        player.do_addmon("jgsbat hp 100 coords 3 4 hello Boo!")

    # Проверяем отправленную команду
    mock_send.assert_called_with("addmon jgsbat 3 4 100 Boo!")


def test_addmon_invalid_monster():
    mock_send = MagicMock()
    player = MUD("test_player")
    player.send = mock_send

    # Пытаемся добавить неизвестного монстра
    with patch('builtins.input', return_value='addmon unknown_monster hp 100 coords 0 0 hello Hi'):
        player.do_addmon("unknown_monster hp 100 coords 0 0 hello Hi")

    # Проверяем, что команда не отправлена, а выведена ошибка
    mock_send.assert_not_called()
