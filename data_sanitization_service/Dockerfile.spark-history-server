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
  </dependencies>
</project>
EOF
RUN mvn dependency:copy-dependencies -f /tmp/pom.xml -DoutputDirectory=/tmp/jars/

FROM apache/spark:3.4.0

# Install requirements to interact with object storage
COPY --from=builder /tmp/jars/ /opt/spark/jars/

# Run with an unprivileged user
USER 185
