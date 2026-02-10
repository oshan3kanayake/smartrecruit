package com.recruitment.app.service;

import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import java.util.HashMap;
import java.util.Map;

@Service
public class ChatbotService {

    private final RestTemplate restTemplate = new RestTemplate();

    // CHANGE THIS if you are using a different model (e.g., "mistral", "gemma")
    private static final String OLLAMA_MODEL = "llama3";
    private static final String OLLAMA_URL = "http://localhost:11434/api/generate";

    public String getResponse(String userMessage) {
        try {
            // 1. Create the JSON Request Payload for Ollama
            Map<String, Object> requestBody = new HashMap<>();
            requestBody.put("model", OLLAMA_MODEL);
            requestBody.put("prompt", "You are a helpful recruitment assistant. Answer this briefly: " + userMessage);
            requestBody.put("stream", false); // Important: Turn off streaming for simple Java handling

            // 2. Send Request to Local Ollama
            Map<String, Object> response = restTemplate.postForObject(OLLAMA_URL, requestBody, Map.class);

            // 3. Extract the "response" text from the JSON
            if (response != null && response.containsKey("response")) {
                return response.get("response").toString();
            }

            return "Ollama did not return a response.";

        } catch (Exception e) {
            e.printStackTrace();
            return "Error connecting to AI: Is Ollama running? (Try 'ollama run llama3' in terminal)";
        }
    }
}