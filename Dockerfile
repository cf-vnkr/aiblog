FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN git config --add --local core.sshCommand 'ssh -i ./id_rsa'

CMD [ "python", "./writer`.py" ]