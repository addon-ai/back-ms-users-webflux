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
import reactor.core.publisher.Mono;
import reactor.core.publisher.Flux;

/**
 * Consolidated use case interface for all Location operations.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
public interface LocationUseCase {
    
    Mono<CreateLocationResponseContent> create(CreateLocationRequestContent request);

    Mono<GetLocationResponseContent> get(String locationId);

    Mono<UpdateLocationResponseContent> update(String locationId, UpdateLocationRequestContent request);

    Mono<DeleteLocationResponseContent> delete(String locationId);

    Mono<ListLocationsResponseContent> list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo);

    Mono<GetNeighborhoodsByCityResponseContent> getNeighborhoodsByCity(String cityId);
    Mono<GetRegionsByCountryResponseContent> getRegionsByCountry(String countryId);
    Mono<GetCitiesByRegionResponseContent> getCitiesByRegion(String regionId);
}