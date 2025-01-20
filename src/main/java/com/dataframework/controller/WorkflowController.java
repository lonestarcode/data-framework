package com.dataframework.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/workflows")
public class WorkflowController {
    private final WorkflowOrchestrator workflowOrchestrator;

    public WorkflowController(WorkflowOrchestrator workflowOrchestrator) {
        this.workflowOrchestrator = workflowOrchestrator;
    }

    @PostMapping("/orchestrate")
    public ResponseEntity<String> orchestrateWorkflow(@RequestBody Map<String, Object> data) {
        workflowOrchestrator.orchestrateDataFlow("default", data);
        return ResponseEntity.ok("Workflow orchestrated successfully");
    }
} 