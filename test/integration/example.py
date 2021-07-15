import docker

client = docker.from_env()
containers = client.containers.list(limit=4)
for co in containers:
    print(co.name)
    if co.name == 'database':
        print("I am here in database container")
        co.start()