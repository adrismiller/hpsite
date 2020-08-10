

CREATE TABLE books(
    id SERIAL PRIMARY KEY, 
    isbn VARCHAR NOT NULL, 
    title VARCHAR NOT NULL, 
    datep VARCHAR NOT NULL, 
    author VARCHAR NOT NULL 

); 

CREATE TABLE users( 
    user VARCHAR PRIMARY KEY,  
    pass VARCHAR NOT NULL
);

CREATE TABLE reviews(
    id SERIAL PRIMARY KEY 
    title VARCHAR NOT NULL , 
    user VARCHAR NOT NULL, 
    rating INTEGER NOT NULL,   
    review VARCHAR NOT NULL
);