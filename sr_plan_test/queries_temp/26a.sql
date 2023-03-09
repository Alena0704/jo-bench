SELECT MIN(chn.name) AS character_name,
       MIN(mi_idx.info) AS rating,
       MIN(n.name) AS playing_actor,
       MIN(t.title) AS complete_hero_movie
FROM complete_cast AS cc,
     comp_cast_type AS cct1,
     comp_cast_type AS cct2,
     char_name AS chn,
     cast_info AS ci,
     info_type AS it2,
     keyword AS k,
     kind_type AS kt,
     movie_info_idx AS mi_idx,
     movie_keyword AS mk,
     name AS n,
     title AS t
WHERE cct1.kind = $1
  AND cct2.kind LIKE $2
  AND chn.name IS NOT NULL
  AND (chn.name LIKE $3
       OR chn.name LIKE $4)
  AND it2.info = $5
  AND k.keyword IN ($6,
                   $7,
                   $8,
                   $9,
                   $10,
                   $11,
                   $12,
                   $13,
                   $14,
                   $15)
  AND kt.kind = $16
  AND mi_idx.info > $17
  AND t.production_year > $18
  AND kt.id = t.kind_id
  AND t.id = mk.movie_id
  AND t.id = ci.movie_id
  AND t.id = cc.movie_id
  AND t.id = mi_idx.movie_id
  AND mk.movie_id = ci.movie_id
  AND mk.movie_id = cc.movie_id
  AND mk.movie_id = mi_idx.movie_id
  AND ci.movie_id = cc.movie_id
  AND ci.movie_id = mi_idx.movie_id
  AND cc.movie_id = mi_idx.movie_id
  AND chn.id = ci.person_role_id
  AND n.id = ci.person_id
  AND k.id = mk.keyword_id
  AND cct1.id = cc.subject_id
  AND cct2.id = cc.status_id
  AND it2.id = mi_idx.info_type_id;

