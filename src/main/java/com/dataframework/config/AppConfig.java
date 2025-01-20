import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Configuration;

@Configuration
public class AppConfig {

    @Value("${python.script.path}")
    private String pythonScriptPath;

    @Value("${mongodb.uri}")
    private String mongoUri;

    @Value("${sql.datasource.url}")
    private String sqlDataSourceUrl;

    // Getters and setters
} 