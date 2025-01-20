import org.springframework.stereotype.Service;
import com.dataframework.model.YourModel;

@Service
public class BusinessLogicService {

    public double calculateMetric(YourModel data) {
        // Example business logic
        return data.getValue1() * data.getValue2();
    }
} 