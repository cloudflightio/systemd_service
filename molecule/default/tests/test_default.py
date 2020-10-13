import os

import testinfra.utils.ansible_runner
import pytest

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')

service_names = [
    ('test'),
    ('test_newimagesyntax'),
    ('test_pullunit')
]


@pytest.mark.parametrize("name", service_names)
def test_service(host, name):
    service = host.service(name)

    assert service.is_running
    assert service.is_enabled


@pytest.mark.parametrize("name", service_names)
def test_payload(host, name):
    f = host.file("/srv/data/container/test/" + name)

    assert f.exists


def test_port(host):
    s = host.socket("tcp://0.0.0.0:9999")

    assert s.is_listening


def test_pullunit(host):
    f = host.file("/etc/systemd/system/test_pullunit-pull@.service")

    assert f.exists

    host.run_test('systemctl start test_pullunit-pull@3.4')
    # parser magic:
    # ansible/jinja                -> bash         -> golang
    # '{{ '{{' }} .Tag {{ '}}' }}' -> '{{ .Tag }}' -> {{ .Tag }}
    cmd = host.run(
        r"docker images alpine --format '{{ '{{' }} .Tag {{ '}}' }}'")
    tags = cmd.stdout.split('\n')

    assert '3.4' in tags
    assert 'latest_pull' in tags
