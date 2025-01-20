package com.dataframework.service;

import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Service;

import java.util.Date;
import java.util.List;
import java.util.Map;

import org.bson.Document;

@Service
public class MonitoringService {
    private final MongoTemplate mongoTemplate;
    private final DatabaseService databaseService;
    
    public void trackMetrics(String component, Map<String, Object> metrics) {
        Document doc = new Document()
            .append("component", component)
            .append("metrics", metrics)
            .append("timestamp", new Date());
        databaseService.storeMetrics("system_metrics", doc);
    }
    
    public void logEvent(String eventType, Map<String, Object> eventData) {
        Document doc = new Document()
            .append("type", eventType)
            .append("data", eventData)
            .append("timestamp", new Date());
        databaseService.storeEvent("system_events", doc);
    }
    
    public List<Document> getMetrics(String component, Date startTime, Date endTime) {
        return databaseService.fetchMetrics(component, startTime, endTime);
    }
} 