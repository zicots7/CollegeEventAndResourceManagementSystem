package com.CollegeEventNotification;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.scheduling.annotation.EnableScheduling;

@SpringBootApplication
@EnableScheduling
public class CollegeEventNotificationApplication {

	public static void main(String[] args) {
		SpringApplication.run(CollegeEventNotificationApplication.class, args);

	}
}