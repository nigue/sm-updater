# Stepmania linux Updater

## Documentations

https://pypi.org/project/Pixeldrain/1.0.1/

https://pypi.org/project/py7zr/

## Configuration

    - Create a file .env with 3 fields
        - ARCADE_ID_NAME
        - SUPABASE_USER_HASH
        - SUPABASE_API_KEY

## To work

    - use supabase phyton library
        - https://supabase.com/docs
    - use supabase stored procedure postgres
    - use supabase enumrated types to files
        - type files to zip or not
        - operative system
    - Generate report log, with success or errors in a supabase table
    - Read stats.xml and upload record using a sp in postgress
        - read xml with phyton
        - sp validate date and points
        - only update if points are upper


zip -rP qwer sm-updater.zip src/* main.py run.sh setup.py update.sh
unzip -P qwer sm-updater.zip