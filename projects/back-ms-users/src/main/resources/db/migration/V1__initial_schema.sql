-- back-ms-users.sql
-- SQL DDL for back-ms-users
-- Database: POSTGRESQL
-- Generated automatically from OpenAPI specification
-- Do not edit manually

-- Table for users
CREATE TABLE IF NOT EXISTS users (
    userId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier -- Unique identifier for the user account. Generated automatically upon creation
    username VARCHAR(255) NOT NULL UNIQUE, -- Users unique username. Cannot be changed after account creation
    email VARCHAR(255) NOT NULL UNIQUE, -- Users email address. Used for notifications and account recovery
    firstName VARCHAR(255), -- Users first name. May be null if not provided during registration
    lastName VARCHAR(255), -- Users last name. May be null if not provided during registration
    status VARCHAR(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL, -- Timestamp when the user account was created. ISO 8601 format
    updatedAt TIMESTAMPTZ NOT NULL -- Timestamp when the user account was last updated. ISO 8601 format
);

CREATE INDEX IF NOT EXISTS idx_users_username ON users (username); -- Users unique username. Cannot be changed after account creation

CREATE INDEX IF NOT EXISTS idx_users_email ON users (email); -- Users email address. Used for notifications and account recovery

CREATE INDEX IF NOT EXISTS idx_users_firstName ON users (firstName); -- Users first name. May be null if not provided during registration

CREATE INDEX IF NOT EXISTS idx_users_lastName ON users (lastName); -- Users last name. May be null if not provided during registration

CREATE INDEX IF NOT EXISTS idx_users_status ON users (status); -- Index for status field

-- Enumeration table for UserStatus
CREATE TABLE IF NOT EXISTS userstatuss (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Unique identifier
    code VARCHAR(50) NOT NULL UNIQUE, -- Enum code value
    name VARCHAR(100) NOT NULL, -- Human readable name
    description VARCHAR(255), -- Detailed description
    active BOOLEAN NOT NULL DEFAULT TRUE, -- Whether this enum value is active
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

-- Enum values
INSERT INTO userstatuss (code, name, description) VALUES ('ACTIVE', 'Active', 'UserStatus - Active') ON CONFLICT (code) DO NOTHING;
INSERT INTO userstatuss (code, name, description) VALUES ('INACTIVE', 'Inactive', 'UserStatus - Inactive') ON CONFLICT (code) DO NOTHING;
INSERT INTO userstatuss (code, name, description) VALUES ('SUSPENDED', 'Suspended', 'UserStatus - Suspended') ON CONFLICT (code) DO NOTHING;

-- back-ms-users-location.sql
-- SQL DDL for back-ms-users-location
-- Database: POSTGRESQL
-- Generated automatically from OpenAPI specification
-- Do not edit manually

-- Table for cities
CREATE TABLE IF NOT EXISTS cities (
    cityId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    regionId UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL,
    updatedAt TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_cities_name ON cities (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_cities_status ON cities (status); -- Index for status field

-- Table for countries
CREATE TABLE IF NOT EXISTS countries (
    countryId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL,
    updatedAt TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_countries_name ON countries (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_countries_status ON countries (status); -- Index for status field

-- Table for locations
CREATE TABLE IF NOT EXISTS locations (
    locationId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    userId UUID NOT NULL,
    country VARCHAR(255) NOT NULL,
    region VARCHAR(255) NOT NULL,
    city VARCHAR(255) NOT NULL,
    neighborhood VARCHAR(255),
    address VARCHAR(255) NOT NULL,
    postalCode VARCHAR(255),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    locationType VARCHAR(255) NOT NULL,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

CREATE INDEX IF NOT EXISTS idx_locations_status ON locations (status); -- Index for status field

-- Enumeration table for LocationType
CREATE TABLE IF NOT EXISTS locationtypes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Unique identifier
    code VARCHAR(50) NOT NULL UNIQUE, -- Enum code value
    name VARCHAR(100) NOT NULL, -- Human readable name
    description VARCHAR(255), -- Detailed description
    active BOOLEAN NOT NULL DEFAULT TRUE, -- Whether this enum value is active
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Record creation timestamp
    updated_at TIMESTAMPTZ -- Record last update timestamp
);

-- Enum values
INSERT INTO locationtypes (code, name, description) VALUES ('HOME', 'Home', 'LocationType - Home') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('WORK', 'Work', 'LocationType - Work') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('BILLING', 'Billing', 'LocationType - Billing') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('SHIPPING', 'Shipping', 'LocationType - Shipping') ON CONFLICT (code) DO NOTHING;
INSERT INTO locationtypes (code, name, description) VALUES ('OTHER', 'Other', 'LocationType - Other') ON CONFLICT (code) DO NOTHING;

-- Table for neighborhoods
CREATE TABLE IF NOT EXISTS neighborhoods (
    neighborhoodId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    cityId UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL,
    updatedAt TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_neighborhoods_name ON neighborhoods (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_neighborhoods_status ON neighborhoods (status); -- Index for status field

-- Table for regions
CREATE TABLE IF NOT EXISTS regions (
    regionId UUID DEFAULT gen_random_uuid() PRIMARY KEY, -- Primary key identifier
    name VARCHAR(255) NOT NULL,
    code VARCHAR(255) NOT NULL,
    countryId UUID NOT NULL,
    status VARCHAR(255) NOT NULL,
    createdAt TIMESTAMPTZ NOT NULL,
    updatedAt TIMESTAMPTZ NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_regions_name ON regions (name); -- Index for name field

CREATE INDEX IF NOT EXISTS idx_regions_status ON regions (status); -- Index for status field
