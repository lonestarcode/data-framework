package core;

import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Map;
import java.util.concurrent.CompletableFuture;
import java.util.stream.Collectors;

@Service
public class PythonServiceOrchestrator {
    private final ProcessBuilder processBuilder;
    private final MonitoringService monitoringService;

    public CompletableFuture<ProcessResult> executePythonScript(
        String scriptPath, 
        Map<String, String> params,
        boolean trackMetrics
    ) {
        if (trackMetrics) {
            monitoringService.trackMetrics("python_execution", Map.of(
                "script", scriptPath,
                "params", params
            ));
        }
        return CompletableFuture.supplyAsync(() -> {
            try {
                List<String> command = new ArrayList<>();
                command.add("python");
                command.add(scriptPath);
                params.forEach((key, value) -> {
                    command.add("--" + key);
                    command.add(value);
                });

                ProcessBuilder processBuilder = new ProcessBuilder(command);
                Process process = processBuilder.start();
                int exitCode = process.waitFor();

                if (exitCode == 0) {
                    String result = new BufferedReader(new InputStreamReader(process.getInputStream()))
                            .lines().collect(Collectors.joining("\n"));
                    return new ProcessResult(result, null);
                } else {
                    String error = new BufferedReader(new InputStreamReader(process.getErrorStream()))
                            .lines().collect(Collectors.joining("\n"));
                    return new ProcessResult(null, error);
                }
            } catch (Exception e) {
                return new ProcessResult(null, e.getMessage());
            }
        });
    }
} 