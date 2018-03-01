FROM centos:7
MAINTAINER SDE <darrell.emilien@afrinic.net>
EXPOSE 3000
COPY marvin/ /root/marvin/
COPY puppeteer/ /root/puppeteer/
COPY launcher.sh /root/
RUN yum install -y epel-release
RUN curl --silent --location https://rpm.nodesource.com/setup_8.x | bash -
RUN yum install -y nodejs chromium python34 python34-pip
RUN cd /root/marvin && \
pip3 install -r requirements.txt
RUN cd /root/puppeteer && \
npm install

RUN rm -rf /var/cache/yum /root/.npm

# Set environment variables. 
ENV HOME /root 
# Define working directory. 
WORKDIR /root
# Define default command. CMD ["bash"]
CMD ["bash","launcher.sh"] 
