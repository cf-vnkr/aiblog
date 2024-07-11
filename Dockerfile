FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY github_known_hosts ~/.ssh/known_hosts

RUN git config --add --local core.sshCommand 'ssh -i ./id_rsa -o UserKnownHostsFile=./github_known_hosts'
RUN git config user.email '78567009+cf-vnkr@users.noreply.github.com'
RUN git config user.name 'Alex'

CMD [ "python", "-u", "writer.py" ]
