FROM maven:3-eclipse-temurin-25-alpine AS build

WORKDIR /app

COPY . .

RUN mvn clean package -DskipTests

FROM eclipse-temurin:25-jre-alpine AS deploy

WORKDIR /app

COPY --from=build /app/target/*.jar CollegeEventNotification.jar


EXPOSE 9000


CMD ["java","-jar","CollegeEventNotification.jar"]