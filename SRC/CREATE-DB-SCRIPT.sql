create table if not exists Movie (
    id char(9) not null,
    title varchar(200) not null,
    budget int,
    revenue bigint,
    releaseDate date,
    posterPath varchar(100),
    overview text,
    rating float(2),
    primary key (id),
    fulltext idx (title)
    ) engine=InnoDB;

create table if not exists Actor (
    id char(9) primary key,
    name varchar(100) not null,
    profilePath varchar(100),
    biography text,
    fulltext idx (name)
    ) engine=InnoDB;

create table if not exists Genre (
    id int primary key,
    name varchar(100) not null
    );

create table if not exists MovieActor (
    movieID char(9) not null,
    actorID char(9) not null,
    foreign key (movieID) references Movie(id),
    foreign key (actorID) references Actor(id)
    );

create table if not exists MovieGenre (
    movieID char(9) not null,
    genreID int not null,
    foreign key (movieID) references Movie(id),
    foreign key (genreID) references Genre(id)
    );