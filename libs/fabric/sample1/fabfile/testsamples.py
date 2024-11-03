from fabric import task, Connection, SerialGroup, ThreadingGroup, Config


@task
def thostname(c):
    return c.run("hostname")
