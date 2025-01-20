package com.dataframework.orchestration;

import org.springframework.stereotype.Service;

import core.DatabaseService;
import core.MonitoringService;
import core.PythonServiceOrchestrator;

import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class DataCollectionOrchestrator {
    private final PythonServiceOrchestrator pythonService;
    private final DatabaseService databaseService;
    private final MonitoringService monitoringService;
    
    public CompletableFuture<ProcessResult> executeScraping(String sourceName, Map<String, Object> config) {
        monitoringService.trackMetrics("scraping_execution", Map.of("source", sourceName));
        
        return pythonService.executePythonScript(
            "applications/core_scraping/scrape.py",
            Map.of("source", sourceName, "config", JsonUtils.toJson(config)),
            true
        ).thenApply(result -> {
            databaseService.storeRawData("scraped_data", result.getData());
            return result;
        });
    }
} 