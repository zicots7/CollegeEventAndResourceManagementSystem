package com.CollegeEventNotification.Services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.mail.SimpleMailMessage;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.scheduling.TaskScheduler;
import org.springframework.stereotype.Service;
import java.time.LocalDateTime;
import java.time.Instant;
import java.time.ZoneId;
import java.util.Map;
import java.util.UUID;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ScheduledFuture;


@Service
public class EmailService {

    @Autowired
    private TaskScheduler taskScheduler;

    private final Map<String, ScheduledFuture<?>> scheduledTasks = new ConcurrentHashMap<>();
    @Autowired
    private JavaMailSender mailSender;

    public String scheduleEmail(String to , String subject, String body, LocalDateTime sendTime ){
       final String taskID = UUID.randomUUID().toString();
        Instant instant = sendTime.atZone(ZoneId.of("Asia/Kolkata")).toInstant();
       ScheduledFuture<?> scheduleTask= taskScheduler.schedule(()->{
            try{
                SimpleMailMessage message = new SimpleMailMessage();
                message.setTo(to);
                message.setSubject(subject);
                message.setText(body);
                mailSender.send(message);
                scheduledTasks.remove(taskID);
            }catch (Exception e){
                System.out.println(e);
            }
            },instant);
        scheduledTasks.put(taskID,scheduleTask);
        return taskID;
    }
public boolean cancelEmail(String taskID){
        ScheduledFuture<?> task = scheduledTasks.get(taskID);
        if(task!=null){
            boolean cancel = task.cancel(false);
            if (cancel){
                scheduledTasks.remove(taskID);
                return true;

            }
        }
        return false;
}
}
