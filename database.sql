--
-- PostgreSQL database dump
--

-- Dumped from database version 10.3
-- Dumped by pg_dump version 10.3

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: d_xml; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.d_xml (
    filepath text NOT NULL,
    xml xml
);


ALTER TABLE public.d_xml OWNER TO postgres;

--
-- Name: d_xml_data_advisory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.d_xml_data_advisory (
    filepath text NOT NULL,
    target_area_code text NOT NULL
);


ALTER TABLE public.d_xml_data_advisory OWNER TO postgres;

--
-- Name: d_xml_header; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.d_xml_header (
    filepath text NOT NULL,
    control_title text,
    head_infokind text,
    report_date_time timestamp without time zone
);


ALTER TABLE public.d_xml_header OWNER TO postgres;

--
-- Name: m_city_code; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.m_city_code (
    pref_code text,
    area_code text,
    city_code text NOT NULL,
    pref_name text,
    area_name text,
    city_name text
);


ALTER TABLE public.m_city_code OWNER TO postgres;

--
-- Name: d_xml_data_advisory d_xml_data_advisory_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.d_xml_data_advisory
    ADD CONSTRAINT d_xml_data_advisory_pkey PRIMARY KEY (filepath, target_area_code);


--
-- Name: d_xml_header d_xml_header_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.d_xml_header
    ADD CONSTRAINT d_xml_header_pkey PRIMARY KEY (filepath);


--
-- Name: d_xml d_xml_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.d_xml
    ADD CONSTRAINT d_xml_pkey PRIMARY KEY (filepath);


--
-- Name: m_city_code m_city_code_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.m_city_code
    ADD CONSTRAINT m_city_code_pkey PRIMARY KEY (city_code);


--
-- Name: idx_d_xml_header; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX idx_d_xml_header ON public.d_xml_header USING btree (control_title, head_infokind, report_date_time);


--
-- PostgreSQL database dump complete
--

