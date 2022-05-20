import os
import re

from .conftest import root_dir


class TestWorkflow:

    def test_workflow(self):
        yamdb_workflow_basename = 'yamdb_workflow'

        yaml = f'{yamdb_workflow_basename}.yaml'
        is_yaml = yaml in os.listdir(root_dir)

        yml = f'{yamdb_workflow_basename}.yml'
        is_yml = yml in os.listdir(root_dir)

        if not is_yaml and not is_yml:
            assert False, (
                f'В каталоге {root_dir} не найден файл с описанием workflow '
                f'{yaml} или {yml}.\n'
                '(Это нужно для проверки тестами на платформе)'
            )

        if is_yaml and is_yml:
            assert False, (
                f'В каталоге {root_dir} не должно быть двух файлов {yamdb_workflow_basename} '
                'с расширениями .yaml и .yml\n'
                'Удалите один из них'
            )

        filename = yaml if is_yaml else yml

        try:
            with open(f'{os.path.join(root_dir, filename)}', 'r') as f:
                yamdb = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что добавили файл {filename} в каталог {root_dir} для проверки'

        assert (
                re.search(r'on:\s*push:\s*branches:\s*-\smaster', yamdb) or
                'on: [push]' in yamdb or
                'on: push' in yamdb
        ), f'Проверьте, что добавили действие при пуше в файл {filename}'
        assert 'pytest' in yamdb, f'Проверьте, что добавили pytest в файл {filename}'
        assert 'appleboy/ssh-action' in yamdb, f'Проверьте, что добавили деплой в файл {filename}'
        assert 'appleboy/telegram-action' in yamdb, (
            'Проверьте, что настроили отправку telegram сообщения '
            f'в файл {filename}'
        )
