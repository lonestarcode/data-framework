package ml;

import org.springframework.stereotype.Service;

import core.MonitoringService;
import core.PythonServiceOrchestrator;

import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class MLTrainingService {
    private final PythonServiceOrchestrator pythonService;
    private final MLModelService modelService;
    private final MonitoringService monitoringService;

    public CompletableFuture<ProcessResult> trainModel(String modelId, Map<String, Object> config) {
        // Validate training data
        // Configure training parameters
        // Execute training pipeline
        return pythonService.executePythonScript(
            "ml_analytics/models/training/train.py",
            Map.of("model_id", modelId, "config", JsonUtils.toJson(config)),
            true
        ).thenApply(result -> {
            modelService.updateModelStatus(modelId, "TRAINED", result.getMetrics());
            return result;
        });
    }

    public CompletableFuture<ProcessResult> evaluateModel(String modelId) {
        // Run model evaluation
        // Track performance metrics
        // Check for model drift
        return pythonService.executePythonScript(
            "ml_analytics/models/evaluation/evaluate.py",
            Map.of("model_id", modelId),
            true
        );
    }
} 