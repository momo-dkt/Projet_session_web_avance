
    CREATE TABLE IF NOT EXISTS lieu_baignade(
        id integer primary key,
        arrondissement varchar(50),
        nom varchar(50),
        genre varchar(50),
        adresse varchar(50)
    );
    
    CREATE TABLE IF NOT EXISTS patinoire (
        id integer primary key,
        arrondissement varchar(50),
        nom vachar(50),
        mise_a_jour varchar(20),
        ouvert varchar(10),
        deblaye varchar(10)
    );
    
    CREATE TABLE IF NOT EXISTS glissade(
        id integer primary key,
        arrondissement varchar(50),
        nom varchar(50),
        ouvert integer,
        deblaye integer,
        mise_a_jour varchar(10)
    );
    