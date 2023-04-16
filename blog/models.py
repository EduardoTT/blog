from django.db import models
from django import forms

from wagtailcodeblock.blocks import CodeBlock

from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel, InlinePanel, MultiFieldPanel
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.blocks import RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.embeds.blocks import EmbedBlock

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase, Tag


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [FieldPanel("intro")]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        blogpages = (
            self.get_children()
            .filter(blogpage__isnull=False)
            .live()
            .order_by("-first_published_at")
        )
        tags = Tag.objects.all()
        context["blogpages"] = blogpages
        context["tags"] = tags
        return context


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        "BlogPage", related_name="tagged_item", on_delete=models.CASCADE
    )


class BlogPage(Page):
    date = models.DateField("Post date")
    intro = models.CharField(max_length=255)
    body = StreamField(
        [
            (
                "rich_text",
                RichTextBlock(
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
                        "blockquote",
                    ]
                ),
            ),
            ("code", CodeBlock(label="code", default_language="python")),
            ("image", ImageChooserBlock()),
            ("embed", EmbedBlock()),
        ],
        verbose_name="Page body",
        blank=True,
        use_json_field=True,
    )
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)
    categories = ParentalManyToManyField("blog.BlogCategory", blank=True)

    search_fields = Page.search_fields + [
        index.SearchField("intro"),
        index.SearchField("body"),
    ]

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [
                FieldPanel("date"),
                FieldPanel("tags"),
                FieldPanel("categories", widget=forms.CheckboxSelectMultiple),
            ],
            heading="Blog information",
        ),
        FieldPanel("intro"),
        FieldPanel("body"),
        InlinePanel("gallery_images", label="Gallery images"),
    ]


class BlogPageGalleryImage(Orderable):
    page = ParentalKey(
        BlogPage, on_delete=models.CASCADE, related_name="gallery_images"
    )
    image = models.ForeignKey(
        "wagtailimages.Image", on_delete=models.CASCADE, related_name="+"
    )
    caption = models.CharField(blank=True, max_length=250)

    panels = [
        FieldPanel("image"),
        FieldPanel("caption"),
    ]


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    panels = [FieldPanel("name"), FieldPanel("icon")]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "blog categories"


class BlogTagIndexPage(Page):
    def get_context(self, request):
        tag = request.GET.get("tag")
        blogpages = BlogPage.objects.filter(tags__name=tag)

        context = super().get_context(request)
        context["blogpages"] = blogpages
        return context
