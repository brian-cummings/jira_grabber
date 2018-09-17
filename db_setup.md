CREATE TABLE public.issue
(
    summary character varying(255) COLLATE pg_catalog."default",
    issuekey character varying(20) COLLATE pg_catalog."default" NOT NULL,
    issuetype character varying(50) COLLATE pg_catalog."default",
    status character varying(50) COLLATE pg_catalog."default",
    projectkey character varying(20) COLLATE pg_catalog."default",
    epiclink character varying(20) COLLATE pg_catalog."default",
    resolution character varying(50) COLLATE pg_catalog."default",
    created timestamp with time zone,
    updated timestamp with time zone,
    resolved timestamp with time zone,
    systemmodified timestamp with time zone,
    CONSTRAINT issue_pkey PRIMARY KEY (issuekey)
);

CREATE TABLE public.worklog
(
    id integer NOT NULL,
    issuekey character varying(20) COLLATE pg_catalog."default",
    comment character varying COLLATE pg_catalog."default",
    logdate timestamp with time zone,
    workdate timestamp with time zone,
    worker character varying(50) COLLATE pg_catalog."default",
    secondsworked bigint,
    systemmodified timestamp with time zone,
    CONSTRAINT worklog_pkey PRIMARY KEY (id)
);

CREATE TABLE public.jirauser
(
    id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    displayname character varying(255) COLLATE pg_catalog."default" NOT NULL,
    email character varying(255) COLLATE pg_catalog."default" NOT NULL,
    subscribed boolean DEFAULT false,
    active boolean,
    updated timestamp with time zone,
    lastemailed timestamp with time zone,
    CONSTRAINT user_pkey PRIMARY KEY (id)
);