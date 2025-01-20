package com.dataframework.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/analytics")
public class AnalyticsController {
    private final AnalyticsOrchestrator analyticsOrchestrator;

    @PostMapping("/process")
    public ResponseEntity<String> processAnalytics(
        @RequestParam String pipelineId,
        @RequestBody Map<String, Object> config
    ) {
        analyticsOrchestrator.executeAnalytics(pipelineId, config);
        return ResponseEntity.ok("Analytics processing initiated");
    }
} 