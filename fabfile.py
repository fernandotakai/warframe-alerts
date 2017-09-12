import os
from fabric.api import local, env
from dockerfabric.api import docker_fabric


env.docker_tunnel_local_port = 22024  # or any other available port above 1024 of your choice

docker_client = docker_fabric()


def get_image_name():
    image_name = 'warframe-alert'

    if env.docker_username:
        image_name = '%s/%s' % (env.docker_username, image_name)

    return image_name


def build():
    local('docker build . -t %s' % get_image_name())


def push():
    if getattr(env, 'docker_username', None):
        local('docker push %(docker_username)s/warframe-alert' % env)
    else:
        print('No docker_username set. Not pushing.')


def pull():
    docker_client.pull(get_image_name())


def stop():
    docker_client.stop('warframe_alert')


def logs():
    docker_client.logs('warframe_alert')


def start():
    docker_client.start('warframe_alert')


def remove():
    docker_client.remove_container('warframe_alert')


def start_from_scratch():
    env_vars = [
        'CONSUMER_KEY',
        'CONSUMER_SECRET',
        'ACCESS_TOKEN',
        'ACCESS_TOKEN_SECRET',
        'PUSHBULLET_TOKEN',
        'ALERTS',
    ]

    docker_env = {e: os.getenv(e) for e in env_vars}

    docker_client.create_container(get_image_name(), environment=docker_env,
                                   name='warframe_alert', detach=True)


STEPS = {
    'running': (build, push, stop, remove, pull, start_from_scratch, start),
    'exited': (build, push, remove, pull, start_from_scratch, start),
    'deleted': (build, push, pull, start_from_scratch, start),
    'created': (build, push, pull, start_from_scratch, start)
}


def deploy():
    status = get_container_status('ofensivaria')

    for step in STEPS[status]:
        step()


def get_container_status(container_name):
    try:
        container = docker_client.containers(filters={'name': container_name}, all=True)[0]
        return container['State']
    except IndexError:
        return 'deleted'
