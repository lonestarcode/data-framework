@Configuration
@ConfigurationProperties(prefix = "workflow")
public class WorkflowConfig {
    private Map<String, String> scriptPaths;
    private Map<String, Integer> timeouts;
    
    // Getters and setters
} 