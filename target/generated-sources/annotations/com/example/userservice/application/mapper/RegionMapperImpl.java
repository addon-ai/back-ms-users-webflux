package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.location.RegionResponse;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.domain.model.Region;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.RegionDbo;
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
public class RegionMapperImpl implements RegionMapper {

    @Override
    public RegionDbo toDbo(Region domain) {
        if ( domain == null ) {
            return null;
        }

        RegionDbo.RegionDboBuilder regionDbo = RegionDbo.builder();

        if ( domain.getRegionId() != null ) {
            regionDbo.id( UUID.fromString( domain.getRegionId() ) );
        }
        regionDbo.code( domain.getCode() );
        regionDbo.countryId( domain.getCountryId() );
        if ( domain.getCreatedAt() != null ) {
            regionDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        regionDbo.name( domain.getName() );
        if ( domain.getStatus() != null ) {
            regionDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            regionDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }

        return regionDbo.build();
    }

    @Override
    public Region toDomain(RegionDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        Region.RegionBuilder region = Region.builder();

        if ( dbo.getId() != null ) {
            region.regionId( dbo.getId().toString() );
        }
        region.code( dbo.getCode() );
        region.countryId( dbo.getCountryId() );
        if ( dbo.getCreatedAt() != null ) {
            region.createdAt( dbo.getCreatedAt().toString() );
        }
        region.name( dbo.getName() );
        if ( dbo.getStatus() != null ) {
            region.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            region.updatedAt( dbo.getUpdatedAt().toString() );
        }

        return region.build();
    }

    @Override
    public List<Region> toDomainList(List<RegionDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<Region> list = new ArrayList<Region>( dbos.size() );
        for ( RegionDbo regionDbo : dbos ) {
            list.add( toDomain( regionDbo ) );
        }

        return list;
    }

    @Override
    public List<RegionDbo> toDboList(List<Region> domains) {
        if ( domains == null ) {
            return null;
        }

        List<RegionDbo> list = new ArrayList<RegionDbo>( domains.size() );
        for ( Region region : domains ) {
            list.add( toDbo( region ) );
        }

        return list;
    }

    @Override
    public RegionResponse toDto(Region domain) {
        if ( domain == null ) {
            return null;
        }

        RegionResponse.RegionResponseBuilder regionResponse = RegionResponse.builder();

        regionResponse.code( domain.getCode() );
        regionResponse.countryId( domain.getCountryId() );
        regionResponse.createdAt( domain.getCreatedAt() );
        regionResponse.name( domain.getName() );
        regionResponse.regionId( domain.getRegionId() );
        regionResponse.status( domain.getStatus() );
        regionResponse.updatedAt( domain.getUpdatedAt() );

        return regionResponse.build();
    }

    @Override
    public List<RegionResponse> toDtoList(List<Region> domains) {
        if ( domains == null ) {
            return null;
        }

        List<RegionResponse> list = new ArrayList<RegionResponse>( domains.size() );
        for ( Region region : domains ) {
            list.add( toDto( region ) );
        }

        return list;
    }
}
