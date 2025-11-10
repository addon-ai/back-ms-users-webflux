package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.location.CityResponse;
import com.example.userservice.domain.model.City;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.CityDbo;
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
public class CityMapperImpl implements CityMapper {

    @Override
    public CityDbo toDbo(City domain) {
        if ( domain == null ) {
            return null;
        }

        CityDbo.CityDboBuilder cityDbo = CityDbo.builder();

        if ( domain.getCityId() != null ) {
            cityDbo.id( UUID.fromString( domain.getCityId() ) );
        }
        if ( domain.getCreatedAt() != null ) {
            cityDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        cityDbo.name( domain.getName() );
        cityDbo.regionId( domain.getRegionId() );
        if ( domain.getStatus() != null ) {
            cityDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            cityDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }

        return cityDbo.build();
    }

    @Override
    public City toDomain(CityDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        City.CityBuilder city = City.builder();

        if ( dbo.getId() != null ) {
            city.cityId( dbo.getId().toString() );
        }
        if ( dbo.getCreatedAt() != null ) {
            city.createdAt( dbo.getCreatedAt().toString() );
        }
        city.name( dbo.getName() );
        city.regionId( dbo.getRegionId() );
        if ( dbo.getStatus() != null ) {
            city.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            city.updatedAt( dbo.getUpdatedAt().toString() );
        }

        return city.build();
    }

    @Override
    public List<City> toDomainList(List<CityDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<City> list = new ArrayList<City>( dbos.size() );
        for ( CityDbo cityDbo : dbos ) {
            list.add( toDomain( cityDbo ) );
        }

        return list;
    }

    @Override
    public List<CityDbo> toDboList(List<City> domains) {
        if ( domains == null ) {
            return null;
        }

        List<CityDbo> list = new ArrayList<CityDbo>( domains.size() );
        for ( City city : domains ) {
            list.add( toDbo( city ) );
        }

        return list;
    }

    @Override
    public CityResponse toDto(City domain) {
        if ( domain == null ) {
            return null;
        }

        CityResponse.CityResponseBuilder cityResponse = CityResponse.builder();

        cityResponse.cityId( domain.getCityId() );
        cityResponse.createdAt( domain.getCreatedAt() );
        cityResponse.name( domain.getName() );
        cityResponse.regionId( domain.getRegionId() );
        cityResponse.status( domain.getStatus() );
        cityResponse.updatedAt( domain.getUpdatedAt() );

        return cityResponse.build();
    }

    @Override
    public List<CityResponse> toDtoList(List<City> domains) {
        if ( domains == null ) {
            return null;
        }

        List<CityResponse> list = new ArrayList<CityResponse>( domains.size() );
        for ( City city : domains ) {
            list.add( toDto( city ) );
        }

        return list;
    }
}
