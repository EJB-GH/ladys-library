create table authors
(
    id           integer generated always as identity
        primary key,
    author_first varchar(50),
    author_last  varchar(50),
    unique (author_first, author_last)
);

alter table authors
    owner to postgres;

create table book_authors
(
    book_id   integer not null
        references old_books,
    author_id integer not null
        references authors,
    primary key (book_id, author_id)
);

alter table book_authors
    owner to postgres;

create table books
(
    id           integer generated always as identity
        constraint books_remake_pkey
            primary key,
    title        varchar(100) not null,
    series       varchar(50),
    genre        varchar(50),
    first_pub    date         not null,
    ver_edition  date         not null,
    author_first varchar(50)  not null,
    author_last  varchar(50)  not null,
    pub_name     varchar(100) not null
);

alter table books
    owner to postgres;
