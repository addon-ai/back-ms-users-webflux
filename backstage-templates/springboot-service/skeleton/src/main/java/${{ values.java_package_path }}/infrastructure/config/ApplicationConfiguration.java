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

    /**
     * Configures the User use case implementation.
     * 
     * @param userRepositoryPort the repository port
     * @param userMapper the mapper
     * @return UserUseCase implementation
     */
    @Bean
    public UserUseCase userUseCase(UserRepositoryPort userRepositoryPort, UserMapper userMapper) {
        return new UserService(userRepositoryPort, userMapper);
    }

    /**
     * Configures the User repository port implementation.
     * 
     * @param jpaUserRepository the JPA repository
     * @param userMapper the mapper
     * @return UserRepositoryPort implementation
     */
    @Bean
    public UserRepositoryPort userRepositoryPort(JpaUserRepository jpaUserRepository, UserMapper userMapper) {
        return new UserRepositoryAdapter(jpaUserRepository, userMapper);
    }

    /**
     * Configures the Location use case implementation.
     * 
     * @param locationRepositoryPort the repository port
     * @param locationMapper the mapper
     * @return LocationUseCase implementation
     */
    @Bean
    public LocationUseCase locationUseCase(LocationRepositoryPort locationRepositoryPort, LocationMapper locationMapper) {
        return new LocationService(locationRepositoryPort, locationMapper);
    }

    /**
     * Configures the Location repository port implementation.
     * 
     * @param jpaLocationRepository the JPA repository
     * @param locationMapper the mapper
     * @return LocationRepositoryPort implementation
     */
    @Bean
    public LocationRepositoryPort locationRepositoryPort(JpaLocationRepository jpaLocationRepository, LocationMapper locationMapper) {
        return new LocationRepositoryAdapter(jpaLocationRepository, locationMapper);
    }

}