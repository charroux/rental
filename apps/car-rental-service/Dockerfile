# Build stage
FROM gradle:9.8-jdk17@sha256:55af4a989cc9188c19668b32e52bbd2a0c801da3b849a6e8f5a25e2134845bf5 AS builder
WORKDIR /app
COPY . .
RUN gradle clean build -x test

# Runtime stage
FROM eclipse-temurin:17-jre-jammy@sha256:aa6381384f8db99762fa7d0d3c2b5de58874e5f12c96df4c13a1455376ae0ed1
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
