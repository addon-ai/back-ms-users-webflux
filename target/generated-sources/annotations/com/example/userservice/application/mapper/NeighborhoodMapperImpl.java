package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.location.NeighborhoodResponse;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.domain.model.Neighborhood;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.NeighborhoodDbo;
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
public class NeighborhoodMapperImpl implements NeighborhoodMapper {

    @Override
    public NeighborhoodDbo toDbo(Neighborhood domain) {
        if ( domain == null ) {
            return null;
        }

        NeighborhoodDbo.NeighborhoodDboBuilder neighborhoodDbo = NeighborhoodDbo.builder();

        if ( domain.getNeighborhoodId() != null ) {
            neighborhoodDbo.id( UUID.fromString( domain.getNeighborhoodId() ) );
        }
        neighborhoodDbo.cityId( domain.getCityId() );
        if ( domain.getCreatedAt() != null ) {
            neighborhoodDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        neighborhoodDbo.name( domain.getName() );
        if ( domain.getStatus() != null ) {
            neighborhoodDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            neighborhoodDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }

        return neighborhoodDbo.build();
    }

    @Override
    public Neighborhood toDomain(NeighborhoodDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        Neighborhood.NeighborhoodBuilder neighborhood = Neighborhood.builder();

        if ( dbo.getId() != null ) {
            neighborhood.neighborhoodId( dbo.getId().toString() );
        }
        neighborhood.cityId( dbo.getCityId() );
        if ( dbo.getCreatedAt() != null ) {
            neighborhood.createdAt( dbo.getCreatedAt().toString() );
        }
        neighborhood.name( dbo.getName() );
        if ( dbo.getStatus() != null ) {
            neighborhood.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            neighborhood.updatedAt( dbo.getUpdatedAt().toString() );
        }

        return neighborhood.build();
    }

    @Override
    public List<Neighborhood> toDomainList(List<NeighborhoodDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<Neighborhood> list = new ArrayList<Neighborhood>( dbos.size() );
        for ( NeighborhoodDbo neighborhoodDbo : dbos ) {
            list.add( toDomain( neighborhoodDbo ) );
        }

        return list;
    }

    @Override
    public List<NeighborhoodDbo> toDboList(List<Neighborhood> domains) {
        if ( domains == null ) {
            return null;
        }

        List<NeighborhoodDbo> list = new ArrayList<NeighborhoodDbo>( domains.size() );
        for ( Neighborhood neighborhood : domains ) {
            list.add( toDbo( neighborhood ) );
        }

        return list;
    }

    @Override
    public NeighborhoodResponse toDto(Neighborhood domain) {
        if ( domain == null ) {
            return null;
        }

        NeighborhoodResponse.NeighborhoodResponseBuilder neighborhoodResponse = NeighborhoodResponse.builder();

        neighborhoodResponse.cityId( domain.getCityId() );
        neighborhoodResponse.createdAt( domain.getCreatedAt() );
        neighborhoodResponse.name( domain.getName() );
        neighborhoodResponse.neighborhoodId( domain.getNeighborhoodId() );
        neighborhoodResponse.status( domain.getStatus() );
        neighborhoodResponse.updatedAt( domain.getUpdatedAt() );

        return neighborhoodResponse.build();
    }

    @Override
    public List<NeighborhoodResponse> toDtoList(List<Neighborhood> domains) {
        if ( domains == null ) {
            return null;
        }

        List<NeighborhoodResponse> list = new ArrayList<NeighborhoodResponse>( domains.size() );
        for ( Neighborhood neighborhood : domains ) {
            list.add( toDto( neighborhood ) );
        }

        return list;
    }
}
