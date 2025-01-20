package com.dataframework.service;

import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Service;
import java.util.Date;
import java.util.Map;

@Service
public class AutomatedWorkflowService {
    private final AutomatedWorkflowOrchestrator workflowOrchestrator;
    private final MonitoringService monitoringService;
    
    @Scheduled(fixedRate = 3600000) // Run every hour
    public void executeScheduledWorkflows() {
        monitoringService.trackMetrics("scheduled_workflow", Map.of(
            "timestamp", new Date()
        ));
        
        workflowOrchestrator.executeAutomatedTask(
            "scheduled_processing",
            Map.of("scheduled", true)
        );
    }
} 