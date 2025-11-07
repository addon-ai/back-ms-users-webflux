-- back-ms-users.sql
-- SQL DDL for back-ms-users
-- Database: POSTGRESQL
-- Generated automatically from OpenAPI specification
-- Do not edit manually

-- Table for users
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'users') THEN
        CREATE TABLE public."users" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "user_id" UUID NOT NULL,
  "username" VARCHAR(255) NOT NULL UNIQUE,
  "email" VARCHAR(255) NOT NULL UNIQUE,
  "firstName" VARCHAR(255),
  "lastName" VARCHAR(255),
  "status" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL,
  "updatedAt" TIMESTAMPTZ NOT NULL
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_users_username" ON "users" ("username");
CREATE INDEX IF NOT EXISTS "idx_users_email" ON "users" ("email");
CREATE INDEX IF NOT EXISTS "idx_users_firstName" ON "users" ("firstName");
CREATE INDEX IF NOT EXISTS "idx_users_lastName" ON "users" ("lastName");
CREATE INDEX IF NOT EXISTS "idx_users_status" ON "users" ("status");

-- Enumeration table for UserStatus
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'userstatuss') THEN
        CREATE TABLE public."userstatuss" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "code" VARCHAR(50) NOT NULL UNIQUE,
  "name" VARCHAR(100) NOT NULL,
  "description" VARCHAR(255),
  "active" BOOLEAN NOT NULL DEFAULT TRUE,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ
            );
    END IF;
END$$;

-- Enum values
INSERT INTO "userstatuss" (code, name, description) VALUES ('ACTIVE', 'Active', 'UserStatus - Active') ON CONFLICT (code) DO NOTHING;
INSERT INTO "userstatuss" (code, name, description) VALUES ('INACTIVE', 'Inactive', 'UserStatus - Inactive') ON CONFLICT (code) DO NOTHING;
INSERT INTO "userstatuss" (code, name, description) VALUES ('SUSPENDED', 'Suspended', 'UserStatus - Suspended') ON CONFLICT (code) DO NOTHING;

-- Table for cities
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'cities') THEN
        CREATE TABLE public."cities" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "city_id" UUID NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "region_id" UUID NOT NULL,
  "status" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL,
  "updatedAt" TIMESTAMPTZ NOT NULL
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_cities_name" ON "cities" ("name");
CREATE INDEX IF NOT EXISTS "idx_cities_status" ON "cities" ("status");

-- Table for countries
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'countries') THEN
        CREATE TABLE public."countries" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "country_id" UUID NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "code" VARCHAR(255) NOT NULL,
  "status" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL,
  "updatedAt" TIMESTAMPTZ NOT NULL
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_countries_name" ON "countries" ("name");
CREATE INDEX IF NOT EXISTS "idx_countries_status" ON "countries" ("status");

-- Table for locations
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'locations') THEN
        CREATE TABLE public."locations" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "location_id" UUID NOT NULL,
  "user_id" UUID NOT NULL,
  "country" VARCHAR(255) NOT NULL,
  "region" VARCHAR(255) NOT NULL,
  "city" VARCHAR(255) NOT NULL,
  "neighborhood" VARCHAR(255),
  "address" VARCHAR(255) NOT NULL,
  "postalCode" VARCHAR(255),
  "latitude" DOUBLE PRECISION,
  "longitude" DOUBLE PRECISION,
  "locationType" VARCHAR(255) NOT NULL,
  "status" VARCHAR(255) NOT NULL,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_locations_status" ON "locations" ("status");

-- Enumeration table for LocationType
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'locationtypes') THEN
        CREATE TABLE public."locationtypes" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "code" VARCHAR(50) NOT NULL UNIQUE,
  "name" VARCHAR(100) NOT NULL,
  "description" VARCHAR(255),
  "active" BOOLEAN NOT NULL DEFAULT TRUE,
  "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "updated_at" TIMESTAMPTZ
            );
    END IF;
END$$;

-- Enum values
INSERT INTO "locationtypes" (code, name, description) VALUES ('HOME', 'Home', 'LocationType - Home') ON CONFLICT (code) DO NOTHING;
INSERT INTO "locationtypes" (code, name, description) VALUES ('WORK', 'Work', 'LocationType - Work') ON CONFLICT (code) DO NOTHING;
INSERT INTO "locationtypes" (code, name, description) VALUES ('BILLING', 'Billing', 'LocationType - Billing') ON CONFLICT (code) DO NOTHING;
INSERT INTO "locationtypes" (code, name, description) VALUES ('SHIPPING', 'Shipping', 'LocationType - Shipping') ON CONFLICT (code) DO NOTHING;
INSERT INTO "locationtypes" (code, name, description) VALUES ('OTHER', 'Other', 'LocationType - Other') ON CONFLICT (code) DO NOTHING;

-- Table for neighborhoods
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'neighborhoods') THEN
        CREATE TABLE public."neighborhoods" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "neighborhood_id" UUID NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "city_id" UUID NOT NULL,
  "status" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL,
  "updatedAt" TIMESTAMPTZ NOT NULL
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_neighborhoods_name" ON "neighborhoods" ("name");
CREATE INDEX IF NOT EXISTS "idx_neighborhoods_status" ON "neighborhoods" ("status");

-- Table for regions
DO $$
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'regions') THEN
        CREATE TABLE public."regions" (
              "id" UUID DEFAULT gen_random_uuid() PRIMARY KEY,
  "region_id" UUID NOT NULL,
  "name" VARCHAR(255) NOT NULL,
  "code" VARCHAR(255) NOT NULL,
  "country_id" UUID NOT NULL,
  "status" VARCHAR(255) NOT NULL,
  "createdAt" TIMESTAMPTZ NOT NULL,
  "updatedAt" TIMESTAMPTZ NOT NULL
            );
    END IF;
END$$;

CREATE INDEX IF NOT EXISTS "idx_regions_name" ON "regions" ("name");
CREATE INDEX IF NOT EXISTS "idx_regions_status" ON "regions" ("status");