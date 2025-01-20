package com.dataframework.orchestration;

import org.springframework.stereotype.Service;

import core.DatabaseService;
import core.MonitoringService;
import core.PythonServiceOrchestrator;

import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class AnalyticsOrchestrator {
    private final PythonServiceOrchestrator pythonService;
    private final DatabaseService databaseService;
    private final MonitoringService monitoringService;
    
    public AnalyticsOrchestrator(PythonServiceOrchestrator pythonService, DatabaseService databaseService, MonitoringService monitoringService) {
        this.pythonService = pythonService;
        this.databaseService = databaseService;
        this.monitoringService = monitoringService;
    }

    public CompletableFuture<ProcessResult> executeAnalytics(String pipelineId, Map<String, Object> config) {
        monitoringService.trackMetrics("analytics_execution", Map.of("pipeline", pipelineId));
        
        return pythonService.executePythonScript(
            "applications/core_analytics/analyze.py",
            Map.of("pipeline", pipelineId, "config", JsonUtils.toJson(config)),
            true
        ).thenApply(result -> {
            databaseService.storeProcessedData("analytics_results", result.getData());
            return result;
        });
    }
} 