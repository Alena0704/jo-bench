SELECT MIN(an.name) AS acress_pseudonym,
       MIN(t.title) AS japanese_anime_movie
FROM aka_name AS an,
     cast_info AS ci,
     company_name AS cn,
     movie_companies AS mc,
     name AS n,
     role_type AS rt,
     title AS t
WHERE ci.note = $1
  AND cn.country_code = $2
  AND mc.note LIKE $3
  AND mc.note NOT LIKE $4
  AND (mc.note LIKE $5
       OR mc.note LIKE $6)
  AND n.name LIKE $7
  AND n.name NOT LIKE $8
  AND rt.role = $9
  AND t.production_year BETWEEN $10 AND $11
  AND (t.title LIKE $12
       OR t.title LIKE $13)
  AND an.person_id = n.id
  AND n.id = ci.person_id
  AND ci.movie_id = t.id
  AND t.id = mc.movie_id
  AND mc.company_id = cn.id
  AND ci.role_id = rt.id
  AND an.person_id = ci.person_id
  AND ci.movie_id = mc.movie_id;

