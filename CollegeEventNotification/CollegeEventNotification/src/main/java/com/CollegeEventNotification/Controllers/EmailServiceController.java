package com.CollegeEventNotification.Controllers;
import com.CollegeEventNotification.Services.EmailService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import java.time.LocalDateTime;
import java.util.HashMap;
import java.util.Map;

@RestController
@RequestMapping("/mail")
public class EmailServiceController {
    private final EmailService emailService;

    @Autowired
    public EmailServiceController(EmailService emailService) {
        this.emailService = emailService;
    }
    @PostMapping("/schedule")
    public ResponseEntity Schedule(
            @RequestParam String to,
            @RequestParam String body,
            @RequestParam String subject,
            @RequestParam @DateTimeFormat(iso= DateTimeFormat.ISO.DATE_TIME)LocalDateTime time){
        String taskID=emailService.scheduleEmail(to,subject,body,time);
        Map<String, String> response = new HashMap<>();
        response.put("taskID", taskID);
        response.put("message", "Email scheduled successfully");

        return ResponseEntity.ok(response);
    }
 @PostMapping("/cancel")
    public String cancel(@RequestParam String taskID){
        boolean isCancelled = emailService.cancelEmail(taskID);
        if(isCancelled){
            return "Scheduled email successfully cancelled";
        }
        else{
            return "cannot find any scheduled email";
        }

 }
}
