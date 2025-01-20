package com.dataframework.controller;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.Map;

@RestController
@RequestMapping("/api/v1/data-collection")
public class DataCollectionController {
    private final DataCollectionOrchestrator dataCollectionOrchestrator;

    @PostMapping("/scrape")
    public ResponseEntity<String> initiateScraping(
        @RequestParam String sourceName,
        @RequestBody Map<String, Object> config
    ) {
        dataCollectionOrchestrator.executeScraping(sourceName, config);
        return ResponseEntity.ok("Scraping initiated");
    }
} 