-- Archivo para importar la extructura database de supabase

-- Clean
DROP TABLE IF EXISTS public.sm_song_pack;
DROP TABLE IF EXISTS public.sm_pack;
DROP TABLE IF EXISTS public.sm_report;
DROP TABLE IF EXISTS public.sm_configuration;
DROP TABLE IF EXISTS public.sm_arcade_paths;
DROP TABLE IF EXISTS public.sm_arcade_credentials;
drop function if exists create_arcade;
drop function if exists publish_report;
drop function if exists latest_reports;
drop function if exists limit_max_reports;
drop function if exists create_pack;
drop function if exists update_pack;
drop function if exists update_program;
DROP TRIGGER IF EXISTS limit_reports ON sm_report;
DROP TYPE if exists log_level;

-- Structure and contraints
create table
  public.sm_arcade_paths (
    id bigint generated by default as identity,
    stepmania_songs_path text not null,
    downloads text not null,
    config text not null,
    program text not null,
    constraint sm_arcade_paths_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.sm_arcade_credentials (
    id bigint generated by default as identity,
    pixeldrain_key text not null,
    pixeldrain_secret text not null,
    constraint sm_arcade_credentials_pkey primary key (id)
  ) tablespace pg_default;

create table
  public.sm_configuration (
    id bigint generated by default as identity,
    name text not null,
    script_program text,
    realize smallint not null,
    so character varying not null,
    sm character varying not null,
    fk_credentials bigint not null,
    fk_paths bigint not null,
    constraint sm_configuration_pkey primary key (id),
    constraint sm_configuration_fk_credentials_fkey foreign key (fk_credentials) references sm_arcade_credentials (id) on update cascade on delete cascade,
    constraint sm_configuration_fk_paths_fkey foreign key (fk_paths) references sm_arcade_paths (id) on update cascade on delete cascade
  ) tablespace pg_default;

create table
  public.sm_pack (
    id bigint generated by default as identity,
    identifier text not null,
    password text not null,
    destination text not null,
    internal text not null,
    file text not null,
    formal_name text not null,
    compress boolean not null default true,
    sm_configuration_id bigint not null,
    constraint sm_pack_pkey primary key (id),
    constraint sm_configuration_id foreign key(sm_configuration_id) references sm_configuration(id)
  ) tablespace pg_default;

create table
  public.sm_song_pack (
    id bigint generated by default as identity,
    formal_name text not null,
    artist text not null,
    source text not null,
    sm_pack_id bigint not null,
    constraint sm_song_pack_pkey primary key (id),
    constraint sm_pack_id foreign key(sm_pack_id) references sm_pack(id)
  ) tablespace pg_default;

CREATE TYPE log_level AS ENUM ('Error', 'Info');

create table
  public.sm_report (
    id bigint generated by default as identity,
    instant timestamp with time zone not null default now(),
    message text not null,
    severity log_level NOT NULL,
    sm_configuration_id bigint not null,
    constraint sm_report_pkey primary key (id),
    constraint sm_configuration_id foreign key(sm_configuration_id) references sm_configuration(id)
  ) tablespace pg_default;

-- Policy data
create policy "sm_arcade_paths select"
on "public"."sm_arcade_paths"
to service_role
using (true);

create policy "sm_arcade_credentials select"
on "public"."sm_arcade_credentials"
to service_role
using (true);

create policy "sm_configuration select"
on "public"."sm_configuration"
to service_role
using (true);

create policy "sm_pack select"
on "public"."sm_pack"
to service_role
using (true);

create policy "sm_report select"
on "public"."sm_report"
to service_role
using (true);

-- Store procedures
create or replace function create_arcade(
    new_name text,
    new_operative_system text,
    new_stepmania_version text,
    new_pixeldrain_key text,
    new_pixeldrain_secret text,
    new_path_stepmania_songs_path text,
    new_path_downloads text,
    new_path_config text,
    new_path_program text)
returns VOID
language plpgsql
as $$
declare
    new_arcade_credentials_id bigint;
    new_arcade_paths_id bigint;
begin
    -- validate params
    IF EXISTS (SELECT 1 FROM sm_configuration WHERE name = new_name) THEN
        RAISE EXCEPTION 'The arcade with the name % already exist', new_name;
    END IF;
    -- obtain dependencies
    INSERT INTO public.sm_arcade_credentials(
        pixeldrain_key,
        pixeldrain_secret)
    VALUES(
        new_pixeldrain_key,
        new_pixeldrain_secret)
    RETURNING id INTO new_arcade_credentials_id;
    IF new_arcade_credentials_id IS NULL THEN
        RAISE EXCEPTION 'Error creating credentials';
    END IF;
    INSERT INTO public.sm_arcade_paths(
        stepmania_songs_path,
        downloads,
        config,
        program)
    VALUES(
        new_path_stepmania_songs_path,
        new_path_downloads,
        new_path_config,
        new_path_program)
    RETURNING id INTO new_arcade_paths_id;
    IF new_arcade_paths_id IS NULL THEN
        RAISE EXCEPTION 'Error creating paths';
    END IF;
    INSERT INTO public.sm_configuration(
        name,
        realize,
        script_program,
        so,
        sm,
        fk_credentials,
        fk_paths)
    VALUES(
        new_name,
        1,
        '',
        new_operative_system,
        new_stepmania_version,
        new_arcade_credentials_id,
        new_arcade_paths_id);
end;
$$;

create or replace function publish_report(
    configuration_name text,
    new_message text,
    new_severity log_level)
returns bigint
language plpgsql
as $$
declare
    configuration_id bigint;
    new_row bigint;
begin
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    select
        id into configuration_id
    from sm_configuration
    where name = configuration_name;
    insert into sm_report(message, severity, sm_configuration_id)
    values (new_message, new_severity, configuration_id)
    returning id into new_row;
    return new_row;
end;
$$;

create or replace function latest_reports(configuration_name text, reports_amount int)
RETURNS TABLE(instant_date TIMESTAMP WITH TIME ZONE, message_log text, severity log_level) AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    RETURN QUERY
    SELECT r.instant, r.message, r.severity
    FROM sm_report r, sm_configuration c
    where r.sm_configuration_id = c.id
    and c.name = configuration_name
    ORDER BY instant desc
    LIMIT reports_amount;
END;
$$ LANGUAGE plpgsql;

-- triggers and triggers functions
CREATE OR REPLACE FUNCTION limit_max_reports()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT COUNT(*) FROM sm_report WHERE sm_configuration_id = NEW.sm_configuration_id) >= 45 THEN
        DELETE FROM sm_report
        WHERE id = (
            SELECT id
            FROM sm_report
            ORDER BY instant ASC
            LIMIT 1
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER limit_reports
BEFORE INSERT ON sm_report
FOR EACH ROW
EXECUTE FUNCTION limit_max_reports();

create or replace function create_pack(
    configuration_name text,
    new_identifier text,
    new_password text,
    new_destination text,
    new_internal text,
    new_file text,
    new_formal_name text,
    new_compress boolean)
returns VOID
language plpgsql
as $$
declare
    configuration_id bigint;
begin
    -- validate params
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    -- obtain dependencies
    SELECT id
    INTO configuration_id
    FROM sm_configuration
    WHERE name = configuration_name;
    INSERT INTO public.sm_pack(
        identifier,
        password,
        destination,
        internal,
        file,
        formal_name,
        compress,
        sm_configuration_id)
    VALUES(
        new_identifier,
        new_password,
        new_destination,
        new_internal,
        new_file,
        new_formal_name,
        new_compress,
        configuration_id);
end;
$$;

create or replace function update_pack(
    configuration_name text,
    pack_identifier text,
    pack_formal_name text)
returns VOID
language plpgsql
as $$
declare
    configuration_id bigint;
begin
    -- validate params
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    -- obtain dependencies
    SELECT id
    INTO configuration_id
    FROM sm_configuration
    WHERE name = configuration_name;
    UPDATE sm_pack
    SET identifier = pack_identifier
    WHERE formal_name = pack_formal_name
    AND sm_configuration_id = configuration_id;
end;
$$;

create or replace function update_program(
    configuration_name text,
    program_identifier text)
returns VOID
language plpgsql
as $$
declare
    configuration_id bigint;
begin
    -- validate params
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    -- obtain dependencies
    SELECT id
    INTO configuration_id
    FROM sm_configuration
    WHERE name = configuration_name;
    UPDATE sm_configuration
    SET script_program = program_identifier
    WHERE id = configuration_id;
end;
$$;