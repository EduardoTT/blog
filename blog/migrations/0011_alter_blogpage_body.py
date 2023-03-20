# Generated by Django 4.1.7 on 2023-03-20 02:52

from django.db import migrations
import wagtail.blocks
import wagtail.embeds.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):
    dependencies = [
        ("blog", "0010_alter_blogpage_body"),
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
                    ),
                    ("image", wagtail.images.blocks.ImageChooserBlock()),
                    ("embed", wagtail.embeds.blocks.EmbedBlock()),
                ],
                blank=True,
                use_json_field=True,
                verbose_name="Page body",
            ),
        ),
    ]