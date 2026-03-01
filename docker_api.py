import docker
import os
import tarfile
import time
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class Docker:
  def __init__(self):
    self.client = docker.from_env()
    self.container = None

  def init_container(self):
    # self.client.con
    self.container = self.client.containers.create("ubuntu", stdin_open=True)

  def copy_to(self, src, dst):
    name, dst = dst.split(':')
    # container = self.client.containers.get(name)

    os.chdir(os.path.dirname(src))
    srcname = os.path.basename(src)
    tar = tarfile.open(src + '.tar', mode='w')
    try:
      tar.add(srcname)
    finally:
      tar.close()

    data = open(src + '.tar', 'rb').read()
    self.container.put_archive(os.path.dirname(dst), data)

  def start_container(self):
    self.container.start()

  
  def run_exec(self):
    self.container.exec_run("chmod 755 ./script.sh", workdir="/tmp")
    result = self.container.exec_run("./script.sh", workdir="/tmp")

  def prune(self):
    self.container.stop()
    self.container.remove()

  

  