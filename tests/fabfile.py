import fabric
from fabric.api import sudo, run, env

env.user = "root"
env.key_filename = ["/root/.ssh/id_rsa"]
env.hosts = ['192.168.1.121']

ret = run("ls -la").return_code
