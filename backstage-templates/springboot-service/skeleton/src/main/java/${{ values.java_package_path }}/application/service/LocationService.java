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
import org.springframework.transaction.annotation.Transactional;
import java.util.List;

/**
 * Consolidated application service implementing all Location use cases.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
@Service
@RequiredArgsConstructor
@Transactional
public class LocationService implements LocationUseCase {

    private static final LoggingUtils logger = LoggingUtils.getLogger(LocationService.class);
    
    private final LocationRepositoryPort locationRepositoryPort;
    private final LocationMapper locationMapper;

    @Override
    public CreateLocationResponseContent create(CreateLocationRequestContent request) {
        logger.info("Executing CreateLocation with request: {}", request);
        
        try {
            Location location = locationMapper.fromCreateRequest(request);
            Location savedLocation = locationRepositoryPort.save(location);
            logger.info("Location created successfully with ID: {}", savedLocation.getLocationId());
            return locationMapper.toCreateResponse(savedLocation);
        } catch (Exception e) {
            logger.error("Error in CreateLocation", e, request);
            throw e;
        }
    }

    @Override
    public GetLocationResponseContent get(String locationId) {
        logger.info("Executing GetLocation with locationId: {}", locationId);
        
        try {
            Location location = locationRepositoryPort.findById(locationId)
                .orElseThrow(() -> new NotFoundException("Location not found"));
            
            logger.info("Location retrieved successfully with ID: {}", locationId);
            return locationMapper.toGetResponse(location);
        } catch (NotFoundException e) {
            logger.error("Location not found in GetLocation", e, locationId);
            throw e;
        } catch (Exception e) {
            logger.error("Error in GetLocation", e, locationId);
            throw e;
        }
    }

    @Override
    public UpdateLocationResponseContent update(String locationId, UpdateLocationRequestContent request) {
        logger.info("Executing UpdateLocation with locationId: {} and request: {}", locationId, request);
        
        try {
            Location existingLocation = locationRepositoryPort.findById(locationId)
                .orElseThrow(() -> new NotFoundException("Location not found"));
            
            // Merge request data into existing entity
            locationMapper.updateEntityFromRequest(request, existingLocation);
            existingLocation.setUpdatedAt(java.time.Instant.now().toString());
            
            Location savedLocation = locationRepositoryPort.save(existingLocation);
            logger.info("Location updated successfully with ID: {}", locationId);
            
            return locationMapper.toUpdateResponse(savedLocation);
        } catch (NotFoundException e) {
            logger.error("Location not found in UpdateLocation", e, locationId);
            throw e;
        } catch (Exception e) {
            logger.error("Error in UpdateLocation", e, locationId);
            throw e;
        }
    }

    @Override
    public DeleteLocationResponseContent delete(String locationId) {
        logger.info("Executing DeleteLocation with locationId: {}", locationId);
        
        try {
            Location location = locationRepositoryPort.findById(locationId)
                .orElseThrow(() -> new NotFoundException("Location not found"));
            
            // Soft delete: update status to INACTIVE and set updatedAt
            location.setStatus("INACTIVE");
            location.setUpdatedAt(java.time.Instant.now().toString());
            locationRepositoryPort.save(location);
            
            logger.info("Location soft deleted (status set to INACTIVE) with ID: {}", locationId);
            
            return DeleteLocationResponseContent.builder()
                .deleted(true)
                .message("Location deleted successfully")
                .build();
        } catch (NotFoundException e) {
            logger.error("Location not found in DeleteLocation", e, locationId);
            throw e;
        } catch (Exception e) {
            logger.error("Error in DeleteLocation", e, locationId);
            throw e;
        }
    }

    @Override
    public ListLocationsResponseContent list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo) {
        logger.info("Executing ListLocations with page: {}, size: {}, search: {}, status: {}, dateFrom: {}, dateTo: {}", 
                   page, size, search, status, dateFrom, dateTo);
        
        try {
            // Apply default values
            String effectiveStatus = (status == null || status.trim().isEmpty()) ? "ACTIVE" : status;
            String effectiveDateFrom = dateFrom;
            String effectiveDateTo = dateTo;
            
            if (effectiveDateFrom == null || effectiveDateFrom.trim().isEmpty()) {
                effectiveDateFrom = java.time.Instant.now().minus(30, java.time.temporal.ChronoUnit.DAYS).toString();
            }
            if (effectiveDateTo == null || effectiveDateTo.trim().isEmpty()) {
                effectiveDateTo = java.time.Instant.now().toString();
            }
            
            logger.info("Effective filters - status: {}, dateFrom: {}, dateTo: {}", 
                       effectiveStatus, effectiveDateFrom, effectiveDateTo);
            
            List<Location> locations = locationRepositoryPort.findByFilters(
                search, effectiveStatus, effectiveDateFrom, effectiveDateTo, page, size);
            
            logger.info("Retrieved {} locations successfully", locations.size());
            return locationMapper.toListResponse(locations, page != null ? page : 1, size != null ? size : 20);
        } catch (Exception e) {
            logger.error("Error in ListLocations", e);
            throw e;
        }
    }

    @Override
    public GetNeighborhoodsByCityResponseContent getNeighborhoodsByCity(String cityId) {
        logger.info("Executing GetNeighborhoodsByCity with cityId: {}", cityId);
        
        try {
            List<Location> locations = locationRepositoryPort.findNeighborhoodsByCity(cityId);
            logger.info("Retrieved {} locations successfully", locations.size());
            return GetNeighborhoodsByCityResponseContent.builder().build();
        } catch (Exception e) {
            logger.error("Error in GetNeighborhoodsByCity", e, cityId);
            throw e;
        }
    }

    @Override
    public GetRegionsByCountryResponseContent getRegionsByCountry(String countryId) {
        logger.info("Executing GetRegionsByCountry with countryId: {}", countryId);
        
        try {
            List<Location> locations = locationRepositoryPort.findRegionsByCountry(countryId);
            logger.info("Retrieved {} locations successfully", locations.size());
            return GetRegionsByCountryResponseContent.builder().build();
        } catch (Exception e) {
            logger.error("Error in GetRegionsByCountry", e, countryId);
            throw e;
        }
    }

    @Override
    public GetCitiesByRegionResponseContent getCitiesByRegion(String regionId) {
        logger.info("Executing GetCitiesByRegion with regionId: {}", regionId);
        
        try {
            List<Location> locations = locationRepositoryPort.findCitiesByRegion(regionId);
            logger.info("Retrieved {} locations successfully", locations.size());
            return GetCitiesByRegionResponseContent.builder().build();
        } catch (Exception e) {
            logger.error("Error in GetCitiesByRegion", e, regionId);
            throw e;
        }
    }

}