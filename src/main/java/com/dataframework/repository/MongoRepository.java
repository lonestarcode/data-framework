import org.springframework.data.mongodb.repository.MongoRepository;
import com.dataframework.model.YourMongoModel;

public interface MongoRepository extends MongoRepository<YourMongoModel, String> {
    // Custom query methods if needed
} 