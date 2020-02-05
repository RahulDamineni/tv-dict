FROM mongo

# install python3 and pip
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN apt install python3-dev -y
RUN ln -s /usr/bin/python3 python
RUN pip3 install --upgrade pip

# for aiortc
# https://github.com/aiortc/aiortc#requirements
RUN apt install libavdevice-dev -y
RUN apt install libavfilter-dev -y
RUN apt install libopus-dev -y
RUN apt install libvpx-dev -y
RUN apt install pkg-config -y
# not listed but needed...
RUN apt install libopencv-dev -y

# for python backend
RUN pip install -r requirements.txt

# Defining working dir
WORKDIR /
