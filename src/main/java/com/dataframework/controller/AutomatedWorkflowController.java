package com.dataframework.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/automated")
public class AutomatedWorkflowController {
    private final AutomatedWorkflowOrchestrator automatedWorkflowOrchestrator;

    @PostMapping("/execute")
    public ResponseEntity<String> executeWorkflow(
        @RequestParam String taskType,
        @RequestBody Map<String, Object> config
    ) {
        automatedWorkflowOrchestrator.executeAutomatedTask(taskType, config);
        return ResponseEntity.ok("Automated workflow initiated");
    }
} 