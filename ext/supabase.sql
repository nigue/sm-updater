-- Archivo para importar la extructura database de supabase

-- Clean
DROP TABLE IF EXISTS public.sm_pack;
DROP TABLE IF EXISTS public.sm_report;
DROP TABLE IF EXISTS public.sm_configuration;
DROP TABLE IF EXISTS public.sm_arcade_paths;
DROP TABLE IF EXISTS public.sm_arcade_credentials;
drop function if exists publish_report(configuration_name, message);
drop function if exists latest_reports(reports_amount);
drop function if exists update_pack(configuration_name, pack_name, new_pack_identifier);

-- Structure and contraints
create table
  public.sm_arcade_paths (
    id bigint generated by default as identity,
    sm text not null,
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
    compress boolean not null default true,
    sm_configuration_id bigint not null,
    constraint sm_pack_pkey primary key (id),
    constraint sm_configuration_id foreign key(sm_configuration_id) references sm_configuration(id)
  ) tablespace pg_default;

create table
  public.sm_report (
    id bigint generated by default as identity,
    instant timestamp with time zone not null default now(),
    message text not null,
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

-- Initial data
INSERT INTO public.sm_arcade_paths(
    sm,
    downloads,
    config,
    program)
VALUES(
    '/opt/NotITG-v4.2.0',
    '/opt/Downloads',
    '/opt/Downloads/sm_sync_config.json',
    '/opt/SmScript');

INSERT INTO public.sm_arcade_credentials(
    pixeldrain_key,
    pixeldrain_secret)
VALUES(
    '1234',
    'asdf');

INSERT INTO public.sm_configuration(
    name,
    realize,
    so,
    sm,
    fk_credentials,
    fk_paths)
VALUES(
    'arcade_center',
    1,
    'linux',
    'ITGmania',
    1,
    1);

INSERT INTO public.sm_pack(
    identifier,
    password,
    destination,
    internal,
    file,
    compress,
    sm_configuration_id)
VALUES(
    'iden',
    'pass',
    'Packages',
    'Songs',
    'srgsgdftz.zip',
    true,
    1);

INSERT INTO public.sm_report(
    instant,
    message,
    sm_configuration_id)
VALUES(
    '2024-07-28 16:12:12+00',
    'text',
    1);

-- Store procedures
create or replace function publish_report(configuration_name text, message text)
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
    insert into sm_report(instant, message, sm_configuration_id)
    values (NOW(), message, configuration_id)
    returning id into new_row;
    return new_row;
end;
$$;

create or replace function latest_reports(configuration_name text, reports_amount int)
RETURNS TABLE(instant_date TIMESTAMP WITH TIME ZONE, message_log text) AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM sm_configuration WHERE name = configuration_name) THEN
        RAISE EXCEPTION 'The arcade with the name % does not exist', configuration_name;
    END IF;
    RETURN QUERY
    SELECT r.instant, r.message
    FROM sm_report r, sm_configuration c
    where r.sm_configuration_id = c.id
    and c.name = configuration_name
    ORDER BY instant asc
    LIMIT reports_amount;
END;
$$ LANGUAGE plpgsql;

--drop function if exists update_pack(configuration_name, pack_name, pack_identifier)
