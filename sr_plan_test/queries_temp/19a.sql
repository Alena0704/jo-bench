SELECT MIN(n.name) AS voicing_actress,
       MIN(t.title) AS voiced_movie
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
WHERE ci.note IN ($1,
                 $2,
                 $3,
                 $4)
  AND cn.country_code = $5
  AND it.info = $6
  AND mc.note IS NOT NULL
  AND (mc.note LIKE $7
       OR mc.note LIKE $8)
  AND mi.info IS NOT NULL
  AND (mi.info LIKE $9
       OR mi.info LIKE $10)
  AND n.gender = $11
  AND n.name LIKE $12
  AND rt.role = $13
  AND t.production_year BETWEEN $14 AND $15
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

