import os
import re

from .conftest import infra_dir_path, root_dir


class TestDockerfileCompose:

    def test_infra_structure(self):
        assert 'infra' in os.listdir(root_dir), (
            f'Проверьте, что в пути {root_dir} указана папка `infra`'
        )
        assert os.path.isdir(infra_dir_path), (
            f'Проверьте, что {infra_dir_path} - это папка, а не файл'
        )

    def test_docker_compose_file(self):
        try:
            with open(f'{os.path.join(infra_dir_path, "docker-compose.yaml")}', 'r') as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, f'Проверьте, что в директорию {infra_dir_path} добавлен файл `docker-compose.yaml`'

        assert re.search(r'image:\s+postgres:', docker_compose), (
            'Проверьте, что  в файл docker-compose.yaml добавлен образ postgres:latest'
        )
        assert re.search(r'image:\s+([a-zA-Z0-9]+)\/([a-zA-Z0-9_\.])+(\:[a-zA-Z0-9_-]+)?', docker_compose), (
            'Проверьте, что добавили сборку контейнера из образа на вашем DockerHub в файл docker-compose.yaml'
        )
