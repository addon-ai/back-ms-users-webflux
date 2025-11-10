package com.example.userservice.application.mapper;

import com.example.userservice.application.dto.user.CreateUserRequestContent;
import com.example.userservice.application.dto.user.CreateUserResponseContent;
import com.example.userservice.application.dto.user.GetUserResponseContent;
import com.example.userservice.application.dto.user.UpdateUserRequestContent;
import com.example.userservice.application.dto.user.UpdateUserResponseContent;
import com.example.userservice.application.dto.user.UserResponse;
import com.example.userservice.domain.model.EntityStatus;
import com.example.userservice.domain.model.User;
import com.example.userservice.infrastructure.adapters.output.persistence.entity.UserDbo;
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
public class UserMapperImpl implements UserMapper {

    @Override
    public UserDbo toDbo(User domain) {
        if ( domain == null ) {
            return null;
        }

        UserDbo.UserDboBuilder userDbo = UserDbo.builder();

        if ( domain.getUserId() != null ) {
            userDbo.id( UUID.fromString( domain.getUserId() ) );
        }
        if ( domain.getCreatedAt() != null ) {
            userDbo.createdAt( Instant.parse( domain.getCreatedAt() ) );
        }
        userDbo.email( domain.getEmail() );
        userDbo.firstName( domain.getFirstName() );
        userDbo.lastName( domain.getLastName() );
        if ( domain.getStatus() != null ) {
            userDbo.status( Enum.valueOf( EntityStatus.class, domain.getStatus() ) );
        }
        if ( domain.getUpdatedAt() != null ) {
            userDbo.updatedAt( Instant.parse( domain.getUpdatedAt() ) );
        }
        userDbo.username( domain.getUsername() );

        return userDbo.build();
    }

    @Override
    public User toDomain(UserDbo dbo) {
        if ( dbo == null ) {
            return null;
        }

        User.UserBuilder user = User.builder();

        if ( dbo.getId() != null ) {
            user.userId( dbo.getId().toString() );
        }
        if ( dbo.getCreatedAt() != null ) {
            user.createdAt( dbo.getCreatedAt().toString() );
        }
        user.email( dbo.getEmail() );
        user.firstName( dbo.getFirstName() );
        user.lastName( dbo.getLastName() );
        if ( dbo.getStatus() != null ) {
            user.status( dbo.getStatus().name() );
        }
        if ( dbo.getUpdatedAt() != null ) {
            user.updatedAt( dbo.getUpdatedAt().toString() );
        }
        user.username( dbo.getUsername() );

        return user.build();
    }

    @Override
    public List<User> toDomainList(List<UserDbo> dbos) {
        if ( dbos == null ) {
            return null;
        }

        List<User> list = new ArrayList<User>( dbos.size() );
        for ( UserDbo userDbo : dbos ) {
            list.add( toDomain( userDbo ) );
        }

        return list;
    }

    @Override
    public List<UserDbo> toDboList(List<User> domains) {
        if ( domains == null ) {
            return null;
        }

        List<UserDbo> list = new ArrayList<UserDbo>( domains.size() );
        for ( User user : domains ) {
            list.add( toDbo( user ) );
        }

        return list;
    }

    @Override
    public User fromCreateRequest(CreateUserRequestContent request) {
        if ( request == null ) {
            return null;
        }

        User.UserBuilder user = User.builder();

        user.email( request.getEmail() );
        user.firstName( request.getFirstName() );
        user.lastName( request.getLastName() );
        user.username( request.getUsername() );

        user.status( "ACTIVE" );
        user.createdAt( java.time.Instant.now().toString() );
        user.updatedAt( java.time.Instant.now().toString() );

        return user.build();
    }

    @Override
    public User fromUpdateRequest(UpdateUserRequestContent request) {
        if ( request == null ) {
            return null;
        }

        User.UserBuilder user = User.builder();

        user.email( request.getEmail() );
        user.firstName( request.getFirstName() );
        user.lastName( request.getLastName() );

        return user.build();
    }

    @Override
    public void updateEntityFromRequest(UpdateUserRequestContent request, User entity) {
        if ( request == null ) {
            return;
        }

        if ( request.getEmail() != null ) {
            entity.setEmail( request.getEmail() );
        }
        if ( request.getFirstName() != null ) {
            entity.setFirstName( request.getFirstName() );
        }
        if ( request.getLastName() != null ) {
            entity.setLastName( request.getLastName() );
        }
    }

    @Override
    public UserResponse toDto(User domain) {
        if ( domain == null ) {
            return null;
        }

        UserResponse.UserResponseBuilder userResponse = UserResponse.builder();

        userResponse.createdAt( domain.getCreatedAt() );
        userResponse.email( domain.getEmail() );
        userResponse.firstName( domain.getFirstName() );
        userResponse.lastName( domain.getLastName() );
        userResponse.status( domain.getStatus() );
        userResponse.updatedAt( domain.getUpdatedAt() );
        userResponse.userId( domain.getUserId() );
        userResponse.username( domain.getUsername() );

        return userResponse.build();
    }

    @Override
    public List<UserResponse> toDtoList(List<User> domains) {
        if ( domains == null ) {
            return null;
        }

        List<UserResponse> list = new ArrayList<UserResponse>( domains.size() );
        for ( User user : domains ) {
            list.add( toDto( user ) );
        }

        return list;
    }

    @Override
    public CreateUserResponseContent toCreateResponse(User domain) {
        if ( domain == null ) {
            return null;
        }

        CreateUserResponseContent.CreateUserResponseContentBuilder createUserResponseContent = CreateUserResponseContent.builder();

        createUserResponseContent.createdAt( domain.getCreatedAt() );
        createUserResponseContent.email( domain.getEmail() );
        createUserResponseContent.firstName( domain.getFirstName() );
        createUserResponseContent.lastName( domain.getLastName() );
        createUserResponseContent.status( domain.getStatus() );
        createUserResponseContent.updatedAt( domain.getUpdatedAt() );
        createUserResponseContent.userId( domain.getUserId() );
        createUserResponseContent.username( domain.getUsername() );

        return createUserResponseContent.build();
    }

    @Override
    public GetUserResponseContent toGetResponse(User domain) {
        if ( domain == null ) {
            return null;
        }

        GetUserResponseContent.GetUserResponseContentBuilder getUserResponseContent = GetUserResponseContent.builder();

        getUserResponseContent.createdAt( domain.getCreatedAt() );
        getUserResponseContent.email( domain.getEmail() );
        getUserResponseContent.firstName( domain.getFirstName() );
        getUserResponseContent.lastName( domain.getLastName() );
        getUserResponseContent.status( domain.getStatus() );
        getUserResponseContent.updatedAt( domain.getUpdatedAt() );
        getUserResponseContent.userId( domain.getUserId() );
        getUserResponseContent.username( domain.getUsername() );

        return getUserResponseContent.build();
    }

    @Override
    public UpdateUserResponseContent toUpdateResponse(User domain) {
        if ( domain == null ) {
            return null;
        }

        UpdateUserResponseContent.UpdateUserResponseContentBuilder updateUserResponseContent = UpdateUserResponseContent.builder();

        updateUserResponseContent.createdAt( domain.getCreatedAt() );
        updateUserResponseContent.email( domain.getEmail() );
        updateUserResponseContent.firstName( domain.getFirstName() );
        updateUserResponseContent.lastName( domain.getLastName() );
        updateUserResponseContent.status( domain.getStatus() );
        updateUserResponseContent.updatedAt( domain.getUpdatedAt() );
        updateUserResponseContent.userId( domain.getUserId() );
        updateUserResponseContent.username( domain.getUsername() );

        return updateUserResponseContent.build();
    }
}
