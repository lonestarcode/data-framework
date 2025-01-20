package com.dataframework.orchestration;

import org.springframework.stereotype.Service;

import core.DatabaseService;
import core.MonitoringService;
import core.PythonServiceOrchestrator;

import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class AutomatedWorkflowOrchestrator {
    private final PythonServiceOrchestrator pythonService;
    private final DatabaseService databaseService;
    private final MonitoringService monitoringService;
    
    public AutomatedWorkflowOrchestrator(PythonServiceOrchestrator pythonService, DatabaseService databaseService, MonitoringService monitoringService) {
        this.pythonService = pythonService;
        this.databaseService = databaseService;
        this.monitoringService = monitoringService;
    }
    
    public CompletableFuture<ProcessResult> executeAutomatedTask(String taskType, Map<String, Object> config) {
        monitoringService.trackMetrics("automated_task", Map.of("type", taskType));
        
        return pythonService.executePythonScript(
            String.format("applications/workflows_automated/%s/execute.py", taskType),
            Map.of("config", JsonUtils.toJson(config)),
            true
        ).thenApply(result -> {
            databaseService.storeTaskResult("automated_tasks", result.getData());
            return result;
        });
    }
} 