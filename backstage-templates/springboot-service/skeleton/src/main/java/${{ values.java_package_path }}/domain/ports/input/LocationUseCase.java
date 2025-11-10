package ${{ values.java_package_name }}.domain.ports.input;

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

/**
 * Consolidated use case interface for all Location operations.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
public interface LocationUseCase {
    
    CreateLocationResponseContent create(CreateLocationRequestContent request);

    GetLocationResponseContent get(String locationId);

    UpdateLocationResponseContent update(String locationId, UpdateLocationRequestContent request);

    DeleteLocationResponseContent delete(String locationId);

    ListLocationsResponseContent list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo);

    GetNeighborhoodsByCityResponseContent getNeighborhoodsByCity(String cityId);
    GetRegionsByCountryResponseContent getRegionsByCountry(String countryId);
    GetCitiesByRegionResponseContent getCitiesByRegion(String regionId);
}