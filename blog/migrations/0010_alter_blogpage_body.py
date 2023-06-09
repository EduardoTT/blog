# Generated by Django 4.1.7 on 2023-03-20 02:43

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0009_alter_blogpage_body"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blogpage",
            name="body",
            field=wagtail.fields.StreamField(
                [
                    (
                        "rich_text",
                        wagtail.blocks.RichTextBlock(
                            features=[
                                "h2",
                                "h3",
                                "h4",
                                "h5",
                                "h6",
                                "bold",
                                "italic",
                                "ol",
                                "ul",
                                "hr",
                                "link",
                                "document-link",
                                "strikethrough",
                                "code",
                                "blockquote",
                            ]
                        ),
                    )
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Page body",
            ),
        ),
    ]
