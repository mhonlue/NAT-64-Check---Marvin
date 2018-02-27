FROM centos:7
MAINTAINER SDE <honlue@gmail.com>
EXPOSE 3000
ADD * /root/
RUN yum install -y epel-release
RUN yum install -y python34 python34-pip
RUN cd /root/ && \
pip3 install -r requirements.txt

# Set environment variables. 
ENV HOME /root 
# Define working directory. 
WORKDIR /root
# Define default command. CMD ["bash"]
#CMD ["/bin/systemctl","start","rpki-validator-3"] 
CMD ["/usr/bin/python3","main.py"] 
