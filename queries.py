CREATE TABLE books (
    id              TEXT PRIMARY KEY,
    title           TEXT NOT NULL,
    author          TEXT NOT NULL,
    total_copies    INT  NOT NULL,
    available_copies INT NOT NULL,
    rent_price      INT  NOT NULL
);

CREATE TABLE members (
    id     TEXT PRIMARY KEY,
    name   TEXT NOT NULL,
    email  TEXT NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE borrowed_books (
    id          TEXT PRIMARY KEY,
    book_id     TEXT NOT NULL REFERENCES books(id),
    borrowed_at TIMESTAMP NOT NULL,
    is_return   BOOLEAN NOT NULL DEFAULT FALSE,
    due_date    TIMESTAMP NOT NULL,
    total_amt   INT NOT NULL
);

CREATE TABLE transactions (
    id                 TEXT PRIMARY KEY,
    member_id          TEXT NOT NULL REFERENCES members(id),
    book_id            TEXT NOT NULL REFERENCES books(id),
    is_penalty_applied BOOLEAN NOT NULL DEFAULT FALSE,
    penalty_amt        INT NOT NULL DEFAULT 0,
    total_amt          INT NOT NULL
    is_return          BOOLEAN NOT NULL DEFAULT FALSE
);