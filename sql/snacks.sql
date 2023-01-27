--
-- PostgreSQL database dump
--

-- Dumped from database version 13.9 (Ubuntu 13.9-1.pgdg20.04+1)
-- Dumped by pg_dump version 13.9 (Ubuntu 13.9-1.pgdg20.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: bad_ingredients; Type: TABLE; Schema: public; Owner: ismaiana
--

CREATE TABLE public.bad_ingredients (
    ingredient_id integer NOT NULL,
    user_id integer NOT NULL,
    ingredient character varying
);


ALTER TABLE public.bad_ingredients OWNER TO ismaiana;

--
-- Name: bad_ingredients_ingredient_id_seq; Type: SEQUENCE; Schema: public; Owner: ismaiana
--

CREATE SEQUENCE public.bad_ingredients_ingredient_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.bad_ingredients_ingredient_id_seq OWNER TO ismaiana;

--
-- Name: bad_ingredients_ingredient_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ismaiana
--

ALTER SEQUENCE public.bad_ingredients_ingredient_id_seq OWNED BY public.bad_ingredients.ingredient_id;


--
-- Name: notsafe_snacks; Type: TABLE; Schema: public; Owner: ismaiana
--

CREATE TABLE public.notsafe_snacks (
    nsnack_id integer NOT NULL,
    user_id integer NOT NULL,
    snack_name character varying NOT NULL,
    snack_brand character varying NOT NULL,
    image character varying,
    bad_ingredients character varying
);


ALTER TABLE public.notsafe_snacks OWNER TO ismaiana;

--
-- Name: notsafe_snacks_nsnack_id_seq; Type: SEQUENCE; Schema: public; Owner: ismaiana
--

CREATE SEQUENCE public.notsafe_snacks_nsnack_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.notsafe_snacks_nsnack_id_seq OWNER TO ismaiana;

--
-- Name: notsafe_snacks_nsnack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ismaiana
--

ALTER SEQUENCE public.notsafe_snacks_nsnack_id_seq OWNED BY public.notsafe_snacks.nsnack_id;


--
-- Name: safe_snacks; Type: TABLE; Schema: public; Owner: ismaiana
--

CREATE TABLE public.safe_snacks (
    snack_id integer NOT NULL,
    user_id integer NOT NULL,
    snack_name character varying NOT NULL,
    snack_brand character varying NOT NULL,
    image character varying
);


ALTER TABLE public.safe_snacks OWNER TO ismaiana;

--
-- Name: safe_snacks_snack_id_seq; Type: SEQUENCE; Schema: public; Owner: ismaiana
--

CREATE SEQUENCE public.safe_snacks_snack_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.safe_snacks_snack_id_seq OWNER TO ismaiana;

--
-- Name: safe_snacks_snack_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ismaiana
--

ALTER SEQUENCE public.safe_snacks_snack_id_seq OWNED BY public.safe_snacks.snack_id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: ismaiana
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    fname character varying(20) NOT NULL,
    lname character varying(30) NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL
);


ALTER TABLE public.users OWNER TO ismaiana;

--
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: ismaiana
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_user_id_seq OWNER TO ismaiana;

--
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: ismaiana
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- Name: bad_ingredients ingredient_id; Type: DEFAULT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.bad_ingredients ALTER COLUMN ingredient_id SET DEFAULT nextval('public.bad_ingredients_ingredient_id_seq'::regclass);


--
-- Name: notsafe_snacks nsnack_id; Type: DEFAULT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.notsafe_snacks ALTER COLUMN nsnack_id SET DEFAULT nextval('public.notsafe_snacks_nsnack_id_seq'::regclass);


--
-- Name: safe_snacks snack_id; Type: DEFAULT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.safe_snacks ALTER COLUMN snack_id SET DEFAULT nextval('public.safe_snacks_snack_id_seq'::regclass);


--
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- Data for Name: bad_ingredients; Type: TABLE DATA; Schema: public; Owner: ismaiana
--

COPY public.bad_ingredients (ingredient_id, user_id, ingredient) FROM stdin;
1	1	sugar
\.


--
-- Data for Name: notsafe_snacks; Type: TABLE DATA; Schema: public; Owner: ismaiana
--

COPY public.notsafe_snacks (nsnack_id, user_id, snack_name, snack_brand, image, bad_ingredients) FROM stdin;
1	1	swiss rolls	Debbie	link	cocoa
\.


--
-- Data for Name: safe_snacks; Type: TABLE DATA; Schema: public; Owner: ismaiana
--

COPY public.safe_snacks (snack_id, user_id, snack_name, snack_brand, image) FROM stdin;
1	1	oat milk	kierland	link
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: ismaiana
--

COPY public.users (user_id, fname, lname, email, password) FROM stdin;
1	Ismaiana	Lima	ismaiana@test.com	123
\.


--
-- Name: bad_ingredients_ingredient_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ismaiana
--

SELECT pg_catalog.setval('public.bad_ingredients_ingredient_id_seq', 1, true);


--
-- Name: notsafe_snacks_nsnack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ismaiana
--

SELECT pg_catalog.setval('public.notsafe_snacks_nsnack_id_seq', 1, true);


--
-- Name: safe_snacks_snack_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ismaiana
--

SELECT pg_catalog.setval('public.safe_snacks_snack_id_seq', 1, true);


--
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: ismaiana
--

SELECT pg_catalog.setval('public.users_user_id_seq', 1, true);


--
-- Name: bad_ingredients bad_ingredients_pkey; Type: CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.bad_ingredients
    ADD CONSTRAINT bad_ingredients_pkey PRIMARY KEY (ingredient_id);


--
-- Name: notsafe_snacks notsafe_snacks_pkey; Type: CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.notsafe_snacks
    ADD CONSTRAINT notsafe_snacks_pkey PRIMARY KEY (nsnack_id);


--
-- Name: safe_snacks safe_snacks_pkey; Type: CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.safe_snacks
    ADD CONSTRAINT safe_snacks_pkey PRIMARY KEY (snack_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: bad_ingredients bad_ingredients_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.bad_ingredients
    ADD CONSTRAINT bad_ingredients_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: notsafe_snacks notsafe_snacks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.notsafe_snacks
    ADD CONSTRAINT notsafe_snacks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: safe_snacks safe_snacks_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: ismaiana
--

ALTER TABLE ONLY public.safe_snacks
    ADD CONSTRAINT safe_snacks_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

--testing something