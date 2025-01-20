package com.dataframework.orchestration;

import org.springframework.stereotype.Service;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import com.dataframework.service.MLTrainingService;
import com.dataframework.service.MLModelService;
import com.dataframework.service.MonitoringService;
import com.dataframework.model.ProcessResult;

@Service
public class MLOrchestrator {
    private final MLTrainingService trainingService;
    private final MLModelService modelService;
    private final MonitoringService monitoringService;

    public CompletableFuture<ProcessResult> orchestrateTraining(String modelId, Map<String, Object> config) {
        // Register model
        modelService.registerModel(modelId, config);
        
        // Execute training pipeline
        return trainingService.trainModel(modelId, config)
            .thenCompose(result -> trainingService.evaluateModel(modelId))
            .thenApply(result -> {
                if (result.getMetrics().get("accuracy") > 0.85) {
                    modelService.deployModel(modelId, "production");
                }
                return result;
            });
    }

    public CompletableFuture<ProcessResult> retrainModel(String modelId) {
        // Handle model retraining
        // Validate current model status
        // Execute retraining pipeline
        return orchestrateTraining(modelId, Map.of("retrain", true));
    }
} 