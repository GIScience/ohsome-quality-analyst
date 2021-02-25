--
-- PostgreSQL database dump
--

-- Dumped from database version 10.15 (Ubuntu 10.15-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 12.4

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

--
-- Name: test_regions; Type: TABLE; Schema: public; Owner: oqt
--

CREATE TABLE public.test_regions (
    ogc_fid integer NOT NULL,
    fid integer,
    infile character varying,
    geom public.geometry(Polygon,4326)
);


ALTER TABLE public.test_regions OWNER TO oqt;

--
-- Name: test_regions_ogc_fid_seq; Type: SEQUENCE; Schema: public; Owner: oqt
--

CREATE SEQUENCE public.test_regions_ogc_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.test_regions_ogc_fid_seq OWNER TO oqt;

--
-- Name: test_regions_ogc_fid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: oqt
--

ALTER SEQUENCE public.test_regions_ogc_fid_seq OWNED BY public.test_regions.ogc_fid;


--
-- Name: test_regions ogc_fid; Type: DEFAULT; Schema: public; Owner: oqt
--

ALTER TABLE ONLY public.test_regions ALTER COLUMN ogc_fid SET DEFAULT nextval('public.test_regions_ogc_fid_seq'::regclass);


--
-- Data for Name: test_regions; Type: TABLE DATA; Schema: public; Owner: oqt
--

COPY public.test_regions (ogc_fid, fid, infile, geom) FROM stdin;
1	0	alger_biskra_bad.geojson	0103000020E6100000010000000500000000000080CDD716406C115050856A414000000080DDE516406C115050856A414000000080DDE516405FA635D5426C414000000080CDD716405FA635D5426C414000000080CDD716406C115050856A4140
2	1	Alger_djanet_bad.geojson	0103000020E61000000100000005000000000000C092F42240BD4FEC4A5E8C3840000000B05FFB2240BD4FEC4A5E8C3840000000B05FFB22408DF5079206903840000000C092F422408DF5079206903840000000C092F42240BD4FEC4A5E8C3840
3	2	Alger_Kenadsa_medium.geojson	0103000020E6100000010000000500000000000060C2451F40C546B0DDDEB72B40010000005C571F40C546B0DDDEB72B40010000005C571F406CE9DA55BDBE2B4000000060C2451F406CE9DA55BDBE2B4000000060C2451F40C546B0DDDEB72B40
4	3	Alger_tougourt_bad.geojson	0103000020E610000001000000170000000000000092461840BBE378C91B94404000000000B2351840F1F3CA89B7914040000000002F2218409D457DC84191404000000000B71218407121ED33118F4040000000009D1D1840B9EB3587BF8C4040000000003D2318409FE68CA199894040FFFFFFFFE72C1840B0993AF42988404000000000BA3C1840A17F91F2DF86404000000000164A184073DAB03ACA884040000000002F4F1840E41E9704698A404000000000F1501840F1D1B7E8D38B404000000000B94C184023003F1E958C4040000000001A6418400CB8873DC48C404000000000B26218408CD3355BD28F4040000000002B621840B049943FBC914040000000003F5D1840B0BBD6ED97934040000000003D5018404C08D699C0944040FFFFFFFFDD451840911C68D1C196404000000000A93E18407C945987F8974040000000001D34184011FC1774C997404000000000553818400E353BC88F95404000000000333C18401E57B48C709440400000000092461840BBE378C91B944040
5	4	antanarivo.geojson	0103000020E61000000100000005000000000000807BBF474095A154C186F232C0000000C0F6C7474095A154C186F232C0000000C0F6C747403674D63873DC32C0000000807BBF47403674D63873DC32C0000000807BBF474095A154C186F232C0
6	5	CH_Basel_Stadt_good.geojson	0103000020E6100000010000000E00000000000000AA551E4068F796D3B4C94740FFFFFFFF53421E401336E30E9EC94740FFFFFFFF3D3A1E407F6671CFE5C7474000000000DE3F1E406CD88A53D2C54740FFFFFFFF33531E408CA71E8CA2C44740FFFFFFFF51621E4057AC1F0378C2474000000000807F1E40C9258817F6C44740FFFFFFFF358D1E4092235C1E83C74740FFFFFFFF21BF1E40FFD7127F48C84740FFFFFFFF0DC41E401BD96B1DD9CC47400000000068971E4081D302CE39CC474001000000766B1E402D7BD37D19CB4740FFFFFFFF495B1E4007491E4E8BCB474000000000AA551E4068F796D3B4C94740
7	6	CH_Lampenberg_good.geojson	0103000020E6100000010000000C000000FFFFFFFF12FB1E40055A98C44DB84740FFFFFF7F02F51E4036459381CAB7474000000080C2E91E40DCB5C6CFEDB64740FFFFFF7FE8FF1E40F26C1FF927B44740FFFFFFFF021A1F40C98B2C666EB4474000000000951E1F40230F5E67E4B44740010000800D261F4004DDBBC07AB547400000000029301F40B9EF6EF6FFB5474000000080143D1F407CE69FD289B7474000000080F92A1F40D6BC07703DB94740FFFFFFFFE9141F40670C351B6EB84740FFFFFFFF12FB1E40055A98C44DB84740
8	7	dar_es_salaam.geojson	0103000020E61000000100000005000000000000C0829A43404A8D656FA3871BC0000000409BA743404A8D656FA3871BC0000000409BA74340500579992AF81AC0000000C0829A4340500579992AF81AC0000000C0829A43404A8D656FA3871BC0
9	8	DE_Aschaffenburg_good.geojson	0103000020E610000001000000050000000000008052392240BAC087214AF9484000000080A75C2240BAC087214AF9484000000080A75C22400FB5610307FF484000000080523922400FB5610307FF48400000008052392240BAC087214AF94840
10	9	De_Hornbach_good.geojson	0103000020E6100000010000000500000001000000FF6A1D408FA736B0009548400000000010961D408FA736B0009548400000000010961D4020A2992FAC98484001000000FF6A1D4020A2992FAC98484001000000FF6A1D408FA736B000954840
11	10	DE_Schopfheim_good.geojson	0103000020E61000000100000005000000FFFFFFFFD7261F40925714157ECC47400000000020C01F40925714157ECC47400000000020C01F40216B92BD11D84740FFFFFFFFD7261F40216B92BD11D84740FFFFFFFFD7261F40925714157ECC4740
12	11	DE_Stuttgart_mitte-süd_good.geojson	0103000020E61000000100000005000000000000087F57224012BBAF2F4C624840000000F0AF5C224012BBAF2F4C624840000000F0AF5C22407592BB2817634840000000087F5722407592BB2817634840000000087F57224012BBAF2F4C624840
13	13	Grec_Athen_medium.geojson	0103000020E6100000010000000500000000000000AC873740DD8BD0DF0DEB4240FFFFFFFF89E53740DD8BD0DF0DEB4240FFFFFFFF89E5374075C5106B5616434000000000AC87374075C5106B5616434000000000AC873740DD8BD0DF0DEB4240
14	14	heidelberg_altstadt.geojson	0103000020E61000000100000005000000000000A02259214055FEE72ABFB34840000000804664214055FEE72ABFB348400000008046642140E62667D030B54840000000A022592140E62667D030B54840000000A02259214055FEE72ABFB34840
15	15	IT_genoa_good.geojson	0103000020E61000000100000005000000000000C058D52140F058C63493314640000000004CED2140F058C63493314640000000004CED2140929F646813354640000000C058D52140929F646813354640000000C058D52140F058C63493314640
16	16	jamaica_hot_project_9142.geojson	0103000020E6100000010000000500000000000040CC3A53C0D20438CAD8ED3140000000A0183453C0D20438CAD8ED3140000000A0183453C063F42BCB6F0A324000000040CC3A53C063F42BCB6F0A324000000040CC3A53C0D20438CAD8ED3140
17	17	Jp_tokyo_good.geojson	0103000020E61000000100000005000000000000945C76614018CC1FB9CDCF4140000000A45978614018CC1FB9CDCF4140000000A45978614021DC36EB3FD54140000000945C76614021DC36EB3FD54140000000945C76614018CC1FB9CDCF4140
18	18	kadoma_zimbabwe.geojson	0103000020E61000000100000005000000000000800BDE3D4012240950AE6032C000000080F3F53D4012240950AE6032C000000080F3F53D40E9950932934C32C0000000800BDE3D40E9950932934C32C0000000800BDE3D4012240950AE6032C0
19	19	kano_city_nigeria.geojson	0103000020E61000000100000005000000000000408BF62040E3D6E5BD37F2274000000040DB0F2140E3D6E5BD37F2274000000040DB0F21407AFBB39990102840000000408BF620407AFBB39990102840000000408BF62040E3D6E5BD37F22740
20	20	kathmandu.geojson	0103000020E61000000100000005000000000000B04252554064919CA0DBAA3B40FFFFFF6F2357554064919CA0DBAA3B40FFFFFF6F2357554087E22BC345BE3B40000000B04252554087E22BC345BE3B40000000B04252554064919CA0DBAA3B40
21	21	Mali_Agarzane_bad.geojson	0103000020E61000000100000005000000FEFFFFBF24690B404AAC1B5104083040FFFFFFFF827F0B404AAC1B5104083040FFFFFFFF827F0B40293785EC100C3040FEFFFFBF24690B40293785EC100C3040FEFFFFBF24690B404AAC1B5104083040
22	22	Mali_Razelma_bad.geojson	0103000020E6100000010000000500000000000000DFE111C0EB9AA3308C96304000000080F2B711C0EB9AA3308C96304000000080F2B711C033DBC623649E304000000000DFE111C033DBC623649E304000000000DFE111C0EB9AA3308C963040
23	23	Monaco_good.geojson	0103000020E61000000100000005000000FFFFFFFFB2981D40D469266441DC454000000000DACB1D40D469266441DC454000000000DACB1D40DE1195B349E04540FFFFFFFFB2981D40DE1195B349E04540FFFFFFFFB2981D40D469266441DC4540
24	24	Moroq_Fnideq_medium.geojson	0103000020E61000000100000005000000000000805B8715C039CE3F7212E9414000000000A55415C039CE3F7212E9414000000000A55415C05252F99CB5EE4140000000805B8715C05252F99CB5EE4140000000805B8715C039CE3F7212E94140
25	25	muang_xay_myanmar.geojson	0103000020E6100000010000000500000000000020847E5940A81F200B1BAD3440000000D4EC7F5940A81F200B1BAD3440000000D4EC7F5940E6B92F8087B3344000000020847E5940E6B92F8087B3344000000020847E5940A81F200B1BAD3440
26	26	Nigeria_Lafia_bad.geojson	0103000020E6100000010000000500000000000000F19C27402F6608557B44234000000000FBB027402F6608557B44234000000000FBB02740D096ECCBCD57234000000000F19C2740D096ECCBCD57234000000000F19C27402F6608557B442340
27	27	Nigeria_lokoja_medium.geojson	0103000020E6100000010000000500000000000080D8E61A404BA8D7F858261F40010000401D001B404BA8D7F858261F40010000401D001B40C10570E5AF3F1F4000000080D8E61A40C10570E5AF3F1F4000000080D8E61A404BA8D7F858261F40
28	28	Niger_Kanan_Bakache_bad.geojson	0103000020E6100000010000000500000000000060C2451F40C546B0DDDEB72B40010000005C571F40C546B0DDDEB72B40010000005C571F406CE9DA55BDBE2B4000000060C2451F406CE9DA55BDBE2B4000000060C2451F40C546B0DDDEB72B40
29	29	Niger_Zinder_small_part_good.geojson	0103000020E61000000100000005000000FFFFFF87920022406B2C95C4469F2B40000000F8B9FF2140F3407CC4C79E2B40000000000A0222404E617F51209B2B4000000098E9022240E4C40571B29B2B40FFFFFF87920022406B2C95C4469F2B40
30	30	Phil_Manila_medium.geojson	0103000020E61000000100000005000000000000C8363D5E407899DFFF10332D40FFFFFF03173F5E407899DFFF10332D40FFFFFF03173F5E4091A7EC9496412D40000000C8363D5E4091A7EC9496412D40000000C8363D5E407899DFFF10332D40
31	31	Tun_Borj_Bourguiba_good.geojson	0103000020E6100000010000000500000000000040700E24409C99BC62E619404000000090861124409C99BC62E619404000000090861124408F7E75F1ED1A404000000040700E24408F7E75F1ED1A404000000040700E24409C99BC62E6194040
32	32	Tun_douriet_bad.geojson	0103000020E610000001000000050000000000009885912440B423B6C9756D40400000003869952440B423B6C9756D40400000003869952440CBB98347EE6D40400000009885912440CBB98347EE6D40400000009885912440B423B6C9756D4040
33	33	Tun_Remada_medium.geojson	0103000020E610000001000000050000000000005089C624404675DB20EB274040000000D0E5CB24404675DB20EB274040000000D0E5CB2440DD9C0455D72840400000005089C62440DD9C0455D72840400000005089C624404675DB20EB274040
34	34	Tun_Sfax_part_good.geojson	0103000020E61000000100000006000000FFFFFF9FCF7A2540B40B21C2E25E4140000000E0A780254056F9715BA45E414000000000B3822540A48DFA662A5F414000000060DD7F2540397E9D520160414000000080FC7C2540A1B14A4F8A5F4140FFFFFF9FCF7A2540B40B21C2E25E4140
35	35	Tun_Tunis_center_medium.geojson	0103000020E61000000100000005000000000000F092592440E95BBBBF5B654240FFFFFF7F73612440E95BBBBF5B654240FFFFFF7F7361244063CDB44347674240000000F09259244063CDB44347674240000000F092592440E95BBBBF5B654240
36	36	UK_London_Westminster_good.geojson	0103000020E610000001000000070000000000000000A4BFBF53F9CF643EC0494005000000609CC2BF70A190DAE6BF49400E00000020F9C3BFCDD82E9B57BE49400000000000CFC2BF5027E7E55EBD4940FBFFFFFF9F31C0BFF48EDE9D65BE4940F7FFFFFF3F47BEBF24F6024A6CBF49400000000000A4BFBF53F9CF643EC04940
37	37	US_NewYork_Manhatten_Harlem.geojson	0103000020E6100000010000000C000000000000604E7B52C0A7A434E51C704440000000A0CC8052C0F71AE8F6E9604440000000E05E8152C0C5954B25E359444000000040788052C06B2109366359444000000020137E52C0AAAE3B0CF45A444000000040A87D52C09DC024D78C5E444000000020327D52C0E34F919D25614440000000A0867B52C0B79ED71C82644440000000E0647B52C018C111C8CD66444000000060D57B52C079008DA1F6694440000000805C7A52C03EF34F9CC86E4440000000604E7B52C0A7A434E51C704440
\.


--
-- Name: test_regions_ogc_fid_seq; Type: SEQUENCE SET; Schema: public; Owner: oqt
--

SELECT pg_catalog.setval('public.test_regions_ogc_fid_seq', 37, true);


--
-- Name: test_regions test_regions_pkey; Type: CONSTRAINT; Schema: public; Owner: oqt
--

ALTER TABLE ONLY public.test_regions
    ADD CONSTRAINT test_regions_pkey PRIMARY KEY (ogc_fid);


--
-- Name: test_regions_geom_geom_idx; Type: INDEX; Schema: public; Owner: oqt
--

CREATE INDEX test_regions_geom_geom_idx ON public.test_regions USING gist (geom);


--
-- PostgreSQL database dump complete
--
