FROM ubuntu:14.04

MAINTAINER Artyom Zaytsev <artyomzaytsev@yandex.ru>

ENV DEBIAN_FRONTEND noninteractive

VOLUME /project/data
WORKDIR /project

RUN apt-get -yq update && apt-get -yq install gcc curl wget supervisor python-pip git tar python3.4 openjdk-7-jre-headless ant && apt-get clean
RUN mkdir -p /var/log/supervisor
RUN pip install pyorient
RUN pip install tornado

#ENV ORIENTDB_VERSION orientdb-community-2.0.13 
#ENV ORIENTDB_URL http://www.orientechnologies.com/download.php?email=unknown@unknown.com&file=${ORIENTDB_VERSION}.tar.gz&os=linux
ENV ORIENTDB_URL http://orientdb.com/download.php?email=unknown@unknown.com&file=orientdb-community-2.1.0.tar.gz&os=multi
ENV ORIENTDB_ROOT_PASSWORD 0r13ntDB 

ADD ${ORIENTDB_URL} /usr/local/src/orientdb-community.tar.gz

RUN cd /usr/local/src \
    && tar -xzf orientdb-community.tar.gz \
    && ln -s ${PWD}/${ORIENTDB_VERSION} ${PWD}/orientdb \
    && ln -s ${PWD}/orientdb/bin/* /usr/local/bin/ \
    && rm ${PWD}/orientdb-community.tar.gz \
    && mkdir /usr/local/log

VOLUME ["/project"] 
ADD hello.py /project/hello.py
ADD hello.py /project/test_create.py 

EXPOSE 2424 
EXPOSE 2480
EXPOSE 3000 

CMD ["cd", "/usr/local/src/orientdb-community-2.1.0/bin/"]
CMD ["sh", "server.sh"]
CMD ["python", "/project/test_create.py"]
CMD ["python", "/project/hello.py"]


