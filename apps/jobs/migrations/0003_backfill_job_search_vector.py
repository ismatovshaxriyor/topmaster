"""Populate search_vector for jobs that existed before the column was added."""
from django.contrib.postgres.search import SearchVector
from django.db import migrations


def backfill(apps, schema_editor):
    Job = apps.get_model("jobs", "Job")
    Job.objects.update(
        search_vector=SearchVector("title", weight="A", config="simple")
        + SearchVector("description", weight="B", config="simple")
    )


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0002_job_search_vector_job_job_search_vector_gin"),
    ]

    operations = [
        migrations.RunPython(backfill, migrations.RunPython.noop),
    ]
