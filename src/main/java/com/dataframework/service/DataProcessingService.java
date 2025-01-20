import org.springframework.stereotype.Service;
import com.dataframework.model.YourModel;

@Service
public class DataProcessingService {

    public YourModel validateAndTransformData(YourModel data) {
        // Perform validation
        if (data == null || data.getField() == null) {
            throw new IllegalArgumentException("Invalid data");
        }

        // Transform data if necessary
        data.setField(data.getField().trim().toUpperCase());

        return data;
    }
} 