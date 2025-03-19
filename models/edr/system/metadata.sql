{{ config(materialized='table'
    , enabled = (target.type != 'fabric')) }}

SELECT
    '{{ elementary.get_elementary_package_version() }}' as dbt_pkg_version
