FROM ubuntu
MAINTAINER Alex Soto <asotobueno@cloudbees.com>

EXPOSE 5000

# Install wget and unzip
RUN apt-get update --yes \
  && apt-get install --yes \
    curl         \
    unzip        \
    python3      \
    python3-pip  \
    python3-dev  \
    wget          \
    vim

# Install Packer

ENV PACKER_BIN_DIR /usr/local
RUN mkdir --parents $PACKER_BIN_DIR

ENV PACKER_ZIP https://releases.hashicorp.com/packer/1.5.4/packer_1.5.4_linux_amd64.zip
RUN curl -sSLo /tmp/packer.zip $PACKER_ZIP && \
  mkdir -p $PACKER_BIN_DIR && \
  unzip /tmp/packer.zip -d $PACKER_BIN_DIR && \
  rm /tmp/packer.zip
RUN curl -sSLo ~/packer-builder-vsphere-clone.linux https://github.com/jetbrains-infra/packer-builder-vsphere/releases/download/v2.3/packer-builder-vsphere-clone.linux && \
  curl -sSLo ~/packer-builder-vsphere-iso.linux https://github.com/jetbrains-infra/packer-builder-vsphere/releases/download/v2.3/packer-builder-vsphere-iso.linux; \
  mv ~/packer-builder-vsphere-clone.linux $PACKER_BIN_DIR/packer-vsphere-clone; mv ~/packer-builder-vsphere-iso.linux $PACKER_BIN_DIR/packer-vsphere-iso; \
  cp $PACKER_BIN_DIR/packer-vsphere-clone $PACKER_BIN_DIR/vsphere-clone ; cp $PACKER_BIN_DIR/packer-vsphere-iso $PACKER_BIN_DIR/vsphere-iso

ENV PATH $PATH:$PACKER_BIN_DIR

# check that packer is correctly installed
RUN type packer


WORKDIR /flask
COPY requirements.txt /flask
RUN pip3 install -r requirements.txt

COPY app.py /flask
COPY . /flask
CMD python3 app.py

