# Build stage
FROM gradle:8.14-jdk17@sha256:a9ead09d1462d8c4ae77554f63200a0088c687e2edb628071537bb84ceaf71fe AS builder
WORKDIR /app
COPY . .
RUN gradle clean build -x test

# Runtime stage
FROM eclipse-temurin:22-jre-jammy@sha256:dbcae8b5dd4d63f81739a538ec2c09797735f04a21d814f9071b62f018326043
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
