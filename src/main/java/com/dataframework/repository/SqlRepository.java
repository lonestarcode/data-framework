import org.springframework.data.jpa.repository.JpaRepository;
import com.dataframework.model.YourSqlModel;

public interface SqlRepository extends JpaRepository<YourSqlModel, Long> {
    // Custom query methods if needed
} 