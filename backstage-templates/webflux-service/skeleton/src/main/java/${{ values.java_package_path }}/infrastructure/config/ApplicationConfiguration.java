package ${{ values.java_package_name }}.infrastructure.config;

import ${{ values.java_package_name }}.domain.ports.input.UserUseCase;
import ${{ values.java_package_name }}.domain.ports.output.UserRepositoryPort;
import ${{ values.java_package_name }}.application.service.UserService;
import ${{ values.java_package_name }}.application.mapper.UserMapper;
import ${{ values.java_package_name }}.infrastructure.adapters.output.persistence.adapter.UserRepositoryAdapter;
import ${{ values.java_package_name }}.infrastructure.adapters.output.persistence.repository.JpaUserRepository;
import ${{ values.java_package_name }}.domain.ports.input.LocationUseCase;
import ${{ values.java_package_name }}.domain.ports.output.LocationRepositoryPort;
import ${{ values.java_package_name }}.application.service.LocationService;
import ${{ values.java_package_name }}.application.mapper.LocationMapper;
import ${{ values.java_package_name }}.infrastructure.adapters.output.persistence.adapter.LocationRepositoryAdapter;
import ${{ values.java_package_name }}.infrastructure.adapters.output.persistence.repository.JpaLocationRepository;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Import;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

/**
 * Spring configuration class for application beans.
 * <p>
 * This configuration class defines beans required by the application,
 * including security components like password encoders and MapStruct mappers.
 * It serves as the infrastructure configuration in Clean Architecture.
 * </p>
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
@Configuration
@Import({OpenApiConfiguration.class})
public class ApplicationConfiguration {

    /**
     * Configures the password encoder bean for security operations.
     * 
     * @return BCryptPasswordEncoder instance for password hashing
     */
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder();
    }


}