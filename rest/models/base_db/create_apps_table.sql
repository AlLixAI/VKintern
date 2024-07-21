CREATE TABLE apps (
    uuid UUID PRIMARY KEY,
    kind VARCHAR(32) NOT NULL,
    name VARCHAR(128) NOT NULL,
    version VARCHAR(32) NOT NULL,
    description VARCHAR(4096),
    state VARCHAR(20) DEFAULT 'NEW' CHECK (state IN ('NEW', 'INSTALLING', 'RUNNING')),
    json JSON
);