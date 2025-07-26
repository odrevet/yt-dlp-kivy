# Build with:
# docker build -t buildozer .
#
# Call the utils script to build or sign:
#
# docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer /bin/bash -c "bash utils.sh --build"
#
# or build directly using buildozer
#
# docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer bash -c "yes | buildozer android release"
#
# To open a bash shell
#
# docker run -it --user root -v $(pwd):/root -v ~/.buildozer:/root/.buildozer buildozer

FROM ubuntu:22.04

RUN apt-get update && \
    apt-get install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

COPY requirements.txt .
RUN pip3 install -r requirements.txt

# add buildozer binary to path
RUN echo "export PATH=$PATH:~/.local/bin/" >> ~/.bashrc

WORKDIR /root
