--
-- PostgreSQL database dump
--

-- Dumped from database version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.10 (Ubuntu 10.10-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
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
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: asmi_group
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO asmi_group;

--
-- Name: generated_video; Type: TABLE; Schema: public; Owner: asmi_group
--

CREATE TABLE public.generated_video (
    gvideoid integer NOT NULL,
    filename character varying(300),
    storagelocation character varying(500),
    "createdTime" timestamp without time zone,
    video_id integer NOT NULL
);


ALTER TABLE public.generated_video OWNER TO asmi_group;

--
-- Name: generated_video_gvideoid_seq; Type: SEQUENCE; Schema: public; Owner: asmi_group
--

CREATE SEQUENCE public.generated_video_gvideoid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.generated_video_gvideoid_seq OWNER TO asmi_group;

--
-- Name: generated_video_gvideoid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asmi_group
--

ALTER SEQUENCE public.generated_video_gvideoid_seq OWNED BY public.generated_video.gvideoid;


--
-- Name: uploaded_video; Type: TABLE; Schema: public; Owner: asmi_group
--

CREATE TABLE public.uploaded_video (
    videoid integer NOT NULL,
    filename character varying(100),
    extension character varying(5),
    storagelocation character varying(500),
    "uploadStartedTime" timestamp without time zone,
    "uploadCompletedTime" timestamp without time zone
);


ALTER TABLE public.uploaded_video OWNER TO asmi_group;

--
-- Name: uploaded_video_videoid_seq; Type: SEQUENCE; Schema: public; Owner: asmi_group
--

CREATE SEQUENCE public.uploaded_video_videoid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.uploaded_video_videoid_seq OWNER TO asmi_group;

--
-- Name: uploaded_video_videoid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asmi_group
--

ALTER SEQUENCE public.uploaded_video_videoid_seq OWNED BY public.uploaded_video.videoid;


--
-- Name: video_analytics_file; Type: TABLE; Schema: public; Owner: asmi_group
--

CREATE TABLE public.video_analytics_file (
    analyticsfileid integer NOT NULL,
    filename character varying(300),
    storagelocation character varying(500),
    "createdTime" timestamp without time zone,
    video_id integer
);


ALTER TABLE public.video_analytics_file OWNER TO asmi_group;

--
-- Name: video_analytics_file_analyticsfileid_seq; Type: SEQUENCE; Schema: public; Owner: asmi_group
--

CREATE SEQUENCE public.video_analytics_file_analyticsfileid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.video_analytics_file_analyticsfileid_seq OWNER TO asmi_group;

--
-- Name: video_analytics_file_analyticsfileid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: asmi_group
--

ALTER SEQUENCE public.video_analytics_file_analyticsfileid_seq OWNED BY public.video_analytics_file.analyticsfileid;


--
-- Name: generated_video gvideoid; Type: DEFAULT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.generated_video ALTER COLUMN gvideoid SET DEFAULT nextval('public.generated_video_gvideoid_seq'::regclass);


--
-- Name: uploaded_video videoid; Type: DEFAULT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.uploaded_video ALTER COLUMN videoid SET DEFAULT nextval('public.uploaded_video_videoid_seq'::regclass);


--
-- Name: video_analytics_file analyticsfileid; Type: DEFAULT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.video_analytics_file ALTER COLUMN analyticsfileid SET DEFAULT nextval('public.video_analytics_file_analyticsfileid_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: asmi_group
--

COPY public.alembic_version (version_num) FROM stdin;
1e0228a5b060
\.


--
-- Data for Name: generated_video; Type: TABLE DATA; Schema: public; Owner: asmi_group
--

COPY public.generated_video (gvideoid, filename, storagelocation, "createdTime", video_id) FROM stdin;
1	20200120075720_generated_20200120075530dogvideo.mp4	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 07:57:20.468669	14
2	20200120110111_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 11:01:11.403431	15
3	20200120111612_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 11:16:12.927493	18
4	20200120131208_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 13:12:08.834137	19
5	20200120134556_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 13:45:56.69221	21
6	20200120135156_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 13:51:56.501125	22
7	20200120142347_generated_roadless	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-20 14:23:47.5679	24
8	20200122044637_generated_the cookie guy	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 04:46:37.554141	29
9	20200122121411_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 12:14:11.161777	31
10	20200122123747_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 12:37:47.150908	32
11	20200122125309_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 12:53:09.845178	33
12	20200122130219_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 13:02:19.996269	35
13	20200122130735_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-22 13:07:35.891923	36
14	20200125061809_generated_dogvideo	/home/sagar/workingDir/projectversion1/app/static/video/generated	2020-01-25 06:18:09.249036	37
\.


--
-- Data for Name: uploaded_video; Type: TABLE DATA; Schema: public; Owner: asmi_group
--

COPY public.uploaded_video (videoid, filename, extension, storagelocation, "uploadStartedTime", "uploadCompletedTime") FROM stdin;
14	20200120075530dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 07:55:30.477773	2020-01-20 07:55:30.6188
15	20200120105928dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 10:59:28.195426	2020-01-20 10:59:28.317939
16	20200120110750dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 11:07:50.170734	2020-01-20 11:07:50.371467
17	20200120110958dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 11:09:58.751286	2020-01-20 11:09:58.815751
18	20200120111437dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 11:14:37.250779	2020-01-20 11:14:37.353388
19	20200120130922dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 13:09:22.894343	2020-01-20 13:09:23.055656
20	20200120133925dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 13:39:25.917618	2020-01-20 13:39:26.013424
21	20200120134354dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 13:43:54.748201	2020-01-20 13:43:54.803478
22	20200120134954dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 13:49:54.513296	2020-01-20 13:49:54.668642
23	20200120140118road	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 14:01:18.537158	2020-01-20 14:01:20.174214
24	20200120141151roadless	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-20 14:11:51.963554	2020-01-20 14:11:52.176776
25	20200121121210tylervideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-21 12:12:10.90887	2020-01-21 12:12:12.316534
26	20200121133445tylervideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-21 13:34:45.291762	2020-01-21 13:34:46.632739
27	20200122035858tylervideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 03:58:58.27228	2020-01-22 03:59:01.579963
28	20200122042705tylervideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 04:27:05.417818	2020-01-22 04:27:06.260373
29	20200122043521the cookie guy	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 04:35:21.156866	2020-01-22 04:35:21.499916
30	20200122120810dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 12:08:10.595722	2020-01-22 12:08:10.747847
31	20200122121227dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 12:12:27.724568	2020-01-22 12:12:27.820772
32	20200122123540dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 12:35:40.171274	2020-01-22 12:35:40.344278
33	20200122125107dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 12:51:07.578444	2020-01-22 12:51:07.735386
34	20200122125846dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 12:58:46.210139	2020-01-22 12:58:46.319143
35	20200122130036dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 13:00:36.228407	2020-01-22 13:00:36.302928
36	20200122130519dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-22 13:05:19.539352	2020-01-22 13:05:19.604284
37	20200125061309dogvideo	mp4	/home/sagar/workingDir/projectversion1/app/static/video/uploaded	2020-01-25 06:13:09.054823	2020-01-25 06:13:09.380031
\.


--
-- Data for Name: video_analytics_file; Type: TABLE DATA; Schema: public; Owner: asmi_group
--

COPY public.video_analytics_file (analyticsfileid, filename, storagelocation, "createdTime", video_id) FROM stdin;
4	20200120075721dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 07:57:21.530175	14
5	20200120110111dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 11:01:11.287634	15
6	20200120111612dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 11:16:12.759737	18
7	20200120131208dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 13:12:08.595286	19
8	20200120134137dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 13:41:37.363913	20
9	20200120134556dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 13:45:56.490595	21
10	20200120135156dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 13:51:56.162905	22
11	20200120142346roadless.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-20 14:23:46.562736	24
12	20200122044636the cookie guy.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 04:46:36.597344	29
13	20200122121410dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 12:14:10.939751	31
14	20200122123746dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 12:37:46.917988	32
15	20200122125309dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 12:53:09.6563	33
16	20200122130219dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 13:02:19.829488	35
17	20200122130735dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-22 13:07:35.711575	36
18	20200125061808dogvideo.json	/home/sagar/workingDir/projectversion1/app/static/analyticsFolder/generated	2020-01-25 06:18:08.825092	37
\.


--
-- Name: generated_video_gvideoid_seq; Type: SEQUENCE SET; Schema: public; Owner: asmi_group
--

SELECT pg_catalog.setval('public.generated_video_gvideoid_seq', 14, true);


--
-- Name: uploaded_video_videoid_seq; Type: SEQUENCE SET; Schema: public; Owner: asmi_group
--

SELECT pg_catalog.setval('public.uploaded_video_videoid_seq', 37, true);


--
-- Name: video_analytics_file_analyticsfileid_seq; Type: SEQUENCE SET; Schema: public; Owner: asmi_group
--

SELECT pg_catalog.setval('public.video_analytics_file_analyticsfileid_seq', 18, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: generated_video generated_video_pkey; Type: CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.generated_video
    ADD CONSTRAINT generated_video_pkey PRIMARY KEY (gvideoid);


--
-- Name: uploaded_video uploaded_video_filename_key; Type: CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.uploaded_video
    ADD CONSTRAINT uploaded_video_filename_key UNIQUE (filename);


--
-- Name: uploaded_video uploaded_video_pkey; Type: CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.uploaded_video
    ADD CONSTRAINT uploaded_video_pkey PRIMARY KEY (videoid);


--
-- Name: video_analytics_file video_analytics_file_pkey; Type: CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.video_analytics_file
    ADD CONSTRAINT video_analytics_file_pkey PRIMARY KEY (analyticsfileid);


--
-- Name: ix_generated_video_createdTime; Type: INDEX; Schema: public; Owner: asmi_group
--

CREATE INDEX "ix_generated_video_createdTime" ON public.generated_video USING btree ("createdTime");


--
-- Name: ix_uploaded_video_uploadCompletedTime; Type: INDEX; Schema: public; Owner: asmi_group
--

CREATE INDEX "ix_uploaded_video_uploadCompletedTime" ON public.uploaded_video USING btree ("uploadCompletedTime");


--
-- Name: ix_uploaded_video_uploadStartedTime; Type: INDEX; Schema: public; Owner: asmi_group
--

CREATE INDEX "ix_uploaded_video_uploadStartedTime" ON public.uploaded_video USING btree ("uploadStartedTime");


--
-- Name: ix_video_analytics_file_createdTime; Type: INDEX; Schema: public; Owner: asmi_group
--

CREATE INDEX "ix_video_analytics_file_createdTime" ON public.video_analytics_file USING btree ("createdTime");


--
-- Name: video_analytics_file video_analytics_file_video_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: asmi_group
--

ALTER TABLE ONLY public.video_analytics_file
    ADD CONSTRAINT video_analytics_file_video_id_fkey FOREIGN KEY (video_id) REFERENCES public.uploaded_video(videoid);


--
-- PostgreSQL database dump complete
--

