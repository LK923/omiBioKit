CREATE TABLE orfs (
    id SERIAL PRIMARY KEY,
    seq_id TEXT NOT NULL,
    start_pos INT NOT NULL,
    end_pos INT NOT NULL,
    strand CHAR(1) NOT NULL,
    frame SMALLINT NOT NULL,
    length INT NOT NULL
);