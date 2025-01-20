import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;
import com.dataframework.model.ExternalApiResponse;

@Service
public class ExternalApiService {
    private final RestTemplate restTemplate;

    public ExternalApiService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
    }

    public ExternalApiResponse fetchDataFromApi(String apiUrl) {
        return restTemplate.getForObject(apiUrl, ExternalApiResponse.class);
    }
} 