FROM maven:3-eclipse-temurin-25-alpine AS build

WORKDIR /home/app/CollegeEventNotification

COPY . .

RUN mvn clean package -DskipTests

FROM eclipse-temurin:25-jre-alpine AS deploy

WORKDIR /home/app/CollegeEventNotification/build

COPY --from=build /home/app/CollegeEventNotification/target/*.jar ./CollegeEventNotification.jar


EXPOSE 9000


CMD ["java","-jar","CollegeEventNotification.jar"]