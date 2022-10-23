EXTRACT_QUERY = """
SELECT jsonb_build_object(
   'id', fw.id,
   'title',fw.title,
   'description',fw.description,
   'rating',fw.rating,
   'type',fw.type,
   'created',fw.created,
   'modified',fw.modified,
   'people', COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'person_role', pfw.role,
               'person_id', p.id,
               'person_name', p.full_name
           )
       ) FILTER (WHERE p.id is not null),
       '[]'
   ),
   'genres', array_agg(DISTINCT g.name))
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
WHERE fw.modified > %s OR
g.modified > %s OR
p.modified > %s
GROUP BY fw.id
ORDER BY fw.modified;
"""
