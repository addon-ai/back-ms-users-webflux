package ${{ values.java_package_name }}.application.mapper;

import ${{ values.java_package_name }}.domain.model.Region;
import ${{ values.java_package_name }}.domain.model.EntityStatus;
import ${{ values.java_package_name }}.infrastructure.adapters.output.persistence.entity.RegionDbo;
import ${{ values.java_package_name }}.application.dto.location.RegionResponse;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mapstruct.factory.Mappers;

import java.util.Arrays;
import java.util.List;

import static org.assertj.core.api.Assertions.assertThat;

/**
 * Unit tests for RegionMapper.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
class RegionMapperTest {

    private RegionMapper mapper;

    @BeforeEach
    void setUp() {
        mapper = Mappers.getMapper(RegionMapper.class);
    }




    @Test
    void toDbo_ShouldMapCorrectly_FromDomain() {
        // Given
        Region domain = Region.builder()
            .build();

        // When
        RegionDbo result = mapper.toDbo(domain);

        // Then
        assertThat(result).isNotNull();
    }

    @Test
    void toDbo_ShouldMapCorrectly_WithStatus() {
        // Given
        Region domain = Region.builder()
            .status("ACTIVE")
            .build();

        // When
        RegionDbo result = mapper.toDbo(domain);

        // Then
        assertThat(result).isNotNull();
        assertThat(result.getStatus()).isEqualTo(EntityStatus.ACTIVE);
    }

    @Test
    void toDomain_ShouldMapCorrectly_FromDbo() {
        // Given
        RegionDbo dbo = RegionDbo.builder()
            .build();

        // When
        Region result = mapper.toDomain(dbo);

        // Then
        assertThat(result).isNotNull();
    }

    @Test
    void toDomainList_ShouldMapCorrectly_FromDboList() {
        // Given
        RegionDbo dbo = RegionDbo.builder().build();
        List<RegionDbo> dboList = Arrays.asList(dbo);

        // When
        List<Region> result = mapper.toDomainList(dboList);

        // Then
        assertThat(result).isNotNull().hasSize(1);
    }

    @Test
    void toDboList_ShouldMapCorrectly_FromDomainList() {
        // Given
        Region domain = Region.builder().build();
        List<Region> domainList = Arrays.asList(domain);

        // When
        List<RegionDbo> result = mapper.toDboList(domainList);

        // Then
        assertThat(result).isNotNull().hasSize(1);
    }


    @Test
    void toDto_ShouldMapCorrectly_FromDomain() {
        // Given
        Region domain = Region.builder().build();

        // When
        RegionResponse result = mapper.toDto(domain);

        // Then
        assertThat(result).isNotNull();
    }

    @Test
    void toDtoList_ShouldMapCorrectly_FromDomainList() {
        // Given
        Region domain = Region.builder().build();
        List<Region> domainList = Arrays.asList(domain);

        // When
        List<RegionResponse> result = mapper.toDtoList(domainList);

        // Then
        assertThat(result).isNotNull().hasSize(1);
    }

    // Null parameter coverage tests


    @Test
    void toDto_ShouldReturnNull_WhenDomainIsNull() {
        // When
        RegionResponse result = mapper.toDto(null);

        // Then
        assertThat(result).isNull();
    }

    @Test
    void toDtoList_ShouldReturnNull_WhenDomainsIsNull() {
        // When
        List<RegionResponse> result = mapper.toDtoList(null);

        // Then
        assertThat(result).isNull();
    }

    @Test
    void toDomain_ShouldReturnNull_WhenDboIsNull() {
        // When
        Region result = mapper.toDomain(null);

        // Then
        assertThat(result).isNull();
    }

    @Test
    void toDbo_ShouldReturnNull_WhenDomainIsNull() {
        // When
        RegionDbo result = mapper.toDbo(null);

        // Then
        assertThat(result).isNull();
    }

    @Test
    void toDomainList_ShouldReturnNull_WhenDboListIsNull() {
        // When
        List<Region> result = mapper.toDomainList(null);

        // Then
        assertThat(result).isNull();
    }

    @Test
    void toDboList_ShouldReturnNull_WhenDomainListIsNull() {
        // When
        List<RegionDbo> result = mapper.toDboList(null);

        // Then
        assertThat(result).isNull();
    }


}