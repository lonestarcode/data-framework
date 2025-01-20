package com.dataframework.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import ml.MLModelService;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/ml")
public class MLController {
    private final MLOrchestrator mlOrchestrator;
    private final MLModelService modelService;

    @PostMapping("/train")
    public ResponseEntity<String> trainModel(
        @RequestParam String modelId,
        @RequestBody Map<String, Object> config
    ) {
        mlOrchestrator.orchestrateTraining(modelId, config);
        return ResponseEntity.ok("ML training initiated");
    }

    @GetMapping("/models/{modelId}")
    public ResponseEntity<Map<String, Object>> getModelStatus(@PathVariable String modelId) {
        return ResponseEntity.ok(modelService.getModelStatus(modelId));
    }
} 