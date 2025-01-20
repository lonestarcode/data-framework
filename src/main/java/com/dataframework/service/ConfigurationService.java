package com.dataframework.service;

import org.springframework.stereotype.Service;
import java.util.Map;

@Service
public class ConfigurationService {
    private final DatabaseService databaseService;
    
    public Map<String, Object> getWorkflowConfig(String workflowType) {
        return databaseService.fetchConfig("workflow_configs", workflowType);
    }
    
    public Map<String, Object> getPythonConfig(String scriptType) {
        return databaseService.fetchConfig("python_configs", scriptType);
    }
    
    public void updateConfig(String configType, String key, Map<String, Object> config) {
        databaseService.updateConfig(configType, key, config);
    }
} 