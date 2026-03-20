# Dockerfile for Rare Disease Knowledge Graph (RDKG)
# Based on Blazegraph 2.1.6 with RDKG data pre-loaded

FROM openjdk:11-jre-slim

LABEL maintainer="UTHealth SBMI <jinlian.wang@uth.tmc.edu>"
LABEL description="Rare Disease Knowledge Graph - Blazegraph RDF Triplestore"
LABEL version="1.0.0"

# Set environment variables
ENV BLAZEGRAPH_VERSION=2.1.6 \
    BLAZEGRAPH_HOME=/opt/blazegraph \
    BLAZEGRAPH_DATA=/var/lib/blazegraph \
    JAVA_OPTS="-Xmx4g -Xms2g" \
    BLAZEGRAPH_PORT=9999

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create directories
RUN mkdir -p ${BLAZEGRAPH_HOME} ${BLAZEGRAPH_DATA}

# Download Blazegraph
WORKDIR ${BLAZEGRAPH_HOME}
RUN wget -q https://github.com/blazegraph/database/releases/download/BLAZEGRAPH_2_1_6_RC/blazegraph.jar \
    && chmod +x blazegraph.jar

# Copy configuration files
COPY blazegraph.properties ${BLAZEGRAPH_HOME}/
COPY RWStore.properties ${BLAZEGRAPH_HOME}/

# Copy RDKG data (if pre-loading)
# Uncomment if you want to include data in the image
# COPY ../data/rdkg_complete.ttl ${BLAZEGRAPH_DATA}/
# COPY load_data.sh ${BLAZEGRAPH_HOME}/

# Expose Blazegraph port
EXPOSE ${BLAZEGRAPH_PORT}

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:${BLAZEGRAPH_PORT}/blazegraph/status || exit 1

# Volume for persistent data
VOLUME ["${BLAZEGRAPH_DATA}"]

# Set working directory
WORKDIR ${BLAZEGRAPH_HOME}

# Start Blazegraph
CMD ["sh", "-c", "java ${JAVA_OPTS} -jar blazegraph.jar"]
