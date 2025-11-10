package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.location.CountryResponse;
import com.example.userservice.domain.model.Country;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.CountryDbo;
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
public class CountryMapperImpl implements CountryMapper {

    @Override
    public CountryDbo toDbo(Country domain) {
        if ( domain == null ) {
            return null;
        }

        CountryDbo.CountryDboBuilder countryDbo = CountryDbo.builder();

        if ( domain.getCountryId() != null ) {
            countryDbo.id( UUID.fromString( domain.getCountryId() ) );
        }
        countryDbo.code( domain.getCode() );
        if ( domain.getCreatedAt() != null ) {
            countryDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        countryDbo.name( domain.getName() );
        if ( domain.getStatus() != null ) {
            countryDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            countryDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }

        return countryDbo.build();
    }

    @Override
    public Country toDomain(CountryDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        Country.CountryBuilder country = Country.builder();

        if ( dbo.getId() != null ) {
            country.countryId( dbo.getId().toString() );
        }
        country.code( dbo.getCode() );
        if ( dbo.getCreatedAt() != null ) {
            country.createdAt( dbo.getCreatedAt().toString() );
        }
        country.name( dbo.getName() );
        if ( dbo.getStatus() != null ) {
            country.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            country.updatedAt( dbo.getUpdatedAt().toString() );
        }

        return country.build();
    }

    @Override
    public List<Country> toDomainList(List<CountryDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<Country> list = new ArrayList<Country>( dbos.size() );
        for ( CountryDbo countryDbo : dbos ) {
            list.add( toDomain( countryDbo ) );
        }

        return list;
    }

    @Override
    public List<CountryDbo> toDboList(List<Country> domains) {
        if ( domains == null ) {
            return null;
        }

        List<CountryDbo> list = new ArrayList<CountryDbo>( domains.size() );
        for ( Country country : domains ) {
            list.add( toDbo( country ) );
        }

        return list;
    }

    @Override
    public CountryResponse toDto(Country domain) {
        if ( domain == null ) {
            return null;
        }

        CountryResponse.CountryResponseBuilder countryResponse = CountryResponse.builder();

        countryResponse.code( domain.getCode() );
        countryResponse.countryId( domain.getCountryId() );
        countryResponse.createdAt( domain.getCreatedAt() );
        countryResponse.name( domain.getName() );
        countryResponse.status( domain.getStatus() );
        countryResponse.updatedAt( domain.getUpdatedAt() );

        return countryResponse.build();
    }

    @Override
    public List<CountryResponse> toDtoList(List<Country> domains) {
        if ( domains == null ) {
            return null;
        }

        List<CountryResponse> list = new ArrayList<CountryResponse>( domains.size() );
        for ( Country country : domains ) {
            list.add( toDto( country ) );
        }

        return list;
    }
}
