FROM ubuntu:25.04
LABEL org.opencontainers.image.authors="bkryza@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt -y update && apt -y install \
       cmake curl wget git vim clang-19  build-essential ninja-build jq \
       pkg-config plantuml nodejs npm software-properties-common python3 \
       python3-pip python3-yaml python3-networkx \
       libpsl-dev libssl-dev gperf libxdamage-dev libxkbcommon-dev && \
    apt clean

#
# Update PlantUML plantuml.jar to 2025.0
#
RUN wget https://github.com/plantuml/plantuml/releases/download/v1.2025.0/plantuml.jar -O /usr/share/plantuml/plantuml.jar


#
# Install clang-include-graph
#
RUN add-apt-repository ppa:bkryza/clang-include-graph && \
    apt -y update && \
    apt -y install clang-include-graph && \
    apt clean

ADD main.sh /
RUN chmod +x /main.sh


ADD calculate_statistics.py /
RUN chmod +x /calculate_statistics.py

ADD annotate_include_graph.py /
RUN chmod +x /annotate_include_graph.py

VOLUME "/build"
WORKDIR "/build"

ENV PATH="/build/depot_tools:$PATH"

ENTRYPOINT ["/main.sh"]
CMD ["usage"]
