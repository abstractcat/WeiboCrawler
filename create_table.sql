-- Table: repost

-- DROP TABLE repost;

CREATE TABLE repost
(
  root_mid character(16) NOT NULL,
  repost_mid character(16) NOT NULL,
  uid character(10),
  content character varying,
  tm timestamp without time zone,
  repost_num integer,
  comment_num integer,
  like_num integer,
  CONSTRAINT repost_pk PRIMARY KEY (root_mid, repost_mid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE repost
  OWNER TO postgres;


-- Table: "user"

-- DROP TABLE "user";

CREATE TABLE "user"
(
  uid character(10) NOT NULL,
  name character varying,
  follow_num integer,
  fan_num integer,
  post_num integer,
  verify boolean,
  CONSTRAINT user_pk PRIMARY KEY (uid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE "user"
  OWNER TO postgres;


-- Table: weibo

-- DROP TABLE weibo;

CREATE TABLE weibo
(
  mid character(16) NOT NULL,
  uid character(10),
  content character varying,
  tm timestamp without time zone,
  repost_num integer,
  comment_num integer,
  like_num integer,
  CONSTRAINT weibo_pk PRIMARY KEY (mid)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE weibo
  OWNER TO postgres;
