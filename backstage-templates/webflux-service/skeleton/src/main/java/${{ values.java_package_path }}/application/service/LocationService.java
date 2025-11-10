package ${{ values.java_package_name }}.application.service;

import ${{ values.java_package_name }}.domain.ports.input.LocationUseCase;
import ${{ values.java_package_name }}.domain.ports.output.LocationRepositoryPort;
import ${{ values.java_package_name }}.application.dto.location.CreateLocationRequestContent;
import ${{ values.java_package_name }}.application.dto.location.CreateLocationResponseContent;
import ${{ values.java_package_name }}.application.dto.location.GetLocationResponseContent;
import ${{ values.java_package_name }}.application.dto.location.UpdateLocationRequestContent;
import ${{ values.java_package_name }}.application.dto.location.UpdateLocationResponseContent;
import ${{ values.java_package_name }}.application.dto.location.DeleteLocationResponseContent;
import ${{ values.java_package_name }}.application.dto.location.ListLocationsResponseContent;
import ${{ values.java_package_name }}.application.dto.location.GetNeighborhoodsByCityResponseContent;
import ${{ values.java_package_name }}.application.dto.location.GetRegionsByCountryResponseContent;
import ${{ values.java_package_name }}.application.dto.location.GetCitiesByRegionResponseContent;
import ${{ values.java_package_name }}.domain.model.Location;
import ${{ values.java_package_name }}.application.mapper.LocationMapper;
import ${{ values.java_package_name }}.infrastructure.config.exceptions.NotFoundException;
import ${{ values.java_package_name }}.utils.LoggingUtils;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

/**
 * Consolidated application service implementing all Location use cases.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
@Service
@RequiredArgsConstructor
public class LocationService implements LocationUseCase {

    private static final LoggingUtils logger = LoggingUtils.getLogger(LocationService.class);
    
    private final LocationRepositoryPort locationRepositoryPort;
    private final LocationMapper locationMapper;

    @Override
    public Mono<CreateLocationResponseContent> create(CreateLocationRequestContent request) {
        logger.info("Executing CreateLocation with request: {}", request);
        
        return Mono.fromCallable(() -> locationMapper.fromCreateRequest(request))
                .flatMap(locationRepositoryPort::save)
                .map(savedLocation -> {
                    logger.info("Location created successfully with ID: {}", savedLocation.getLocationId());
                    return locationMapper.toCreateResponse(savedLocation);
                })
                .doOnError(e -> logger.error("Error in CreateLocation", e, request));
    }

    @Override
    public Mono<GetLocationResponseContent> get(String locationId) {
        logger.info("Executing GetLocation with locationId: {}", locationId);
        
        return locationRepositoryPort.findById(locationId)
                .switchIfEmpty(Mono.error(new NotFoundException("Location not found")))
                .map(location -> {
                    logger.info("Location retrieved successfully with ID: {}", locationId);
                    return locationMapper.toGetResponse(location);
                })
                .doOnError(e -> logger.error("Error in GetLocation", e, locationId));
    }

    @Override
    public Mono<UpdateLocationResponseContent> update(String locationId, UpdateLocationRequestContent request) {
        logger.info("Executing UpdateLocation with locationId: {} and request: {}", locationId, request);
        
        return locationRepositoryPort.findById(locationId)
                .switchIfEmpty(Mono.error(new NotFoundException("Location not found")))
                .map(existingLocation -> {
                    locationMapper.updateEntityFromRequest(request, existingLocation);
                    existingLocation.setUpdatedAt(java.time.Instant.now().toString());
                    return existingLocation;
                })
                .flatMap(locationRepositoryPort::save)
                .map(savedLocation -> {
                    logger.info("Location updated successfully with ID: {}", locationId);
                    return locationMapper.toUpdateResponse(savedLocation);
                })
                .doOnError(e -> logger.error("Error in UpdateLocation", e, locationId));
    }

    @Override
    public Mono<DeleteLocationResponseContent> delete(String locationId) {
        logger.info("Executing DeleteLocation with locationId: {}", locationId);
        
        return locationRepositoryPort.findById(locationId)
                .switchIfEmpty(Mono.error(new NotFoundException("Location not found")))
                .map(location -> {
                    // Soft delete: update status to INACTIVE and set updatedAt
                    location.setStatus("INACTIVE");
                    location.setUpdatedAt(java.time.Instant.now().toString());
                    return location;
                })
                .flatMap(locationRepositoryPort::save)
                .map(updatedLocation -> {
                    logger.info("Location soft deleted (status set to INACTIVE) with ID: {}", locationId);
                    return DeleteLocationResponseContent.builder()
                            .deleted(true)
                            .message("Location deleted successfully")
                            .build();
                })
                .doOnError(e -> logger.error("Error in DeleteLocation", e, locationId));
    }

    @Override
    public Mono<ListLocationsResponseContent> list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo) {
        // Apply default values
        String effectiveStatus = (status == null || status.trim().isEmpty()) ? "ACTIVE" : status;
        String effectiveDateFrom = (dateFrom == null || dateFrom.trim().isEmpty()) ? 
            java.time.Instant.now().minus(30, java.time.temporal.ChronoUnit.DAYS).toString() : dateFrom;
        String effectiveDateTo = (dateTo == null || dateTo.trim().isEmpty()) ? 
            java.time.Instant.now().toString() : dateTo;
        
        logger.info("Executing ListLocations with page: {}, size: {}, search: {}, status: {} (effective: {}), dateFrom: {} (effective: {}), dateTo: {} (effective: {})", 
                   page, size, search, status, effectiveStatus, dateFrom, effectiveDateFrom, dateTo, effectiveDateTo);
        
        return locationRepositoryPort.findByFilters(search, effectiveStatus, effectiveDateFrom, effectiveDateTo, page, size)
                .collectList()
                .map(locations -> {
                    logger.info("Retrieved {} locations successfully", locations.size());
                    int pageNum = page != null ? page : 1;
                    int pageSize = size != null ? size : 20;
                    return locationMapper.toListResponse(locations, pageNum, pageSize);
                })
                .doOnError(e -> logger.error("Error in ListLocations", e));
    }

    @Override
    public Mono<GetNeighborhoodsByCityResponseContent> getNeighborhoodsByCity(String cityId) {
        logger.info("Executing GetNeighborhoodsByCity with cityId: {}", cityId);
        
        return locationRepositoryPort.findNeighborhoodsByCity(cityId)
                .collectList()
                .map(locations -> {
                    logger.info("Retrieved {} locations successfully", locations.size());
                    return GetNeighborhoodsByCityResponseContent.builder().build();
                })
                .doOnError(e -> logger.error("Error in GetNeighborhoodsByCity", e, cityId));
    }

    @Override
    public Mono<GetRegionsByCountryResponseContent> getRegionsByCountry(String countryId) {
        logger.info("Executing GetRegionsByCountry with countryId: {}", countryId);
        
        return locationRepositoryPort.findRegionsByCountry(countryId)
                .collectList()
                .map(locations -> {
                    logger.info("Retrieved {} locations successfully", locations.size());
                    return GetRegionsByCountryResponseContent.builder().build();
                })
                .doOnError(e -> logger.error("Error in GetRegionsByCountry", e, countryId));
    }

    @Override
    public Mono<GetCitiesByRegionResponseContent> getCitiesByRegion(String regionId) {
        logger.info("Executing GetCitiesByRegion with regionId: {}", regionId);
        
        return locationRepositoryPort.findCitiesByRegion(regionId)
                .collectList()
                .map(locations -> {
                    logger.info("Retrieved {} locations successfully", locations.size());
                    return GetCitiesByRegionResponseContent.builder().build();
                })
                .doOnError(e -> logger.error("Error in GetCitiesByRegion", e, regionId));
    }

}