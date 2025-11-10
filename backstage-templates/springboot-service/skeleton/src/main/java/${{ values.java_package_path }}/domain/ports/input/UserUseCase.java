package ${{ values.java_package_name }}.domain.ports.input;

import ${{ values.java_package_name }}.application.dto.user.CreateUserRequestContent;
import ${{ values.java_package_name }}.application.dto.user.CreateUserResponseContent;
import ${{ values.java_package_name }}.application.dto.user.GetUserResponseContent;
import ${{ values.java_package_name }}.application.dto.user.UpdateUserRequestContent;
import ${{ values.java_package_name }}.application.dto.user.UpdateUserResponseContent;
import ${{ values.java_package_name }}.application.dto.user.DeleteUserResponseContent;
import ${{ values.java_package_name }}.application.dto.user.ListUsersResponseContent;

/**
 * Consolidated use case interface for all User operations.
 * 
 * @author Jiliar Silgado <jiliar.silgado@gmail.com>
 * @version 1.0.0
 */
public interface UserUseCase {
    
    CreateUserResponseContent create(CreateUserRequestContent request);

    GetUserResponseContent get(String userId);

    UpdateUserResponseContent update(String userId, UpdateUserRequestContent request);

    DeleteUserResponseContent delete(String userId);

    ListUsersResponseContent list(Integer page, Integer size, String search, String status, String dateFrom, String dateTo);

}