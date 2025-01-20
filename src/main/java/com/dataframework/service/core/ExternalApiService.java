package com.dataframework.service.core;

import org.springframework.http.HttpEntity;
import org.springframework.http.HttpHeaders;
import org.springframework.http.HttpMethod;
import org.springframework.http.MediaType;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.Map;
import java.util.concurrent.CompletableFuture;

@Service
public class ExternalApiService {
    private final MonitoringService monitoringService;
    private final ConfigurationService configService;
    private final RestTemplate restTemplate;

    public ExternalApiService(
        MonitoringService monitoringService,
        ConfigurationService configService,
        RestTemplate restTemplate
    ) {
        this.monitoringService = monitoringService;
        this.configService = configService;
        this.restTemplate = restTemplate;
    }

    public <T> CompletableFuture<T> executeApiCall(
        String apiName,
        String endpoint,
        HttpMethod method,
        Object body,
        Class<T> responseType
    ) {
        Map<String, Object> apiConfig = configService.getApiConfig(apiName);
        String baseUrl = (String) apiConfig.get("baseUrl");
        
        monitoringService.trackMetrics("external_api_call", Map.of(
            "api", apiName,
            "endpoint", endpoint,
            "method", method
        ));

        return CompletableFuture.supplyAsync(() -> {
            try {
                HttpHeaders headers = createHeaders(apiConfig);
                HttpEntity<?> requestEntity = new HttpEntity<>(body, headers);
                
                ResponseEntity<T> response = restTemplate.exchange(
                    baseUrl + endpoint,
                    method,
                    requestEntity,
                    responseType
                );
                
                return response.getBody();
            } catch (Exception e) {
                monitoringService.trackMetrics("external_api_error", Map.of(
                    "api", apiName,
                    "error", e.getMessage()
                ));
                throw new ExternalApiException("API call failed: " + apiName, e);
            }
        });
    }

    private HttpHeaders createHeaders(Map<String, Object> apiConfig) {
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        
        if (apiConfig.containsKey("authToken")) {
            headers.setBearerAuth((String) apiConfig.get("authToken"));
        }
        
        return headers;
    }
} 