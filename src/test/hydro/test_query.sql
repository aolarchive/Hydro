{% autoescape off %}
            SELECT A,B,C,D,E,F, SUM(M1)
            FROM TEST_TB
            WHERE
            client = '{{CLIENT_ID}}'
            AND DATE BETWEEN '{{FROM_DATE}}' AND '{{TO_DATE}}'
            AND object_type NOT IN ('all objects')
            AND object_type IN ({{OBJECT_TYPES}})
            GROUP BY
            1, 2, 3, 4, 5, 6
{% endautoescape %}