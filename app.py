import docker
import os
import tarfile
import time

client = docker.from_env()

# client.containers.run("ubuntu", "echo hello world")
container = client.containers.create("ubuntu", stdin_open=True)

# container.start()

def copy_to(src, dst):
  name, dst = dst.split(':')
  container = client.containers.get(name)

  os.chdir(os.path.dirname(src))
  srcname = os.path.basename(src)
  tar = tarfile.open(src + '.tar', mode='w')
  try:
    tar.add(srcname)
  finally:
    tar.close()

  data = open(src + '.tar', 'rb').read()
  container.put_archive(os.path.dirname(dst), data)

container.start()
time.sleep(1)

copy_to('./script.sh', f'{container.name}:/tmp/script.sh')

container.exec_run("chmod 755 ./script.sh", workdir="/tmp")
result = container.exec_run("./script.sh", workdir="/tmp")

print("Exit code:", result.exit_code)
print("Output:", result.output.decode('utf-8'))

container.stop()
container.remove()