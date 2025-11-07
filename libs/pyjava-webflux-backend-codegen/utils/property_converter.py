"""
OpenAPI property converter for Java types and validation.
"""
import re
from typing import Dict, List, Any


class PropertyConverter:
    """Converts OpenAPI properties to Java properties with validation."""
    
    @staticmethod
    def camel_to_snake(name: str) -> str:
        """
        Convert camelCase to snake_case.
        
        Args:
            name: camelCase string
            
        Returns:
            snake_case string
        """
        # Insert underscore before uppercase letters that follow lowercase letters
        s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
        # Insert underscore before uppercase letters that follow lowercase letters or digits
        return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
    
    @staticmethod
    def convert_openapi_property(prop_name: str, prop_data: Dict[str, Any], required_fields: List[str]) -> Dict[str, Any]:
        """
        Convert OpenAPI property to Java property.
        
        Args:
            prop_name: Name of the property
            prop_data: OpenAPI property definition
            required_fields: List of required field names
            
        Returns:
            Dictionary containing Java property information
        """
        prop_type = prop_data.get('type', 'string')
        prop_format = prop_data.get('format')
        
        # Map OpenAPI types to Java types
        java_type = 'String'
        import_type = None
        
        if prop_type == 'string':
            if prop_format == 'date-time':
                java_type = 'OffsetDateTime'
                import_type = 'java.time.OffsetDateTime'
            else:
                java_type = 'String'
        elif prop_type == 'number':
            if prop_format == 'double':
                if prop_name in ['createdAt', 'updatedAt']:
                    java_type = 'String'
                else:
                    java_type = 'Double'
            else:
                java_type = 'BigDecimal'
                import_type = 'java.math.BigDecimal'
        elif prop_type == 'integer':
            java_type = 'Integer'
        elif prop_type == 'boolean':
            java_type = 'Boolean'
        elif prop_type == 'array':
            items = prop_data.get('items', {})
            if '$ref' in items:
                ref_type = items['$ref'].split('/')[-1]
                java_type = f'List<{ref_type}>'
            else:
                java_type = 'List<String>'
            import_type = 'java.util.List'
        
        # Build validation annotations
        validation_annotations = []
        if prop_name in required_fields:
            validation_annotations.append('@NotNull')
        
        if 'minLength' in prop_data:
            validation_annotations.append(f'@Size(min = {prop_data["minLength"]})')
        if 'maxLength' in prop_data:
            if 'minLength' in prop_data:
                validation_annotations[-1] = f'@Size(min = {prop_data["minLength"]}, max = {prop_data["maxLength"]})'  
            else:
                validation_annotations.append(f'@Size(max = {prop_data["maxLength"]})')
        
        if 'pattern' in prop_data:
            pattern = prop_data['pattern']
            if 'email' in prop_name.lower() or pattern == '^[^@]+@[^@]+\\.[^@]+$':
                pattern = '^[^@]+@[^@]+\\\\.[^@]+$'
            validation_annotations.append(f'@Pattern(regexp = "{pattern}")')
        
        return {
            'name': prop_name,
            'nameSnake': PropertyConverter.camel_to_snake(prop_name),
            'dataType': java_type,
            'datatypeWithEnum': java_type,
            'baseName': prop_name,
            'getter': f'get{prop_name.capitalize()}',
            'setter': f'set{prop_name.capitalize()}',
            'jsonProperty': prop_name,
            'required': prop_name in required_fields,
            'hasValidation': len(validation_annotations) > 0,
            'validationAnnotations': validation_annotations,
            'import': import_type
        }