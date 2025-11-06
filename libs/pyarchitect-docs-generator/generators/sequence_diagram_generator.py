#!/usr/bin/env python3

"""
Sequence diagram generator for hexagonal architecture CRUD operations.
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Any, Optional
import pystache


class SequenceDiagramGenerator:
    """Generates PlantUML sequence diagrams for CRUD operations."""
    
    def __init__(self, templates_dir: str = "templates"):
        self.templates_dir = Path(templates_dir)
        self.renderer = pystache.Renderer()
    
    def generate_sequence_diagrams(self, project: Dict[str, Any], output_dir: str) -> List[str]:
        """Generate sequence diagrams based on actual endpoints found in the project."""
        generated_files = []
        
        # Create project-specific output directory
        project_output_dir = Path(output_dir) / "puml" / "sequences" / project["name"]
        project_output_dir.mkdir(parents=True, exist_ok=True)
        
        # Extract main entity from project
        entities = project.get("entities", [])
        if not entities:
            return generated_files
        
        # Use the first entity as the main entity for the service
        main_entity = entities[0]
        
        # Analyze actual endpoints from controllers
        endpoints = self._extract_endpoints_from_project(project)
        
        if not endpoints:
            return generated_files
        
        # Generate sequence diagrams for each found endpoint
        for endpoint in endpoints:
            context = self._build_sequence_context_for_endpoint(project, main_entity, endpoint)
            diagram_content = self._render_sequence_template(endpoint["operation_type"], context)
            
            if diagram_content:
                filename = f"{endpoint['operation_name']} - Sequence Diagram.puml"
                output_file = project_output_dir / filename
                
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(diagram_content)
                
                generated_files.append(str(output_file))
        
        return generated_files
    
    def _extract_endpoints_from_project(self, project: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Extract actual endpoints from controller classes."""
        endpoints = []
        
        # Get controllers from project layers
        controllers = project.get("layers", {}).get("infrastructure", {}).get("controllers", [])
        for controller in controllers:
            controller_file = controller.get("file", "")
            controller_name = controller.get("name", "")
            controller_methods = controller.get("methods", [])
            
            for method in controller_methods:
                method_name = method.get("name", "")
                
                # Skip constructors and utility methods
                if method_name in ["equals", "hashCode", "toString"]:
                    continue
                
                # Analyze the actual method implementation
                method_details = self._analyze_controller_method(controller_file, method_name, controller_name)
                if method_details:
                    endpoints.append(method_details)
        return endpoints
    
    def _analyze_controller_method(self, controller_file: str, method_name: str, controller_name: str) -> Optional[Dict[str, Any]]:
        """Analyze actual controller method implementation."""
        try:
            with open(controller_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Find the method in the file
            method_pattern = rf'public\s+ResponseEntity<\w+>\s+{method_name}\s*\([^{{]*\)\s*{{[^}}]*?}}'  
            method_match = re.search(method_pattern, content, re.DOTALL)
            
            if not method_match:
                return None
            
            method_code = method_match.group(0)
            
            # Extract use case call
            use_case_call = self._extract_use_case_call(method_code)
            
            # Extract controller entity (LocationController -> Location)
            controller_entity = controller_name.replace("Controller", "")
            
            # Build operation details
            operation_name = method_name.replace(method_name[0], method_name[0].upper(), 1)
            
            return {
                "operation_type": self._determine_operation_type(method_name),
                "operation_name": operation_name,
                "http_method": self._extract_http_method_from_name(method_name),
                "use_case_call": use_case_call,
                "controller_entity": controller_entity,
                "method_code": method_code
            }
            
        except Exception as e:
            print(f"Error analyzing method {method_name}: {e}")
            return None
    
    def _extract_use_case_call(self, method_code: str) -> str:
        """Extract use case method call."""
        use_case_pattern = r'\w+UseCase\.(\w+)\s*\([^)]*\)'
        match = re.search(use_case_pattern, method_code)
        return match.group(1) if match else ""
    
    def _determine_operation_type(self, method_name: str) -> str:
        """Determine operation type from method name."""
        method_lower = method_name.lower()
        if method_name.startswith("create"):
            return "Create"
        elif method_name.startswith("get"):
            # Check if it's a simple get by ID (getMovie, getUser, etc.)
            if method_lower in ["getmovie", "getuser", "getlocation", "getrental"] or "ById" in method_name:
                return "Get"
            elif method_lower.startswith("list") or "list" in method_lower:
                return "List"
            else:
                return "Custom"
        elif method_name.startswith("update"):
            return "Update"
        elif method_name.startswith("delete"):
            return "Delete"
        elif method_name.startswith("list"):
            return "List"
        else:
            return "Custom"
    
    def _extract_http_method_from_name(self, method_name: str) -> str:
        """Extract HTTP method from method name."""
        if method_name.startswith("create"):
            return "POST"
        elif method_name.startswith("update"):
            return "PUT"
        elif method_name.startswith("delete"):
            return "DELETE"
        else:
            return "GET"
    
    def _map_method_to_operation(self, method_name: str) -> Dict[str, Any]:
        """Map controller method names to operation types."""
        method_lower = method_name.lower()
        
        # CRUD mappings - exact method name matches
        if method_name == "createUser":
            return {"operation_type": "Create", "operation_name": "Create User", "http_method": "POST"}
        elif method_name == "getUser":
            return {"operation_type": "Get", "operation_name": "Get User", "http_method": "GET"}
        elif method_name == "updateUser":
            return {"operation_type": "Update", "operation_name": "Update User", "http_method": "PUT"}
        elif method_name == "deleteUser":
            return {"operation_type": "Delete", "operation_name": "Delete User", "http_method": "DELETE"}
        elif method_name == "listUsers":
            return {"operation_type": "List", "operation_name": "List Users", "http_method": "GET"}
        # Generic CRUD mappings for other entities
        elif method_lower.startswith("create"):
            entity_name = method_name[6:] if len(method_name) > 6 else "Entity"
            return {"operation_type": "Create", "operation_name": f"Create {entity_name}", "http_method": "POST"}
        elif method_lower.startswith("get") and not method_lower.startswith("getall"):
            entity_name = method_name[3:] if len(method_name) > 3 else "Entity"
            return {"operation_type": "Get", "operation_name": f"Get {entity_name}", "http_method": "GET"}
        elif method_lower.startswith("update"):
            entity_name = method_name[6:] if len(method_name) > 6 else "Entity"
            return {"operation_type": "Update", "operation_name": f"Update {entity_name}", "http_method": "PUT"}
        elif method_lower.startswith("delete"):
            entity_name = method_name[6:] if len(method_name) > 6 else "Entity"
            return {"operation_type": "Delete", "operation_name": f"Delete {entity_name}", "http_method": "DELETE"}
        elif method_lower.startswith("list"):
            entity_name = method_name[4:] if len(method_name) > 4 else "Entities"
            return {"operation_type": "List", "operation_name": f"List {entity_name}", "http_method": "GET"}
        # Custom operations
        elif method_lower.startswith("search"):
            return {"operation_type": "Search", "operation_name": f"Search {method_name[6:]}", "http_method": "GET"}
        elif method_lower.startswith("validate"):
            return {"operation_type": "Validate", "operation_name": f"Validate {method_name[8:]}", "http_method": "POST"}
        elif method_lower.startswith("process"):
            return {"operation_type": "Process", "operation_name": f"Process {method_name[7:]}", "http_method": "POST"}
        elif method_lower.startswith("calculate"):
            return {"operation_type": "Calculate", "operation_name": f"Calculate {method_name[9:]}", "http_method": "POST"}
        else:
            # Generic custom operation
            return {"operation_type": "Custom", "operation_name": method_name.capitalize(), "http_method": "POST"}
        
        return None
    
    def _build_sequence_context_for_endpoint(self, project: Dict[str, Any], entity: str, endpoint: Dict[str, Any]) -> Dict[str, Any]:
        """Build context for sequence diagram template based on endpoint."""
        base_package = project.get("base_package", "com.example.service")
        operation = endpoint["operation_type"]
        operation_name = endpoint["operation_name"]
        use_case_call = endpoint.get("use_case_call", "")
        controller_entity = endpoint.get("controller_entity", entity)
        
        # Use controller entity for accurate naming
        entity = controller_entity
        
        return {
            "operation": operation,
            "operation_name": operation_name,
            "entity": entity,
            "entity_lower": entity.lower(),
            "service_name": entity,
            "base_package": base_package,
            "controller_name": f"{entity}Controller",
            "use_case_name": f"{entity}UseCase", 
            "service_class_name": f"{entity}Service",
            "mapper_name": f"{entity}Mapper",
            "repository_port_name": f"{entity}RepositoryPort",
            "repository_adapter_name": f"{entity}RepositoryAdapter",
            "jpa_repository_name": f"Jpa{entity}Repository",
            "entity_dbo_name": f"{entity}Dbo",
            "request_dto": f"{operation}{entity}RequestContent",
            "response_dto": f"{operation}{entity}ResponseContent",
            "use_case_call": use_case_call,
            "is_create": operation == "Create",
            "is_get": operation == "Get",
            "is_update": operation == "Update", 
            "is_delete": operation == "Delete",
            "is_list": operation == "List",
            "is_search": operation == "Search",
            "is_custom": operation in ["Custom", "Validate", "Process", "Calculate"],
            "http_method": endpoint["http_method"],
            "http_status": self._get_http_status(operation),
            "endpoint": self._build_actual_endpoint(endpoint)
        }
    
    def _build_actual_endpoint(self, endpoint: Dict[str, Any]) -> str:
        """Build actual endpoint from method analysis."""
        method_name = endpoint["operation_name"].lower()
        controller_entity = endpoint.get("controller_entity", "entity")
        
        if method_name == "getneighborhoodsbycity":
            return "/locations/neighborhoods-by-city"
        elif method_name == "getregionsbycountry":
            return "/locations/regions-by-country"
        elif method_name == "getcitiesbyregion":
            return "/locations/cities-by-region"
        else:
            return self._get_endpoint_for_operation(controller_entity.lower(), endpoint["operation_type"], endpoint["http_method"])
    
    def _extract_entity_from_operation(self, operation_name: str) -> Optional[str]:
        """Extract entity name from operation name."""
        # Remove operation prefix and extract entity
        if operation_name.startswith("Create "):
            return operation_name[7:].split()[0]  # "Create User" -> "User"
        elif operation_name.startswith("Get "):
            entity_part = operation_name[4:]  # "Get NeighborhoodsByCity" -> "NeighborhoodsByCity"
            # Extract the main entity (first word before "By" or "s")
            if "By" in entity_part:
                return entity_part.split("By")[0].rstrip("s")  # "NeighborhoodsByCity" -> "Neighborhood"
            elif entity_part.endswith("s"):
                return entity_part[:-1]  # "Users" -> "User"
            return entity_part
        elif operation_name.startswith("Update "):
            return operation_name[7:].split()[0]  # "Update User" -> "User"
        elif operation_name.startswith("Delete "):
            return operation_name[7:].split()[0]  # "Delete User" -> "User"
        elif operation_name.startswith("List "):
            entity_part = operation_name[5:]  # "List Users" -> "Users"
            return entity_part.rstrip("s")  # "Users" -> "User"
        
        return None
    
    def _build_sequence_context(self, project: Dict[str, Any], entity: str, operation: str) -> Dict[str, Any]:
        """Build context for sequence diagram template."""
        base_package = project.get("base_package", "com.example.service")
        
        # Extract service name from project name or entity
        service_name = entity
        
        return {
            "operation": operation,
            "entity": entity,
            "entity_lower": entity.lower(),
            "service_name": service_name,
            "base_package": base_package,
            "controller_name": f"{entity}Controller",
            "use_case_name": f"{entity}UseCase", 
            "service_class_name": f"{entity}Service",
            "mapper_name": f"{entity}Mapper",
            "repository_port_name": f"{entity}RepositoryPort",
            "repository_adapter_name": f"{entity}RepositoryAdapter",
            "jpa_repository_name": f"Jpa{entity}Repository",
            "entity_dbo_name": f"{entity}Dbo",
            "request_dto": f"{operation}{entity}RequestContent",
            "response_dto": f"{operation}{entity}ResponseContent",
            "is_create": operation == "Create",
            "is_get": operation == "Get",
            "is_update": operation == "Update", 
            "is_delete": operation == "Delete",
            "is_list": operation == "List",
            "http_method": self._get_http_method(operation),
            "http_status": self._get_http_status(operation),
            "endpoint": self._get_endpoint(entity.lower(), operation)
        }
    
    def _get_http_method(self, operation: str) -> str:
        """Get HTTP method for operation."""
        method_map = {
            "Create": "POST",
            "Get": "GET", 
            "Update": "PUT",
            "Delete": "DELETE",
            "List": "GET"
        }
        return method_map.get(operation, "GET")
    
    def _get_http_status(self, operation: str) -> str:
        """Get HTTP status code for operation."""
        status_map = {
            "Create": "201",
            "Get": "200",
            "Update": "200", 
            "Delete": "200",
            "List": "200"
        }
        return status_map.get(operation, "200")
    
    def _get_endpoint_for_operation(self, entity_lower: str, operation: str, http_method: str) -> str:
        """Get REST endpoint for operation."""
        if operation == "Create":
            return f"/{entity_lower}s"
        elif operation == "Get":
            return f"/{entity_lower}s/{{{entity_lower}Id}}"
        elif operation == "Update":
            return f"/{entity_lower}s/{{{entity_lower}Id}}"
        elif operation == "Delete":
            return f"/{entity_lower}s/{{{entity_lower}Id}}"
        elif operation == "List":
            return f"/{entity_lower}s"
        elif operation == "Search":
            return f"/{entity_lower}s/search"
        else:
            return f"/{entity_lower}s/{operation.lower()}"
    
    def _get_endpoint(self, entity_lower: str, operation: str) -> str:
        """Get REST endpoint for operation."""
        return self._get_endpoint_for_operation(entity_lower, operation, "GET")
    
    def _render_sequence_template(self, operation: str, context: Dict[str, Any]) -> str:
        """Render sequence diagram template."""
        template_file = self.templates_dir / f"sequence_{operation.lower()}.mustache"
        
        if not template_file.exists():
            # Use generic template if specific one doesn't exist
            template_file = self.templates_dir / "sequence_generic.mustache"
        
        if not template_file.exists():
            return self._generate_inline_template(operation, context)
        
        try:
            with open(template_file, 'r', encoding='utf-8') as f:
                template_content = f.read()
            
            return self.renderer.render(template_content, context)
        
        except Exception as e:
            print(f"Error rendering template {template_file}: {e}")
            return self._generate_inline_template(operation, context)
    
    def _generate_inline_template(self, operation: str, context: Dict[str, Any]) -> str:
        """Generate sequence diagram content inline when template is not available."""
        entity = context["entity"]
        entity_lower = context["entity_lower"]
        
        if operation == "Create":
            return f"""@startuml Create {entity}
!theme plain
title Create {entity} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['service_class_name']}\\n(Application Service)" as Service
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: create({context['request_dto']})
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> Mapper: fromCreateRequest({context['request_dto']})
activate Mapper
Mapper --> UseCase: {entity} (domain object)
deactivate Mapper

UseCase -> RepoPort: save({entity})
activate RepoPort
RepoPort -> RepoAdapter: save({entity})
activate RepoAdapter

RepoAdapter -> Mapper: toDbo({entity})
activate Mapper
Mapper --> RepoAdapter: {context['entity_dbo_name']}
deactivate Mapper

RepoAdapter -> JpaRepo: save({context['entity_dbo_name']})
activate JpaRepo
JpaRepo -> DB: INSERT INTO {entity_lower}s
DB --> JpaRepo: {context['entity_dbo_name']}
JpaRepo --> RepoAdapter: {context['entity_dbo_name']}
deactivate JpaRepo

RepoAdapter -> Mapper: toDomain({context['entity_dbo_name']})
activate Mapper
Mapper --> RepoAdapter: {entity}
deactivate Mapper

RepoAdapter --> RepoPort: {entity}
deactivate RepoAdapter
RepoPort --> UseCase: {entity}
deactivate RepoPort

UseCase -> Mapper: toCreateResponse({entity})
activate Mapper
Mapper --> UseCase: {context['response_dto']}
deactivate Mapper

UseCase --> Controller: {context['response_dto']}
deactivate UseCase

Controller --> Client: HTTP {context['http_status']}
deactivate Controller

@enduml"""
        
        elif operation == "Get":
            return f"""@startuml Get {entity}
!theme plain
title Get {entity} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: get({entity_lower}Id)
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> RepoPort: findById({entity_lower}Id)
activate RepoPort
RepoPort -> RepoAdapter: findById({entity_lower}Id)
activate RepoAdapter
RepoAdapter -> JpaRepo: findById({entity_lower}Id)
activate JpaRepo
JpaRepo -> DB: SELECT * FROM {entity_lower}s WHERE id = ?
DB --> JpaRepo: Optional<{context['entity_dbo_name']}>
JpaRepo --> RepoAdapter: Optional<{context['entity_dbo_name']}>
deactivate JpaRepo

alt {entity} Found
    RepoAdapter -> Mapper: toDomain({context['entity_dbo_name']})
    activate Mapper
    Mapper --> RepoAdapter: {entity}
    deactivate Mapper
    
    RepoAdapter --> RepoPort: Optional<{entity}>
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional<{entity}>
    deactivate RepoPort
    
    UseCase -> Mapper: toGetResponse({entity})
    activate Mapper
    Mapper --> UseCase: {context['response_dto']}
    deactivate Mapper
    
    UseCase --> Controller: {context['response_dto']}
    deactivate UseCase
    
    Controller --> Client: HTTP {context['http_status']}
    deactivate Controller

else {entity} Not Found
    RepoAdapter --> RepoPort: Optional.empty()
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional.empty()
    deactivate RepoPort
    
    UseCase --> Controller: NotFoundException("{entity} not found")
    deactivate UseCase
    
    Controller --> Client: HTTP 404
    deactivate Controller
end

@enduml"""
        
        elif operation == "Update":
            return f"""@startuml Update {entity}
!theme plain
title Update {entity} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: update({entity_lower}Id, {context['request_dto']})
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> RepoPort: findById({entity_lower}Id)
activate RepoPort
RepoPort -> RepoAdapter: findById({entity_lower}Id)
activate RepoAdapter
RepoAdapter -> JpaRepo: findById({entity_lower}Id)
activate JpaRepo
JpaRepo -> DB: SELECT * FROM {entity_lower}s WHERE id = ?
DB --> JpaRepo: Optional<{context['entity_dbo_name']}>
JpaRepo --> RepoAdapter: Optional<{context['entity_dbo_name']}>
deactivate JpaRepo

alt {entity} Found
    RepoAdapter -> Mapper: toDomain({context['entity_dbo_name']})
    activate Mapper
    Mapper --> RepoAdapter: {entity}
    deactivate Mapper
    
    RepoAdapter --> RepoPort: Optional<{entity}>
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional<{entity}>
    deactivate RepoPort
    
    UseCase -> Mapper: updateEntityFromRequest({context['request_dto']}, {entity})
    activate Mapper
    Mapper --> UseCase: void ({entity} updated)
    deactivate Mapper
    
    UseCase -> RepoPort: save({entity})
    activate RepoPort
    RepoPort -> RepoAdapter: save({entity})
    activate RepoAdapter
    
    RepoAdapter -> Mapper: toDbo({entity})
    activate Mapper
    Mapper --> RepoAdapter: {context['entity_dbo_name']}
    deactivate Mapper
    
    RepoAdapter -> JpaRepo: save({context['entity_dbo_name']})
    activate JpaRepo
    JpaRepo -> DB: UPDATE {entity_lower}s SET ... WHERE id = ?
    DB --> JpaRepo: {context['entity_dbo_name']}
    JpaRepo --> RepoAdapter: {context['entity_dbo_name']}
    deactivate JpaRepo
    
    RepoAdapter -> Mapper: toDomain({context['entity_dbo_name']})
    activate Mapper
    Mapper --> RepoAdapter: {entity}
    deactivate Mapper
    
    RepoAdapter --> RepoPort: {entity}
    deactivate RepoAdapter
    RepoPort --> UseCase: {entity}
    deactivate RepoPort
    
    UseCase -> Mapper: toUpdateResponse({entity})
    activate Mapper
    Mapper --> UseCase: {context['response_dto']}
    deactivate Mapper
    
    UseCase --> Controller: {context['response_dto']}
    deactivate UseCase
    
    Controller --> Client: HTTP {context['http_status']}
    deactivate Controller

else {entity} Not Found
    RepoAdapter --> RepoPort: Optional.empty()
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional.empty()
    deactivate RepoPort
    
    UseCase --> Controller: NotFoundException("{entity} not found")
    deactivate UseCase
    
    Controller --> Client: HTTP 404
    deactivate Controller
end

@enduml"""
        
        elif operation == "Delete":
            return f"""@startuml Delete {entity}
!theme plain
title Delete {entity} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: delete({entity_lower}Id)
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> RepoPort: findById({entity_lower}Id)
activate RepoPort
RepoPort -> RepoAdapter: findById({entity_lower}Id)
activate RepoAdapter
RepoAdapter -> JpaRepo: findById({entity_lower}Id)
activate JpaRepo
JpaRepo -> DB: SELECT * FROM {entity_lower}s WHERE id = ?
DB --> JpaRepo: Optional<{context['entity_dbo_name']}>
JpaRepo --> RepoAdapter: Optional<{context['entity_dbo_name']}>
deactivate JpaRepo

alt {entity} Found
    RepoAdapter -> Mapper: toDomain({context['entity_dbo_name']})
    activate Mapper
    Mapper --> RepoAdapter: {entity}
    deactivate Mapper
    
    RepoAdapter --> RepoPort: Optional<{entity}>
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional<{entity}>
    deactivate RepoPort
    
    UseCase -> RepoPort: deleteById({entity_lower}Id)
    activate RepoPort
    RepoPort -> RepoAdapter: deleteById({entity_lower}Id)
    activate RepoAdapter
    RepoAdapter -> JpaRepo: deleteById({entity_lower}Id)
    activate JpaRepo
    JpaRepo -> DB: DELETE FROM {entity_lower}s WHERE id = ?
    DB --> JpaRepo: void
    JpaRepo --> RepoAdapter: void
    deactivate JpaRepo
    RepoAdapter --> RepoPort: void
    deactivate RepoAdapter
    RepoPort --> UseCase: void
    deactivate RepoPort
    
    UseCase --> Controller: {context['response_dto']}
    deactivate UseCase
    
    Controller --> Client: HTTP {context['http_status']}
    deactivate Controller

else {entity} Not Found
    RepoAdapter --> RepoPort: Optional.empty()
    deactivate RepoAdapter
    RepoPort --> UseCase: Optional.empty()
    deactivate RepoPort
    
    UseCase --> Controller: NotFoundException("{entity} not found")
    deactivate UseCase
    
    Controller --> Client: HTTP 404
    deactivate Controller
end

@enduml"""
        
        elif operation == "List":
            return f"""@startuml List {entity}s
!theme plain
title List {entity}s - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: list()
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> RepoPort: findAll()
activate RepoPort
RepoPort -> RepoAdapter: findAll()
activate RepoAdapter
RepoAdapter -> JpaRepo: findAll()
activate JpaRepo
JpaRepo -> DB: SELECT * FROM {entity_lower}s
DB --> JpaRepo: List<{context['entity_dbo_name']}>
JpaRepo --> RepoAdapter: List<{context['entity_dbo_name']}>
deactivate JpaRepo

RepoAdapter -> Mapper: toDomainList(List<{context['entity_dbo_name']}>)
activate Mapper
Mapper --> RepoAdapter: List<{entity}>
deactivate Mapper

RepoAdapter --> RepoPort: List<{entity}>
deactivate RepoAdapter
RepoPort --> UseCase: List<{entity}>
deactivate RepoPort

UseCase -> Mapper: toListResponse(List<{entity}>)
activate Mapper
Mapper --> UseCase: {context['response_dto']}
deactivate Mapper

UseCase --> Controller: {context['response_dto']}
deactivate UseCase

Controller --> Client: HTTP {context['http_status']}
deactivate Controller

@enduml"""
        
        elif operation == "Search":
            title = context.get("operation_name", f"Search {entity}")
            return f"""@startuml {title}
!theme plain
title {title} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['service_class_name']}\\n(Application Service)" as Service
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}?query=searchTerm
activate Controller

Controller -> UseCase: search(searchTerm)
activate UseCase

UseCase -> Service: search(searchTerm)
activate Service

Service -> RepoPort: findBySearchTerm(searchTerm)
activate RepoPort
RepoPort -> RepoAdapter: findBySearchTerm(searchTerm)
activate RepoAdapter
RepoAdapter -> JpaRepo: findBySearchTerm(searchTerm)
activate JpaRepo
JpaRepo -> DB: SELECT * FROM {entity_lower}s WHERE ... LIKE '%searchTerm%'
DB --> JpaRepo: List<{context['entity_dbo_name']}>
JpaRepo --> RepoAdapter: List<{context['entity_dbo_name']}>
deactivate JpaRepo

RepoAdapter -> Mapper: toDomainList(List<{context['entity_dbo_name']}>)
activate Mapper
Mapper --> RepoAdapter: List<{entity}>
deactivate Mapper

RepoAdapter --> RepoPort: List<{entity}>
deactivate RepoAdapter
RepoPort --> Service: List<{entity}>
deactivate RepoPort

Service -> Mapper: toSearchResponse(List<{entity}>)
activate Mapper
Mapper --> Service: SearchResponse
deactivate Mapper

Service --> UseCase: SearchResponse
deactivate Service
UseCase --> Controller: SearchResponse
deactivate UseCase

Controller --> Client: HTTP {context['http_status']}
deactivate Controller

@enduml"""
        
        elif operation in ["Custom", "Validate", "Process", "Calculate"]:
            title = context.get("operation_name", f"{operation} {entity}")
            use_case_call = context.get("use_case_call", "customOperation")
            return f"""@startuml {title}
!theme plain
title {title} - Hexagonal Architecture Flow

actor Client
participant "{context['controller_name']}\\n(Input Adapter)" as Controller
participant "{context['use_case_name']}\\n(Domain Port)" as UseCase
participant "{context['service_class_name']}\\n(Application Service)" as Service
participant "{context['mapper_name']}\\n(Application Layer)" as Mapper
participant "{context['repository_port_name']}\\n(Domain Port)" as RepoPort
participant "{context['repository_adapter_name']}\\n(Output Adapter)" as RepoAdapter
participant "{context['jpa_repository_name']}\\n(Infrastructure)" as JpaRepo
database "Database" as DB

Client -> Controller: {context['http_method']} {context['endpoint']}
activate Controller

Controller -> UseCase: {use_case_call}()
activate UseCase
note right: UseCase is implemented by {context['service_class_name']}

UseCase -> UseCase: processBusinessLogic()
note right: Custom business logic for {title} operation

UseCase -> RepoPort: findRelatedData()
activate RepoPort
RepoPort -> RepoAdapter: findRelatedData()
activate RepoAdapter
RepoAdapter -> JpaRepo: findRelatedData()
activate JpaRepo
JpaRepo -> DB: SELECT related data
DB --> JpaRepo: List<RelatedDbo>
JpaRepo --> RepoAdapter: List<RelatedDbo>
deactivate JpaRepo
RepoAdapter --> RepoPort: List<RelatedDbo>
deactivate RepoAdapter
RepoPort --> UseCase: List<RelatedDbo>
deactivate RepoPort

UseCase -> Mapper: toResponse(List<RelatedDbo>)
activate Mapper
Mapper --> UseCase: {context.get('response_dto', 'CustomResponse')}
deactivate Mapper

UseCase --> Controller: {context.get('response_dto', 'CustomResponse')}
deactivate UseCase

Controller --> Client: HTTP {context['http_status']}
deactivate Controller

@enduml"""
        
        return ""