from django.db import models
from django.utils import timezone
from django.conf import settings

TEMPLATE = settings.TEMPLATE

class fly_line(models.Model):
    gene_name = models.CharField(
        max_length=128,
        blank=False
    )

    effector_type = models.CharField(
        max_length=16,
        choices=TEMPLATE.field_opts['effector_type'],
        blank=False
    )
    source_id = models.CharField(
        max_length=32,
        blank=True,
        default=""
    )

    ins_seqname = models.CharField(
       max_length=4,
       choices=TEMPLATE.field_opts['ins_seqname'],
       blank=True,
       default=""
    )

    ins_site = models.BigIntegerField(
        blank=True,
        null=True,
        default=None
    )

    cassette = models.CharField(
        max_length=32,
        choices=TEMPLATE.field_opts['cassette'],
        blank=False
    )
    dimerizer = models.CharField(
        max_length=16,
        choices=TEMPLATE.field_opts['dimerizer'],
        blank=False,
        default="zip"
    )

    status = models.CharField(
        max_length=32,
        blank=False,
        default="ava",
        choices=TEMPLATE.field_opts['status']
    )

    private = models.BooleanField(default=False, blank=False)

    contributor = models.CharField(
        max_length=256, blank=False, default=""
    )

    citation = models.CharField(max_length=1024, blank=True, default="")
    citation_url = models.URLField(
        max_length=1024, blank=True,
        default="https://www.ncbi.nlm.nih.gov/pmc/"
    )
    
    uploader = models.ForeignKey(
        "members.CustomUser",
        on_delete=models.SET_NULL,
        blank = True,
        null = True
    )
    

    contact = models.EmailField(max_length=256)
    private = models.BooleanField(default=False, blank=False)
    notes = models.CharField(
        max_length = 2048,
        blank = True, null = True, default = ""
    )
    need_review = models.BooleanField(default=False, blank=False)
    date_created = models.DateTimeField(default = timezone.now)
    removed = models.BooleanField(default=False,blank=False)

    def __str__(self):
        return self.gene_name + '-' + self.effector_type

