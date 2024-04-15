FROM maven as builder

# Download requirements to interact with object storage
RUN cat > /tmp/pom.xml <<EOF
<project>
  <modelVersion>4.0.0</modelVersion>

  <groupId>eu.glaciation-project.mondrian</groupId>
  <artifactId>object-storage-deps</artifactId>
  <version>1</version>
  <dependencies>
    <dependency>
      <groupId>org.apache.hadoop</groupId>
      <artifactId>hadoop-aws</artifactId>
      <version>3.3.4</version>
    </dependency>
    <dependency>
      <groupId>org.apache.spark</groupId>
      <artifactId>spark-hadoop-cloud_2.13</artifactId>
      <version>3.3.4</version>
    </dependency>
  </dependencies>
</project>
EOF
RUN mvn dependency:copy-dependencies -f /tmp/pom.xml -DoutputDirectory=/tmp/jars/

FROM apache/spark-py:v3.4.0
# FROM apache/spark:3.5.0-python3

# Install requirements to interact with object storage
COPY --from=builder /tmp/jars/ /opt/spark/jars/

USER root

# Install application requirements
COPY spark-app/distributed/spark/requirements.txt /tmp/
RUN ["pip", "install", "--upgrade", "pip"]
RUN ["pip", "install", "--requirement", "/tmp/requirements.txt"]

# Import application
RUN mkdir "/mondrian"
COPY spark-app/distributed/anonymize.py /mondrian/
COPY spark-app/distributed/mondrian.zip /mondrian/

# Run with an unprivileged user
USER 185
