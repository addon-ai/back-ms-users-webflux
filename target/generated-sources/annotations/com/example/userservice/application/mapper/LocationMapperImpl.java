package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.location.CreateLocationRequestContent;
import com.example.userservice.application.dto.location.CreateLocationResponseContent;
import com.example.userservice.application.dto.location.GetLocationResponseContent;
import com.example.userservice.application.dto.location.LocationResponse;
import com.example.userservice.application.dto.location.UpdateLocationRequestContent;
import com.example.userservice.application.dto.location.UpdateLocationResponseContent;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.domain.model.Location;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.LocationDbo;
import java.time.Instant;
import java.util.ArrayList;
import java.util.List;
import java.util.UUID;
import javax.annotation.processing.Generated;
import org.springframework.stereotype.Component;

@Generated(
    value = "org.mapstruct.ap.MappingProcessor",
    date = "2025-11-10T16:40:35-0500",
    comments = "version: 1.5.5.Final, compiler: Eclipse JDT (IDE) 3.44.0.v20251023-0518, environment: Java 21.0.8 (Eclipse Adoptium)"
)
@Component
public class LocationMapperImpl implements LocationMapper {

    @Override
    public LocationDbo toDbo(Location domain) {
        if ( domain == null ) {
            return null;
        }

        LocationDbo.LocationDboBuilder locationDbo = LocationDbo.builder();

        if ( domain.getLocationId() != null ) {
            locationDbo.id( UUID.fromString( domain.getLocationId() ) );
        }
        locationDbo.address( domain.getAddress() );
        locationDbo.city( domain.getCity() );
        locationDbo.country( domain.getCountry() );
        if ( domain.getCreatedAt() != null ) {
            locationDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        locationDbo.latitude( domain.getLatitude() );
        locationDbo.locationType( domain.getLocationType() );
        locationDbo.longitude( domain.getLongitude() );
        locationDbo.neighborhood( domain.getNeighborhood() );
        locationDbo.postalCode( domain.getPostalCode() );
        locationDbo.region( domain.getRegion() );
        if ( domain.getStatus() != null ) {
            locationDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            locationDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }
        locationDbo.userId( domain.getUserId() );

        return locationDbo.build();
    }

    @Override
    public Location toDomain(LocationDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        Location.LocationBuilder location = Location.builder();

        if ( dbo.getId() != null ) {
            location.locationId( dbo.getId().toString() );
        }
        location.address( dbo.getAddress() );
        location.city( dbo.getCity() );
        location.country( dbo.getCountry() );
        if ( dbo.getCreatedAt() != null ) {
            location.createdAt( dbo.getCreatedAt().toString() );
        }
        location.latitude( dbo.getLatitude() );
        location.locationType( dbo.getLocationType() );
        location.longitude( dbo.getLongitude() );
        location.neighborhood( dbo.getNeighborhood() );
        location.postalCode( dbo.getPostalCode() );
        location.region( dbo.getRegion() );
        if ( dbo.getStatus() != null ) {
            location.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            location.updatedAt( dbo.getUpdatedAt().toString() );
        }
        location.userId( dbo.getUserId() );

        return location.build();
    }

    @Override
    public List<Location> toDomainList(List<LocationDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<Location> list = new ArrayList<Location>( dbos.size() );
        for ( LocationDbo locationDbo : dbos ) {
            list.add( toDomain( locationDbo ) );
        }

        return list;
    }

    @Override
    public List<LocationDbo> toDboList(List<Location> domains) {
        if ( domains == null ) {
            return null;
        }

        List<LocationDbo> list = new ArrayList<LocationDbo>( domains.size() );
        for ( Location location : domains ) {
            list.add( toDbo( location ) );
        }

        return list;
    }

    @Override
    public Location fromCreateRequest(CreateLocationRequestContent request) {
        if ( request == null ) {
            return null;
        }

        Location.LocationBuilder location = Location.builder();

        location.address( request.getAddress() );
        location.latitude( request.getLatitude() );
        location.locationType( request.getLocationType() );
        location.longitude( request.getLongitude() );
        location.postalCode( request.getPostalCode() );
        location.userId( request.getUserId() );

        location.status( "ACTIVE" );
        location.createdAt( java.time.Instant.now().toString() );
        location.updatedAt( java.time.Instant.now().toString() );

        return location.build();
    }

    @Override
    public Location fromUpdateRequest(UpdateLocationRequestContent request) {
        if ( request == null ) {
            return null;
        }

        Location.LocationBuilder location = Location.builder();

        location.address( request.getAddress() );
        location.latitude( request.getLatitude() );
        location.locationType( request.getLocationType() );
        location.longitude( request.getLongitude() );
        location.postalCode( request.getPostalCode() );

        return location.build();
    }

    @Override
    public void updateEntityFromRequest(UpdateLocationRequestContent request, Location entity) {
        if ( request == null ) {
            return;
        }

        if ( request.getAddress() != null ) {
            entity.setAddress( request.getAddress() );
        }
        if ( request.getLatitude() != null ) {
            entity.setLatitude( request.getLatitude() );
        }
        if ( request.getLocationType() != null ) {
            entity.setLocationType( request.getLocationType() );
        }
        if ( request.getLongitude() != null ) {
            entity.setLongitude( request.getLongitude() );
        }
        if ( request.getPostalCode() != null ) {
            entity.setPostalCode( request.getPostalCode() );
        }
    }

    @Override
    public LocationResponse toDto(Location domain) {
        if ( domain == null ) {
            return null;
        }

        LocationResponse.LocationResponseBuilder locationResponse = LocationResponse.builder();

        locationResponse.address( domain.getAddress() );
        locationResponse.city( domain.getCity() );
        locationResponse.country( domain.getCountry() );
        locationResponse.latitude( domain.getLatitude() );
        locationResponse.locationId( domain.getLocationId() );
        locationResponse.locationType( domain.getLocationType() );
        locationResponse.longitude( domain.getLongitude() );
        locationResponse.neighborhood( domain.getNeighborhood() );
        locationResponse.postalCode( domain.getPostalCode() );
        locationResponse.region( domain.getRegion() );
        locationResponse.status( domain.getStatus() );
        locationResponse.userId( domain.getUserId() );

        return locationResponse.build();
    }

    @Override
    public List<LocationResponse> toDtoList(List<Location> domains) {
        if ( domains == null ) {
            return null;
        }

        List<LocationResponse> list = new ArrayList<LocationResponse>( domains.size() );
        for ( Location location : domains ) {
            list.add( toDto( location ) );
        }

        return list;
    }

    @Override
    public CreateLocationResponseContent toCreateResponse(Location domain) {
        if ( domain == null ) {
            return null;
        }

        CreateLocationResponseContent.CreateLocationResponseContentBuilder createLocationResponseContent = CreateLocationResponseContent.builder();

        createLocationResponseContent.address( domain.getAddress() );
        createLocationResponseContent.createdAt( domain.getCreatedAt() );
        createLocationResponseContent.latitude( domain.getLatitude() );
        createLocationResponseContent.locationId( domain.getLocationId() );
        createLocationResponseContent.locationType( domain.getLocationType() );
        createLocationResponseContent.longitude( domain.getLongitude() );
        createLocationResponseContent.postalCode( domain.getPostalCode() );
        createLocationResponseContent.status( domain.getStatus() );
        createLocationResponseContent.userId( domain.getUserId() );

        return createLocationResponseContent.build();
    }

    @Override
    public GetLocationResponseContent toGetResponse(Location domain) {
        if ( domain == null ) {
            return null;
        }

        GetLocationResponseContent.GetLocationResponseContentBuilder getLocationResponseContent = GetLocationResponseContent.builder();

        getLocationResponseContent.address( domain.getAddress() );
        getLocationResponseContent.city( domain.getCity() );
        getLocationResponseContent.country( domain.getCountry() );
        getLocationResponseContent.createdAt( domain.getCreatedAt() );
        getLocationResponseContent.latitude( domain.getLatitude() );
        getLocationResponseContent.locationId( domain.getLocationId() );
        getLocationResponseContent.locationType( domain.getLocationType() );
        getLocationResponseContent.longitude( domain.getLongitude() );
        getLocationResponseContent.neighborhood( domain.getNeighborhood() );
        getLocationResponseContent.postalCode( domain.getPostalCode() );
        getLocationResponseContent.region( domain.getRegion() );
        getLocationResponseContent.status( domain.getStatus() );
        getLocationResponseContent.updatedAt( domain.getUpdatedAt() );
        getLocationResponseContent.userId( domain.getUserId() );

        return getLocationResponseContent.build();
    }

    @Override
    public UpdateLocationResponseContent toUpdateResponse(Location domain) {
        if ( domain == null ) {
            return null;
        }

        UpdateLocationResponseContent.UpdateLocationResponseContentBuilder updateLocationResponseContent = UpdateLocationResponseContent.builder();

        updateLocationResponseContent.address( domain.getAddress() );
        updateLocationResponseContent.city( domain.getCity() );
        updateLocationResponseContent.country( domain.getCountry() );
        updateLocationResponseContent.latitude( domain.getLatitude() );
        updateLocationResponseContent.locationId( domain.getLocationId() );
        updateLocationResponseContent.locationType( domain.getLocationType() );
        updateLocationResponseContent.longitude( domain.getLongitude() );
        updateLocationResponseContent.neighborhood( domain.getNeighborhood() );
        updateLocationResponseContent.postalCode( domain.getPostalCode() );
        updateLocationResponseContent.region( domain.getRegion() );
        updateLocationResponseContent.status( domain.getStatus() );
        updateLocationResponseContent.updatedAt( domain.getUpdatedAt() );
        updateLocationResponseContent.userId( domain.getUserId() );

        return updateLocationResponseContent.build();
    }
}
