-- Test Schema for H2 Database
-- Automatically loaded by Spring Boot for tests

-- Table: createmoviecontents
CREATE TABLE IF NOT EXISTS createmoviecontents (
    createmoviecontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: rentalcontents
CREATE TABLE IF NOT EXISTS rentalcontents (
    rentalcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: rentals
CREATE TABLE IF NOT EXISTS rentals (
    rental_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    movie_id VARCHAR(255) NOT NULL,
    user_id VARCHAR(255) NOT NULL,
    rental_date VARCHAR(255) NOT NULL,
    due_date VARCHAR(255) NOT NULL,
    total_price DOUBLE PRECISION NOT NULL,
    created_at VARCHAR(255),
    status VARCHAR(255) NOT NULL
);

-- Table: notfounderrorcontents
CREATE TABLE IF NOT EXISTS notfounderrorcontents (
    notfounderrorcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: moviecontents
CREATE TABLE IF NOT EXISTS moviecontents (
    moviecontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: deletemoviecontents
CREATE TABLE IF NOT EXISTS deletemoviecontents (
    deletemoviecontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: listrentalscontents
CREATE TABLE IF NOT EXISTS listrentalscontents (
    listrentalscontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: listmoviescontents
CREATE TABLE IF NOT EXISTS listmoviescontents (
    listmoviescontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: updatemoviecontents
CREATE TABLE IF NOT EXISTS updatemoviecontents (
    updatemoviecontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: updaterentalcontents
CREATE TABLE IF NOT EXISTS updaterentalcontents (
    updaterentalcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: conflicterrorcontents
CREATE TABLE IF NOT EXISTS conflicterrorcontents (
    conflicterrorcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: validationerrorcontents
CREATE TABLE IF NOT EXISTS validationerrorcontents (
    validationerrorcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

-- Table: movies
CREATE TABLE IF NOT EXISTS movies (
    movie_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    director VARCHAR(255) NOT NULL,
    genre VARCHAR(255) NOT NULL,
    release_year DOUBLE PRECISION NOT NULL,
    duration DOUBLE PRECISION NOT NULL,
    description VARCHAR(255),
    available_copies DOUBLE PRECISION NOT NULL,
    rental_price DOUBLE PRECISION NOT NULL,
    created_at VARCHAR(255),
    status VARCHAR(255) NOT NULL
);

-- Table: createrentalcontents
CREATE TABLE IF NOT EXISTS createrentalcontents (
    createrentalcontent_id UUID DEFAULT RANDOM_UUID() PRIMARY KEY,
    status VARCHAR(255) NOT NULL,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
