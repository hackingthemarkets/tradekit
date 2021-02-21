#!/usr/bin/env python 
 
import sys
sys.path.append('/app')
import dbwrapper as dbw


dbw.initDb()

with dbw.dbEngine.connect() as conn:
    
    result = conn.execute("""
            DO $$ DECLARE
                r RECORD;
            BEGIN
                FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                    EXECUTE 'DROP TABLE IF EXISTS ' || quote_ident(r.tablename) || ' CASCADE';
                END LOOP;
            END $$;
        """)