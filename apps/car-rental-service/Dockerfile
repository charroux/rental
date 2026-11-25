# Build stage
FROM gradle:8.14-jdk17@sha256:a9ead09d1462d8c4ae77554f63200a0088c687e2edb628071537bb84ceaf71fe AS builder
WORKDIR /app
COPY . .
RUN gradle clean build -x test

# Runtime stage
FROM eclipse-temurin:17-jre-jammy@sha256:aa6381384f8db99762fa7d0d3c2b5de58874e5f12c96df4c13a1455376ae0ed1
WORKDIR /app
COPY --from=builder /app/build/libs/*.jar app.jar

EXPOSE 8080

ENTRYPOINT ["java", "-jar", "app.jar"]
