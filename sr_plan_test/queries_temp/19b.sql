SELECT MIN(n.name) AS voicing_actress,
       MIN(t.title) AS kung_fu_panda
FROM aka_name AS an,
     char_name AS chn,
     cast_info AS ci,
     company_name AS cn,
     info_type AS it,
     movie_companies AS mc,
     movie_info AS mi,
     name AS n,
     role_type AS rt,
     title AS t
WHERE ci.note = $1
  AND cn.country_code = $2
  AND it.info = $3
  AND mc.note LIKE $4
  AND (mc.note LIKE $5
       OR mc.note LIKE $6)
  AND mi.info IS NOT NULL
  AND (mi.info LIKE $7
       OR mi.info LIKE $8)
  AND n.gender = $9
  AND n.name LIKE $10
  AND rt.role = $11
  AND t.production_year BETWEEN $12 AND $13
  AND t.title LIKE $14
  AND t.id = mi.movie_id
  AND t.id = mc.movie_id
  AND t.id = ci.movie_id
  AND mc.movie_id = ci.movie_id
  AND mc.movie_id = mi.movie_id
  AND mi.movie_id = ci.movie_id
  AND cn.id = mc.company_id
  AND it.id = mi.info_type_id
  AND n.id = ci.person_id
  AND rt.id = ci.role_id
  AND n.id = an.person_id
  AND ci.person_id = an.person_id
  AND chn.id = ci.person_role_id;

