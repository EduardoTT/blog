# Generated by Django 4.1.7 on 2023-03-18 15:07

from django.db import migrations
import modelcluster.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0004_blogcategory"),
    ]

    operations = [
        migrations.AddField(
            model_name="blogpage",
            name="categories",
            field=modelcluster.fields.ParentalManyToManyField(
                blank=True, to="blog.blogcategory"
            ),
        ),
    ]
