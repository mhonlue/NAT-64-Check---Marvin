FROM centos:7
MAINTAINER SDE <darrell.emilien@afrinic.net>
EXPOSE 3001
ADD * /root/
RUN yum install -y epel-release
RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
RUN yum install -y nodejs chromium
RUN cd /root/ && \
npm install

RUN rm -rf /var/cache/yum /root/.npm

# Set environment variables. 
ENV HOME /root 
# Define working directory. 
WORKDIR /root
# Define default command. CMD ["bash"]
CMD ["/bin/node","main.js"] 
